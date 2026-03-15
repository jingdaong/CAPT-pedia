"""
CAPT-pedia Telegram Bot
=======================
A bot that helps NUS CAPT freshmen discover committees, browse FAQs,
and ask anonymous questions to committee directors.

Environment variables (set in .env or the host environment):
  BOT_TOKEN       - Telegram Bot API token (required)
  ADMIN_CHAT_ID   - Telegram chat ID for the admin / directors group (required)
  OPENAI_API_KEY  - OpenAI API key for the AI chatbot feature (optional)

Run:
  python bot.py
"""

import html
import logging
import os
import uuid
from typing import Optional

from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from data.committees import (
    ACE_SUBCOMMITTEES,
    ACE_SUBCOMMITTEES_BY_KEY,
    COMMITTEES,
    COMMITTEES_BY_KEY,
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
ADMIN_CHAT_ID: str = os.environ["ADMIN_CHAT_ID"]
OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")

# ---------------------------------------------------------------------------
# Conversation states
# ---------------------------------------------------------------------------
(
    SELECT_COMM,
    VIEW_COMM,
    VIEW_FAQS,
    VIEW_FAQ_ANSWER,
    ASK_QUESTION_MENU,
    AWAITING_QUESTION,
) = range(6)

# ---------------------------------------------------------------------------
# In-memory store for pending anonymous questions
# Maps question_id (str) -> sender user_id (int)
# ---------------------------------------------------------------------------
pending_questions: dict[str, int] = {}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

WELCOME_TEXT = (
    "👋 <b>Welcome to CAPT-pedia!</b>\n\n"
    "I'm here to help you learn about the committees at "
    "<b>College of Alice &amp; Peter Tan (CAPT)</b>, NUS.\n\n"
    "🔍 <b>What would you like to do?</b>\n"
    "• Browse a committee to read its overview, resources and FAQs\n"
    "• Ask an anonymous question to a committee's directors\n"
    "• Chat with the AI assistant for quick answers\n\n"
    "👇 <b>Select a committee below to get started:</b>"
)

HELP_TEXT = (
    "ℹ️ <b>CAPT-pedia Help</b>\n\n"
    "/start — Show the committee menu\n"
    "/help  — Show this help message\n"
    "/ask   — Ask the AI assistant a question\n\n"
    "<i>Tip: You can also tap</i> <b>Ask a Question</b> <i>inside any committee "
    "to send an anonymous message to its directors.</i>"
)


def build_committee_keyboard() -> InlineKeyboardMarkup:
    """Return an inline keyboard listing all committees."""
    buttons = [
        [InlineKeyboardButton(c["name"], callback_data=f"comm|{c['short_name']}")]
        for c in COMMITTEES
    ]
    return InlineKeyboardMarkup(buttons)


def get_committee(short_name: str) -> Optional[dict]:
    """Return a committee from top-level or ACE subcommittee dictionaries."""
    return COMMITTEES_BY_KEY.get(short_name) or ACE_SUBCOMMITTEES_BY_KEY.get(short_name)


def is_ace_subcommittee(short_name: str) -> bool:
    """Whether the key belongs to one of the ACE subcommittees."""
    return short_name in ACE_SUBCOMMITTEES_BY_KEY


def build_ace_subcommittee_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard listing all ACE subcommittees/projects."""
    buttons = [
        [InlineKeyboardButton(c["name"], callback_data=f"acesub|{c['short_name']}")]
        for c in ACE_SUBCOMMITTEES
    ]
    buttons.append([InlineKeyboardButton("🔙 Back to Committees", callback_data="back|main")])
    return InlineKeyboardMarkup(buttons)


def build_ace_menu_text() -> str:
    """Formatted ACE overview text shown before selecting an ACE subcommittee."""
    ace = COMMITTEES_BY_KEY["ace"]
    return (
        f"📋 <b>{html.escape(ace['name'])}</b>\n\n"
        f"{html.escape(ace['overview'])}\n\n"
        "👇 <b>Select an ACE subcommittee/project:</b>"
    )


def build_comm_detail_text(comm: dict) -> str:
    """Format a committee overview + resources message."""
    lines = [
        f"📋 <b>{html.escape(comm['name'])}</b>\n",
        html.escape(comm["overview"]),
        "",
        "📌 <b>Resources</b>",
    ]
    if comm["ig_handle"]:
        lines.append(f"• Instagram: {html.escape(comm['ig_handle'])}")
    if comm["tele_handle"]:
        lines.append(f"• Telegram:  {html.escape(comm['tele_handle'])}")
    if comm["website"]:
        lines.append(f"• Website:   {html.escape(comm['website'])}")

    if comm["directors"]:
        lines.append("")
        lines.append("👤 <b>Directors / ExCo Leads</b>")
        for d in comm["directors"]:
            entry = f"• {html.escape(d['name'])}"
            if d["tele_handle"]:
                entry += f": {html.escape(d['tele_handle'])}"
            lines.append(entry)

    return "\n".join(lines)


def build_comm_action_keyboard(short_name: str, back_target: str = "main") -> InlineKeyboardMarkup:
    """Inline keyboard shown below a committee detail."""
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "❓ View FAQs", callback_data=f"faqs|{short_name}"
                ),
                InlineKeyboardButton(
                    "✉️ Ask a Question", callback_data=f"ask|{short_name}"
                ),
            ],
            [
                InlineKeyboardButton(
                    "🔙 Back to ACE" if back_target == "ace" else "🔙 Back to Committees",
                    callback_data=f"back|{back_target}",
                )
            ],
        ]
    )


def build_faq_keyboard(short_name: str) -> InlineKeyboardMarkup:
    """Return an inline keyboard listing all FAQs for a committee."""
    comm = get_committee(short_name)
    if comm is None:
        return InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Back to Committees", callback_data="back|main")]]
        )
    buttons = [
        [
            InlineKeyboardButton(
                faq["question"], callback_data=f"faq|{short_name}|{i}"
            )
        ]
        for i, faq in enumerate(comm["faqs"])
    ]
    buttons.append(
        [
            InlineKeyboardButton(
                "💬 Others (Ask Anonymously)", callback_data=f"ask|{short_name}"
            )
        ]
    )
    buttons.append(
        [InlineKeyboardButton("🔙 Back to Committee", callback_data=f"comm|{short_name}")]
    )
    return InlineKeyboardMarkup(buttons)


def build_faq_answer_keyboard(short_name: str) -> InlineKeyboardMarkup:
    """Keyboard shown after displaying an FAQ answer."""
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔙 Back to FAQs", callback_data=f"faqs|{short_name}")],
            [
                InlineKeyboardButton(
                    "🏠 Back to Committees", callback_data="back|main"
                )
            ],
        ]
    )


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point — display welcome message and committee list."""
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=build_committee_keyboard(),
    )
    return SELECT_COMM


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help information."""
    await update.message.reply_text(HELP_TEXT, parse_mode=ParseMode.HTML)


# --- Committee selection ---

async def show_committee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show committee detail when user taps a committee button."""
    query = update.callback_query
    await query.answer()

    short_name = query.data.split("|")[1]

    # ACE is shown as a parent menu first, then users choose a specific subcommittee.
    if short_name == "ace":
        context.user_data["current_comm"] = short_name
        await query.edit_message_text(
            build_ace_menu_text(),
            parse_mode=ParseMode.HTML,
            reply_markup=build_ace_subcommittee_keyboard(),
        )
        return VIEW_COMM

    comm = get_committee(short_name)
    if comm is None:
        await query.edit_message_text("Committee not found. Please try /start again.")
        return SELECT_COMM

    context.user_data["current_comm"] = short_name
    back_target = "ace" if is_ace_subcommittee(short_name) else "main"
    await query.edit_message_text(
        build_comm_detail_text(comm),
        parse_mode=ParseMode.HTML,
        reply_markup=build_comm_action_keyboard(short_name, back_target=back_target),
    )
    return VIEW_COMM


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to the main committee list."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        WELCOME_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=build_committee_keyboard(),
    )
    return SELECT_COMM


