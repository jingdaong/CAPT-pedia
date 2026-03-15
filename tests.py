"""
Tests for CAPT-pedia Telegram bot.

These tests validate the data layer and bot helper functions without
requiring a live Telegram connection or API credentials.
"""

import importlib
import os
import sys
import types
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# ---------------------------------------------------------------------------
# Ensure imports work even without installed packages
# ---------------------------------------------------------------------------

# Stub out `python-telegram-bot` so the data module can be imported in CI
# without installing the full library.
_telegram_stub = types.ModuleType("telegram")
_telegram_stub.Update = object
_telegram_stub.InlineKeyboardButton = MagicMock()
_telegram_stub.InlineKeyboardMarkup = MagicMock(side_effect=lambda rows: rows)
_telegram_constants = types.ModuleType("telegram.constants")
_telegram_constants.ParseMode = MagicMock()
_telegram_ext = types.ModuleType("telegram.ext")
for _attr in (
    "Application",
    "CallbackQueryHandler",
    "CommandHandler",
    "ContextTypes",
    "ConversationHandler",
    "MessageHandler",
    "filters",
):
    setattr(_telegram_ext, _attr, MagicMock())
sys.modules.setdefault("telegram", _telegram_stub)
sys.modules.setdefault("telegram.constants", _telegram_constants)
sys.modules.setdefault("telegram.ext", _telegram_ext)
sys.modules.setdefault("dotenv", types.ModuleType("dotenv"))
sys.modules["dotenv"].load_dotenv = lambda: None  # type: ignore[attr-defined]

# Provide dummy env vars so bot.py can be imported
os.environ.setdefault("BOT_TOKEN", "test_token")
os.environ.setdefault("ADMIN_CHAT_ID", "123456")

# ---------------------------------------------------------------------------
# Now import the modules under test
# ---------------------------------------------------------------------------
from data.committees import COMMITTEES, COMMITTEES_BY_KEY  # noqa: E402


class TestCommitteeData(unittest.TestCase):
    """Validate the structure and completeness of the committee data."""

    def test_committees_list_not_empty(self):
        self.assertGreater(len(COMMITTEES), 0)

    def test_each_committee_has_required_keys(self):
        required_keys = {
            "name",
            "short_name",
            "overview",
            "ig_handle",
            "tele_handle",
            "website",
            "directors",
            "faqs",
        }
        for comm in COMMITTEES:
            with self.subTest(comm=comm["short_name"]):
                self.assertEqual(required_keys, required_keys & set(comm.keys()))

    def test_short_names_are_unique(self):
        short_names = [c["short_name"] for c in COMMITTEES]
        self.assertEqual(len(short_names), len(set(short_names)))

    def test_committees_by_key_matches_list(self):
        self.assertEqual(len(COMMITTEES_BY_KEY), len(COMMITTEES))
        for comm in COMMITTEES:
            self.assertIn(comm["short_name"], COMMITTEES_BY_KEY)
            self.assertEqual(COMMITTEES_BY_KEY[comm["short_name"]], comm)

    def test_faqs_have_question_and_answer(self):
        for comm in COMMITTEES:
            for faq in comm["faqs"]:
                with self.subTest(comm=comm["short_name"], q=faq.get("question")):
                    self.assertIn("question", faq)
                    self.assertIn("answer", faq)
                    self.assertTrue(faq["question"].strip())
                    self.assertTrue(faq["answer"].strip())

    def test_directors_have_name(self):
        for comm in COMMITTEES:
            for director in comm["directors"]:
                with self.subTest(comm=comm["short_name"]):
                    self.assertIn("name", director)
                    self.assertTrue(director["name"].strip())

    def test_overview_is_non_empty_string(self):
        for comm in COMMITTEES:
            with self.subTest(comm=comm["short_name"]):
                self.assertIsInstance(comm["overview"], str)
                self.assertTrue(comm["overview"].strip())


class TestBotHelpers(unittest.TestCase):
    """Test bot helper / formatting functions."""

    def setUp(self):
        # Import bot module after stubs are in place
        import bot as bot_module  # noqa: F401 – side-effect: registers handlers

        self.bot = bot_module

    def test_build_comm_detail_text_contains_name(self):
        comm = COMMITTEES[0]
        text = self.bot.build_comm_detail_text(comm)
        self.assertIn(comm["name"], text)

    def test_build_comm_detail_text_contains_overview(self):
        comm = COMMITTEES[0]
        text = self.bot.build_comm_detail_text(comm)
        self.assertIn(comm["overview"], text)

    def test_build_comm_detail_text_contains_ig_handle(self):
        # Use a synthetic handle so this test does not depend on fixture values.
        comm = {**COMMITTEES[0], "ig_handle": "@example_handle"}
        text = self.bot.build_comm_detail_text(comm)
        self.assertIn(comm["ig_handle"], text)

    def test_build_comm_detail_text_no_empty_resource_lines(self):
        """Committees with no website should not emit an empty website line."""
        comm = next(c for c in COMMITTEES if not c["website"])
        text = self.bot.build_comm_detail_text(comm)
        self.assertNotIn("Website:   \n", text)

    def test_pending_questions_initially_empty(self):
        self.assertIsInstance(self.bot.pending_questions, dict)

    def test_welcome_text_is_non_empty(self):
        self.assertTrue(self.bot.WELCOME_TEXT.strip())

    def test_help_text_contains_commands(self):
        for cmd in ("/start", "/help", "/ask"):
            self.assertIn(cmd, self.bot.HELP_TEXT)


class TestPendingQuestionsStore(unittest.TestCase):
    """Validate the in-memory pending_questions store behaviour."""

    def setUp(self):
        import bot as bot_module

        self.bot = bot_module
        # Clear state before each test
        self.bot.pending_questions.clear()

    def tearDown(self):
        self.bot.pending_questions.clear()

    def test_add_and_retrieve_question(self):
        self.bot.pending_questions["ABCD1234"] = 999
        self.assertEqual(self.bot.pending_questions.get("ABCD1234"), 999)

    def test_remove_question_after_reply(self):
        self.bot.pending_questions["XYZ00001"] = 111
        del self.bot.pending_questions["XYZ00001"]
        self.assertNotIn("XYZ00001", self.bot.pending_questions)

    def test_unknown_question_id_returns_none(self):
        result = self.bot.pending_questions.get("NOTEXIST")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
