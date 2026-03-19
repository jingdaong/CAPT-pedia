# CAPT-pedia

A Telegram bot that helps NUS CAPT (College of Alice & Peter Tan) freshmen discover committees, browse FAQs, and ask anonymous questions to directors.

---

## Features

| Feature | Description |
|---------|-------------|
| 📋 Committee Listing | Browse all CAPT committees from a single menu |
| 📌 Committee Details | View each committee's overview, Instagram/Telegram handles, website and director contacts |
| ❓ FAQs | Browse per-committee FAQs with a single tap |
| ✉️ Anonymous Questions | Send questions anonymously to committee directors via the bot |
| 💬 Admin Replies | Directors reply to anonymous questions using `/reply` and the bot delivers the response |
| 🌐 Directors Portal | Web dashboard for directors to view pending questions and reply from one place |
| 🔐 NUS Email 2-Step Login | Portal sign-in via NUS email + one-time verification code |

---

## Judge Guide: Local Setup and Usage

Use this section to run the full hackathon demo locally (Telegram bot + directors portal).

### 1. Prerequisites

- Python 3.10+
- A Telegram account
- A Telegram Bot token from [@BotFather](https://t.me/BotFather)
- The Telegram **chat ID** of the admin/directors group that receives anonymous questions
- SMTP credentials for OTP email login in the portal
- *(Optional)* Node.js 18+ only if you want to rebuild frontend assets

### 2. Clone and set up Python environment

```bash
git clone https://github.com/jingdaong/CAPT-pedia.git
cd CAPT-pedia
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Set at least these values in `.env`:

```dotenv
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_CHAT_ID=your_admin_group_chat_id_here
JWT_SECRET=your_random_secret

SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_username
SMTP_PASSWORD=your_smtp_password
SMTP_FROM=your_sender_email

SECURE_COOKIES=false
ALLOWED_EMAIL_DOMAINS=u.nus.edu
```

For local judging with non-NUS email, set `ALLOWED_EMAIL_DOMAINS` to your email domain (for example `gmail.com`).

Generate a JWT secret quickly with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> **Tip:** To find a group's chat ID, add [@userinfobot](https://t.me/userinfobot) to the group and send any message.

### 4. Run locally (2 terminals)

Terminal A (Directors Portal backend + web UI):

```bash
source .venv/bin/activate
python server.py
```

Terminal B (Telegram bot):

```bash
source .venv/bin/activate
python bot.py
```

Portal URL: `http://localhost:8000`

### Important data note for judges

This project uses a local SQLite database file (`DB_PATH`, default: `capt_pedia.db`).

- Data is machine-local by default.
- If `bot.py` and `server.py` run on different machines, questions will not sync automatically.
- For judging, run both services on the same machine (recommended), or ensure both point to the same shared database.

### 5. Judge demo flow

1. Open Telegram, message your bot, and run `/start`.
2. Select a committee and submit an anonymous question.
3. Open `http://localhost:8000`, sign in with email OTP, and view pending questions.
4. Reply to the pending question from the portal.
5. Confirm the original Telegram user receives the reply message.

### 6. Optional: rebuild the portal frontend

Only needed if frontend source files are changed.

```bash
cd frontend
npm install
npm run build
cd ..
```

---

## Bot Commands

| Command | Who | Description |
|---------|-----|-------------|
| `/start` | Anyone | Show the welcome message and committee list |
| `/help` | Anyone | Show available commands |
| `/cancel` | Anyone | Cancel the current action and return to the menu |
| `/reply <ID> <text>` | Admins only | Reply to an anonymous question by its ID |

---

## User Flow

```
/start
 └─ Committee List
     └─ [Select Committee]
         ├─ Committee Details (overview, resources, directors)
         │   ├─ ❓ View FAQs
         │   │   ├─ [Select FAQ] → Answer → Back to FAQs
         │   │   └─ 💬 Others (Ask Anonymously) → type question → forwarded to admins
         │   └─ ✉️ Ask a Question → type question → forwarded to admins
         └─ 🔙 Back to Committees
```

---

## Adding / Editing Committees

All committee data lives in `data/committees.py`. Each entry follows this structure:

```python
{
    "name":       "Committee Name",          # Display name
    "short_name": "comm_key",                # Unique identifier (no spaces)
    "overview":   "What the committee does.",
    "ig_handle":  "@instagram_handle",       # Empty string if none
    "tele_handle":"@telegram_handle",        # Empty string if none
    "website":    "https://...",             # Empty string if none
    "directors": [
        {"name": "Role Title", "tele_handle": "@handle"},
    ],
    "faqs": [
        {"question": "How do I join?", "answer": "..."},
    ],
}
```

After editing, run the tests to verify data integrity:

```bash
python -m pytest tests.py -v
```

---

## Project Structure

```
CAPT-pedia/
├── bot.py              # Main bot logic and conversation handlers
├── server.py           # FastAPI backend for directors portal
├── database.py         # SQLAlchemy models/shared DB helpers
├── static/
│   └── index.html      # Directors portal frontend
├── data/
│   ├── __init__.py
│   └── committees.py   # Committee data (overview, FAQs, resources)
├── tests.py            # Unit tests
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `python-telegram-bot==20.7` | Telegram Bot API wrapper |
| `python-dotenv==1.0.1` | Load `.env` configuration |
| `fastapi==0.111.0` | Directors portal backend APIs |
| `uvicorn[standard]==0.29.0` | ASGI server for portal backend |
| `sqlalchemy==2.0.30` | Persistent storage for questions and OTP codes |
| `httpx==0.27.0` | Outbound HTTP calls (Telegram API from portal) |
| `python-jose[cryptography]==3.3.0` | JWT session signing and verification |