async def back_to_ace(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to the ACE subcommittee list."""
    query = update.callback_query
    await query.answer()
    context.user_data["current_comm"] = "ace"
    await query.edit_message_text(
        build_ace_menu_text(),
        parse_mode=ParseMode.HTML,
        reply_markup=build_ace_subcommittee_keyboard(),
    )
    return VIEW_COMM


async def show_ace_subcommittee(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Show one ACE subcommittee after the user taps it in the ACE submenu."""
    query = update.callback_query
    await query.answer()

    short_name = query.data.split("|")[1]
    comm = ACE_SUBCOMMITTEES_BY_KEY.get(short_name)
    if comm is None:
        await query.edit_message_text("ACE subcommittee not found. Please try /start again.")
        return SELECT_COMM

    context.user_data["current_comm"] = short_name
    await query.edit_message_text(
        build_comm_detail_text(comm),
        parse_mode=ParseMode.HTML,
        reply_markup=build_comm_action_keyboard(short_name, back_target="ace"),
    )
    return VIEW_COMM


# --- FAQ flow ---

async def show_faqs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show the FAQ list for a committee."""
    query = update.callback_query
    await query.answer()

    short_name = query.data.split("|")[1]
    comm = get_committee(short_name)
    if comm is None:
        await query.edit_message_text("Committee not found. Please try /start again.")
        return SELECT_COMM

    context.user_data["current_comm"] = short_name

    if not comm["faqs"]:
        await query.edit_message_text(
            f"No FAQs available for <b>{html.escape(comm['name'])}</b> yet.\n"
            "You can submit a question using the button below.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✉️ Ask a Question", callback_data=f"ask|{short_name}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🔙 Back to Committee",
                            callback_data=f"comm|{short_name}",
                        )
                    ],
                ]
            ),
        )
        return VIEW_FAQS

    await query.edit_message_text(
        f"<b>{html.escape(comm['name'])} — FAQs</b>\n\nSelect a question to see the answer:",
        parse_mode=ParseMode.HTML,
        reply_markup=build_faq_keyboard(short_name),
    )
    return VIEW_FAQS


async def show_faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the answer to a specific FAQ."""
    query = update.callback_query
    await query.answer()

    _, short_name, idx_str = query.data.split("|")
    comm = get_committee(short_name)
    if comm is None:
        await query.edit_message_text("Committee not found. Please try /start again.")
        return SELECT_COMM

    idx = int(idx_str)
    faq = comm["faqs"][idx]

    text = (
        f"<b>{html.escape(comm['name'])}</b>\n\n"
        f"❓ <b>{html.escape(faq['question'])}</b>\n\n"
        f"{html.escape(faq['answer'])}"
    )
    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=build_faq_answer_keyboard(short_name),
    )
    return VIEW_FAQ_ANSWER


