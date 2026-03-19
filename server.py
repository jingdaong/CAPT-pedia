"""
CAPT-pedia Directors Portal - FastAPI server
============================================

Environment variables (in .env or host):
  BOT_TOKEN                      - Telegram Bot API token (shared with bot.py)
  JWT_SECRET                     - Random secret for signing JWTs
                                   (generate with: python -c "import secrets; print(secrets.token_hex(32))")
  DB_PATH                        - Path to SQLite DB file (default: capt_pedia.db)
  PORTAL_PORT                    - Port to listen on (default: 8000)
  SECURE_COOKIES                 - Set to "false" for local HTTP development (default: "true")

  ALLOWED_EMAIL_DOMAINS          - Comma-separated domains allowed to sign in
                                   (default: u.nus.edu)
  OTP_LENGTH                     - Number of digits in OTP (default: 6)
  OTP_TTL_MINUTES                - OTP expiry in minutes (default: 10)
  OTP_RESEND_COOLDOWN_SECONDS    - Minimum seconds between OTP requests (default: 60)
  OTP_MAX_ATTEMPTS               - Max wrong attempts per OTP (default: 5)

  SMTP_HOST                      - SMTP server hostname (required for email OTP)
  SMTP_PORT                      - SMTP port (default: 587)
  SMTP_USERNAME                  - SMTP username (optional)
  SMTP_PASSWORD                  - SMTP password (optional)
  SMTP_FROM                      - From-address for OTP emails (optional)
  SMTP_USE_TLS                   - "true" to use STARTTLS (default: "true")

Run:
  python server.py
"""

import hashlib
import logging
import os
import random
import re
import smtplib
import string
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from typing import Annotated, Optional

import httpx
from dotenv import load_dotenv
from fastapi import Cookie, Depends, FastAPI, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from data.committees import COMMITTEES
from database import (
    Director,
    LoginOTP,
    QuestionStatus,
    answer_question,
    create_login_otp,
    get_db,
    get_latest_login_otp,
    get_or_create_director,
    get_question,
    init_db,
    list_questions,
)

load_dotenv()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
JWT_SECRET: str = os.environ["JWT_SECRET"]
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 8
SECURE_COOKIES = os.environ.get("SECURE_COOKIES", "true").lower() == "true"

ALLOWED_EMAIL_DOMAINS = tuple(
    domain.strip().lower()
    for domain in os.environ.get("ALLOWED_EMAIL_DOMAINS", "u.nus.edu").split(",")
    if domain.strip()
)
OTP_LENGTH = int(os.environ.get("OTP_LENGTH", "6"))
OTP_TTL_MINUTES = int(os.environ.get("OTP_TTL_MINUTES", "10"))
OTP_RESEND_COOLDOWN_SECONDS = int(os.environ.get("OTP_RESEND_COOLDOWN_SECONDS", "60"))
OTP_MAX_ATTEMPTS = int(os.environ.get("OTP_MAX_ATTEMPTS", "5"))

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_FROM = os.environ.get("SMTP_FROM") or SMTP_USERNAME or "no-reply@u.nus.edu"
SMTP_USE_TLS = os.environ.get("SMTP_USE_TLS", "true").lower() == "true"

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

# ---------------------------------------------------------------------------
# App init
# ---------------------------------------------------------------------------

app = FastAPI(title="CAPT-pedia Directors Portal", docs_url=None, redoc_url=None)
init_db()


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------


def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(tz=timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS)
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session. Please sign in again.",
        )


def _normalise_email(email: str) -> str:
    return email.strip().lower()


def _is_allowed_nus_email(email: str) -> bool:
    if not EMAIL_PATTERN.fullmatch(email):
        return False
    return any(email.endswith(f"@{domain}") for domain in ALLOWED_EMAIL_DOMAINS)


def _director_name_from_email(email: str) -> str:
    local_part = email.split("@", 1)[0]
    return local_part.replace(".", " ").replace("_", " ").title()


def _generate_otp_code() -> str:
    return "".join(random.choice(string.digits) for _ in range(OTP_LENGTH))


