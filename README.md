# CAPT-pedia

A Telegram bot that helps NUS CAPT (College of Alice & Peter Tan) freshmen discover committees, browse FAQs, ask anonymous questions to directors, and chat with an AI assistant.

---

## Features

| Feature | Description |
|---------|-------------|
| 📋 Committee Listing | Browse all CAPT committees from a single menu |
| 📌 Committee Details | View each committee's overview, Instagram/Telegram handles, website and director contacts |
| ❓ FAQs | Browse per-committee FAQs with a single tap |
| ✉️ Anonymous Questions | Send questions anonymously to committee directors via the bot |
| 💬 Admin Replies | Directors reply to anonymous questions using `/reply` and the bot delivers the response |
| 🤖 AI Chatbot | Ask the AI assistant (powered by OpenAI) any CAPT-related question using `/ask` |

---

## Quick Start

### 1. Prerequisites

- Python 3.10+
- A Telegram Bot token — create one via [@BotFather](https://t.me/BotFather)
- The Telegram **chat ID** of the admin/directors group where anonymous questions will be forwarded
- *(Optional)* An OpenAI API key for the AI chatbot feature

### 2. Clone & Install

```bash
git clone https://github.com/jingdaong/CAPT-pedia.git
cd CAPT-pedia
pip install -r requirements.txt
```

### 3. Configure

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
# Required
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_CHAT_ID=your_admin_group_chat_id_here

# Optional – enables the /ask AI chatbot feature
OPENAI_API_KEY=your_openai_api_key_here
```

> **Tip:** To find a group's chat ID, add [@userinfobot](https://t.me/userinfobot) to the group and send any message.

### 4. Run

```bash
python bot.py
```

---

## Bot Commands

| Command | Who | Description |
|---------|-----|-------------|
| `/start` | Anyone | Show the welcome message and committee list |
| `/help` | Anyone | Show available commands |
| `/ask <question>` | Anyone | Ask the AI assistant a CAPT-related question |
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
| `openai==1.12.0` | AI chatbot (optional) |