# --- Anonymous question flow ---

async def ask_question_prompt(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Prompt the user to type their anonymous question."""
    query = update.callback_query
    await query.answer()

    short_name = query.data.split("|")[1]
    comm = get_committee(short_name)
    if comm is None:
        await query.edit_message_text("Committee not found. Please try /start again.")
        return SELECT_COMM

    context.user_data["current_comm"] = short_name
    await query.edit_message_text(
        f"✉️ <b>Ask {html.escape(comm['name'])} Anonymously</b>\n\n"
        "Type your question below and it will be forwarded anonymously "
        "to the committee directors.\n\n"
        "<i>Your identity will NOT be shared.</i>\n\n"
        "Send /cancel to go back without asking.",
        parse_mode=ParseMode.HTML,
    )
    return AWAITING_QUESTION


async def receive_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Receive the user's question and forward it to admins anonymously."""
    user_id = update.effective_user.id
    short_name = context.user_data.get("current_comm")
    comm = get_committee(short_name) if short_name else None

    question_text = update.message.text.strip()
    if not question_text:
        await update.message.reply_text(
            "Please send a non-empty message, or /cancel to go back."
        )
        return AWAITING_QUESTION

    # Generate a unique ID for this question so admins can reply to it
    question_id = str(uuid.uuid4())[:8].upper()
    pending_questions[question_id] = user_id

    comm_name = comm["name"] if comm else "Unknown Committee"

    # Forward to admin chat
    admin_message = (
        f"📬 <b>New Anonymous Question</b>\n\n"
        f"Committee: <b>{html.escape(comm_name)}</b>\n"
        f"Question ID: <code>{html.escape(question_id)}</code>\n\n"
        f"<i>{html.escape(question_text)}</i>\n\n"
        f"To reply, use:\n<code>/reply {html.escape(question_id)} &lt;your reply&gt;</code>"
    )
    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            parse_mode=ParseMode.HTML,
        )
    except Exception as exc:
        logger.error("Failed to forward question to admin chat: %s", exc)
        await update.message.reply_text(
            "⚠️ There was a problem forwarding your question. Please try again later."
        )
        return AWAITING_QUESTION

    await update.message.reply_text(
        f"✅ Your question has been sent anonymously to <b>{html.escape(comm_name)}</b>!\n\n"
        f"Reference ID: <code>{html.escape(question_id)}</code>\n\n"
        "You will receive a reply here when the directors respond.\n\n"
        "Use /start to return to the main menu.",
        parse_mode=ParseMode.HTML,
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the current conversation and return to main menu."""
    await update.message.reply_text(
        "Cancelled. Use /start to return to the main menu."
    )
    return ConversationHandler.END


# --- Admin: reply to anonymous question ---

async def reply_to_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Admin command: /reply <question_id> <reply text>
    Looks up the original user and forwards the reply to them.
    """
    args = context.args
    if not args or len(args) < 2:
        await update.message.reply_text(
            "Usage: <code>/reply &lt;QUESTION_ID&gt; &lt;reply text&gt;</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    question_id = args[0].upper()
    reply_text = " ".join(args[1:])

    user_id = pending_questions.get(question_id)
    if user_id is None:
        await update.message.reply_text(
            f"⚠️ Question ID <code>{html.escape(question_id)}</code> not found or already answered.",
            parse_mode=ParseMode.HTML,
        )
        return

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"💬 <b>Reply to your anonymous question</b> (ID: <code>{html.escape(question_id)}</code>)\n\n"
                f"{html.escape(reply_text)}"
            ),
            parse_mode=ParseMode.HTML,
        )
        # Remove from pending after successful reply
        del pending_questions[question_id]
        await update.message.reply_text(
            f"✅ Reply sent successfully for question <code>{html.escape(question_id)}</code>.",
            parse_mode=ParseMode.HTML,
        )
    except Exception as exc:
        logger.error("Failed to send reply to user %s: %s", user_id, exc)
        await update.message.reply_text(
            "⚠️ Failed to deliver the reply. The user may have blocked the bot."
        )