def _hash_otp(email: str, code: str) -> str:
    salted = f"{email}:{code}:{JWT_SECRET}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def _send_otp_email(recipient: str, code: str) -> None:
    if not SMTP_HOST:
        raise RuntimeError("SMTP_HOST is not configured")

    subject = "CAPT-pedia verification code"
    body = (
        "Your CAPT-pedia Directors Portal verification code is:\n\n"
        f"{code}\n\n"
        f"This code expires in {OTP_TTL_MINUTES} minutes.\n"
        "If you did not request this login, you can ignore this email."
    )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = SMTP_FROM
    message["To"] = recipient
    message.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as smtp:
        if SMTP_USE_TLS:
            smtp.starttls()
        if SMTP_USERNAME and SMTP_PASSWORD:
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
        smtp.send_message(message)


def _set_auth_cookie(response: JSONResponse, director: Director) -> None:
    token = create_access_token({"sub": director.email, "name": director.name})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=SECURE_COOKIES,
        samesite="strict",
        max_age=JWT_EXPIRE_HOURS * 3600,
    )


def get_current_director(
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db),
) -> Director:
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated.")

    payload = _decode_token(access_token)
    email: Optional[str] = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Malformed token.")

    director = db.query(Director).filter(Director.email == email).first()
    if director is None:
        raise HTTPException(status_code=401, detail="Account not found.")
    return director


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------


class RequestCodeRequest(BaseModel):
    email: str


class VerifyCodeRequest(BaseModel):
    email: str
    code: str


class ReplyRequest(BaseModel):
    reply_text: str


# ---------------------------------------------------------------------------
# Auth endpoints
# ---------------------------------------------------------------------------


@app.post("/auth/request-code")
def request_login_code(body: RequestCodeRequest, db: Session = Depends(get_db)):
    email = _normalise_email(body.email)

    if not _is_allowed_nus_email(email):
        raise HTTPException(
            status_code=403,
            detail="Access is restricted to NUS emails. Please use your @u.nus.edu account.",
        )

    latest = get_latest_login_otp(db, email)
    now = datetime.utcnow()
    if latest and not latest.consumed:
        age_seconds = int((now - latest.created_at).total_seconds())
        if age_seconds < OTP_RESEND_COOLDOWN_SECONDS:
            wait_seconds = OTP_RESEND_COOLDOWN_SECONDS - age_seconds
            raise HTTPException(
                status_code=429,
                detail=f"Please wait {wait_seconds}s before requesting another code.",
            )

    code = _generate_otp_code()
    code_hash = _hash_otp(email, code)
    expires_at = now + timedelta(minutes=OTP_TTL_MINUTES)

    db.query(LoginOTP).filter(
        LoginOTP.email == email,
        LoginOTP.consumed.is_(False),
    ).update({LoginOTP.consumed: True}, synchronize_session=False)
    db.commit()

    try:
        _send_otp_email(email, code)
    except Exception as exc:
        logger.error("Failed to send OTP email to %s: %s", email, exc)
        raise HTTPException(
            status_code=502,
            detail="Failed to send verification code email. Please try again later.",
        )

    create_login_otp(
        db=db,
        email=email,
        code_hash=code_hash,
        expires_at=expires_at,
    )
    return {"message": "Verification code sent.", "email": email}


