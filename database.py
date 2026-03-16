"""
Database models and helpers for CAPT-pedia.

SQLite-backed via SQLAlchemy (synchronous).

Tables:
  questions  — anonymous questions submitted by users via Telegram
    directors  — portal accounts for authenticated directors
    login_otps — one-time verification codes for portal sign-in
"""

import enum
import os
from datetime import datetime
from typing import Generator, Optional

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# ---------------------------------------------------------------------------
# Engine / session
# ---------------------------------------------------------------------------

DB_PATH = os.environ.get("DB_PATH", "capt_pedia.db")

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------------
# Base & enums
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


class QuestionStatus(str, enum.Enum):
    PENDING = "pending"
    ANSWERED = "answered"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Question(Base):
    __tablename__ = "questions"

    id = Column(String(8), primary_key=True)
    committee_short_name = Column(String(64), nullable=False, index=True)
    committee_name = Column(String(128), nullable=False)
    question_text = Column(Text, nullable=False)
    telegram_user_id = Column(Integer, nullable=False)
    status = Column(
        Enum(QuestionStatus),
        default=QuestionStatus.PENDING,
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    answered_at = Column(DateTime, nullable=True)
    answered_by = Column(String(256), nullable=True)   # director email
    reply_text = Column(Text, nullable=True)


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), unique=True, nullable=False, index=True)
    name = Column(String(256), nullable=False)
    google_sub = Column(String(256), unique=True, nullable=True)  # Legacy SSO subject ID
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class LoginOTP(Base):
    __tablename__ = "login_otps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(256), nullable=False, index=True)
    code_hash = Column(String(128), nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    consumed = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# ---------------------------------------------------------------------------
# DB lifecycle helpers
# ---------------------------------------------------------------------------

def init_db() -> None:
    """Create all tables if they don't exist yet."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Question helpers
# ---------------------------------------------------------------------------

def create_question(
    db: Session,
    question_id: str,
    committee_short_name: str,
    committee_name: str,
    question_text: str,
    telegram_user_id: int,
) -> Question:
    q = Question(
        id=question_id,
        committee_short_name=committee_short_name,
        committee_name=committee_name,
        question_text=question_text,
        telegram_user_id=telegram_user_id,
        status=QuestionStatus.PENDING,
        created_at=datetime.utcnow(),
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


def get_question(db: Session, question_id: str) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()


def list_questions(db: Session, status: Optional[str] = None) -> list[Question]:
    q = db.query(Question)
    if status:
        q = q.filter(Question.status == status)
    return q.order_by(Question.created_at.desc()).all()


def answer_question(
    db: Session,
    question_id: str,
    reply_text: str,
    answered_by: str,
) -> Optional[Question]:
    q = get_question(db, question_id)
    if q is None:
        return None
    q.status = QuestionStatus.ANSWERED
    q.reply_text = reply_text
    q.answered_by = answered_by
    q.answered_at = datetime.utcnow()
    db.commit()
    db.refresh(q)
    return q


# ---------------------------------------------------------------------------
# Director helpers
# ---------------------------------------------------------------------------

def get_or_create_director(
    db: Session,
    email: str,
    name: str,
    google_sub: Optional[str] = None,
) -> Director:
    """Return existing director or create a new one on first sign-in."""
    director = db.query(Director).filter(Director.email == email).first()
    if director is None and google_sub:
        director = db.query(Director).filter(Director.google_sub == google_sub).first()
    if director is None:
        director = Director(email=email, name=name, google_sub=google_sub)
        db.add(director)
        db.commit()
        db.refresh(director)
    elif google_sub and director.google_sub is None:
        director.google_sub = google_sub
        db.commit()
    return director


def create_login_otp(
    db: Session,
    email: str,
    code_hash: str,
    expires_at: datetime,
) -> LoginOTP:
    otp = LoginOTP(
        email=email,
        code_hash=code_hash,
        expires_at=expires_at,
        attempts=0,
        consumed=False,
        created_at=datetime.utcnow(),
    )
    db.add(otp)
    db.commit()
    db.refresh(otp)
    return otp


def get_latest_login_otp(db: Session, email: str) -> Optional[LoginOTP]:
    return (
        db.query(LoginOTP)
        .filter(LoginOTP.email == email)
        .order_by(LoginOTP.created_at.desc())
        .first()
    )