# --- AI chatbot ---

async def ai_chat_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    /ask <question> — Answer the question using the AI assistant.
    Falls back to a helpful message if OpenAI is not configured.
    """
    if not context.args:
        await update.message.reply_text(
            "Usage: <code>/ask &lt;your question&gt;</code>\n\nExample: <code>/ask What does SportsCom do?</code>",
            parse_mode=ParseMode.HTML,
        )
        return

    question = " ".join(context.args)
    await _handle_ai_question(update, question)


async def _handle_ai_question(update: Update, question: str) -> None:
    """Send an AI-generated answer for the given question."""
    if not OPENAI_API_KEY:
        await update.message.reply_text(
            "🤖 The AI assistant is not configured yet.\n\n"
            "Please use /start to browse committees and FAQs, or use "
            "<b>Ask a Question</b> inside a committee to reach the directors directly.",
            parse_mode=ParseMode.HTML,
        )
        return

    try:
        import openai  # pylint: disable=import-outside-toplevel

        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        # Build a context string from committee data for the AI
        context_lines = ["You are a helpful assistant for CAPT (College of Alice & Peter Tan) at NUS Singapore."]
        context_lines.append("Here is information about CAPT's committees:\n")
        for comm in COMMITTEES:
            context_lines.append(f"- {comm['name']}: {comm['overview']}")
        context_lines.append(
            "\nAnswer the user's question helpfully and concisely. "
            "If you don't know the answer, suggest they use the bot's "
            "'Ask a Question' feature to contact the committee directly."
        )
        system_prompt = "\n".join(context_lines)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            max_tokens=500,
        )
        answer = response.choices[0].message.content.strip()
        await update.message.reply_text(
            f"🤖 <b>AI Assistant</b>\n\n{html.escape(answer)}", parse_mode=ParseMode.HTML
        )
    except Exception as exc:
        logger.error("OpenAI API error: %s", exc)
        await update.message.reply_text(
            "⚠️ The AI assistant encountered an error. Please try again later."
        )


# ---------------------------------------------------------------------------
# Application setup
# ---------------------------------------------------------------------------


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Conversation handler for the main browse flow
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_COMM: [
                CallbackQueryHandler(show_committee, pattern=r"^comm\|"),
                CallbackQueryHandler(show_ace_subcommittee, pattern=r"^acesub\|"),
            ],
            VIEW_COMM: [
                CallbackQueryHandler(show_faqs, pattern=r"^faqs\|"),
                CallbackQueryHandler(ask_question_prompt, pattern=r"^ask\|"),
                CallbackQueryHandler(show_ace_subcommittee, pattern=r"^acesub\|"),
                CallbackQueryHandler(back_to_ace, pattern=r"^back\|ace$"),
                CallbackQueryHandler(back_to_main, pattern=r"^back\|main$"),
                CallbackQueryHandler(show_committee, pattern=r"^comm\|"),
            ],
            VIEW_FAQS: [
                CallbackQueryHandler(show_faq_answer, pattern=r"^faq\|"),
                CallbackQueryHandler(ask_question_prompt, pattern=r"^ask\|"),
                CallbackQueryHandler(show_ace_subcommittee, pattern=r"^acesub\|"),
                CallbackQueryHandler(back_to_ace, pattern=r"^back\|ace$"),
                CallbackQueryHandler(show_committee, pattern=r"^comm\|"),
                CallbackQueryHandler(back_to_main, pattern=r"^back\|main$"),
            ],
            VIEW_FAQ_ANSWER: [
                CallbackQueryHandler(show_faqs, pattern=r"^faqs\|"),
                CallbackQueryHandler(back_to_ace, pattern=r"^back\|ace$"),
                CallbackQueryHandler(back_to_main, pattern=r"^back\|main$"),
            ],
            AWAITING_QUESTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_question),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reply", reply_to_question))
    application.add_handler(CommandHandler("ask", ai_chat_command))

    logger.info("CAPT-pedia bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