@app.post("/auth/verify-code")
def verify_login_code(body: VerifyCodeRequest, db: Session = Depends(get_db)) -> JSONResponse:
    email = _normalise_email(body.email)
    code = body.code.strip()

    if not _is_allowed_nus_email(email):
        raise HTTPException(status_code=403, detail="Invalid NUS email address.")
    if not (code.isdigit() and len(code) == OTP_LENGTH):
        raise HTTPException(status_code=400, detail=f"Code must be {OTP_LENGTH} digits.")

    otp = get_latest_login_otp(db, email)
    if otp is None or otp.consumed:
        raise HTTPException(
            status_code=401,
            detail="No active verification code. Request a new code first.",
        )

    now = datetime.utcnow()
    if otp.expires_at < now:
        otp.consumed = True
        db.commit()
        raise HTTPException(status_code=401, detail="Verification code has expired.")

    if otp.attempts >= OTP_MAX_ATTEMPTS:
        otp.consumed = True
        db.commit()
        raise HTTPException(
            status_code=429,
            detail="Too many failed attempts. Request a new code.",
        )

    if otp.code_hash != _hash_otp(email, code):
        otp.attempts += 1
        if otp.attempts >= OTP_MAX_ATTEMPTS:
            otp.consumed = True
        db.commit()
        raise HTTPException(status_code=401, detail="Incorrect verification code.")

    otp.consumed = True
    db.commit()

    director = get_or_create_director(
        db,
        email=email,
        name=_director_name_from_email(email),
    )
    response = JSONResponse({"name": director.name, "email": director.email})
    _set_auth_cookie(response, director)
    return response


@app.post("/auth/logout")
def logout() -> JSONResponse:
    response = JSONResponse({"message": "Logged out."})
    response.delete_cookie("access_token")
    return response


@app.get("/api/me")
def get_me(director: Annotated[Director, Depends(get_current_director)]):
    return {"email": director.email, "name": director.name}


# ---------------------------------------------------------------------------
# Questions endpoints
# ---------------------------------------------------------------------------


@app.get("/api/questions")
def api_list_questions(
    filter: Optional[str] = None,
    committee: Optional[str] = None,
    director: Annotated[Director, Depends(get_current_director)] = None,
    db: Session = Depends(get_db),
):
    if filter and filter not in {QuestionStatus.PENDING.value, QuestionStatus.ANSWERED.value}:
        raise HTTPException(status_code=400, detail="Invalid filter value.")

    questions = list_questions(db, status=filter)
    if committee:
        questions = [q for q in questions if q.committee_short_name == committee]

    return [
        {
            "id": q.id,
            "committee_short_name": q.committee_short_name,
            "committee_name": q.committee_name,
            "question_text": q.question_text,
            "status": q.status.value if isinstance(q.status, QuestionStatus) else str(q.status),
            "created_at": q.created_at.isoformat(),
            "answered_at": q.answered_at.isoformat() if q.answered_at else None,
            "answered_by": q.answered_by,
            "reply_text": q.reply_text,
        }
        for q in questions
    ]


@app.post("/api/questions/{question_id}/reply")
async def api_reply_question(
    question_id: str,
    body: ReplyRequest,
    director: Annotated[Director, Depends(get_current_director)],
    db: Session = Depends(get_db),
):
    """Send a Telegram reply to the user and mark the question answered."""
    reply_text = body.reply_text.strip()
    if not reply_text:
        raise HTTPException(status_code=400, detail="Reply text cannot be empty.")

    qid = question_id.upper()
    q = get_question(db, qid)
    if q is None:
        raise HTTPException(status_code=404, detail="Question not found.")
    if q.status == QuestionStatus.ANSWERED:
        raise HTTPException(status_code=409, detail="This question has already been answered.")

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    tg_text = (
        f"💬 <b>Reply to your anonymous question</b> (ID: <code>{qid}</code>)\n\n"
        f"{reply_text}"
    )
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            telegram_url,
            json={"chat_id": q.telegram_user_id, "text": tg_text, "parse_mode": "HTML"},
        )

    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Failed to deliver reply via Telegram. Please try again.",
        )

    answered = answer_question(db, qid, reply_text, director.email)
    return {
        "id": answered.id,
        "status": answered.status.value if isinstance(answered.status, QuestionStatus) else str(answered.status),
        "answered_by": answered.answered_by,
        "answered_at": answered.answered_at.isoformat(),
    }


@app.get("/api/committees")
def api_committees(director: Annotated[Director, Depends(get_current_director)]):
    return [{"short_name": c["short_name"], "name": c["name"]} for c in COMMITTEES]


# ---------------------------------------------------------------------------
# Serve the single-page portal app
# ---------------------------------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")


@app.get("/{full_path:path}", include_in_schema=False)
def serve_spa(full_path: str):
    return FileResponse("static/index.html")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORTAL_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)