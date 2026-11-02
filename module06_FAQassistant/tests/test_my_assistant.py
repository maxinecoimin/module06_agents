# tests/test_my_assistant.py
# Author: Maxine Coimin

from my_assistant import InvoiceAssistant
from my_tool import InvoiceLookup


def make_bot():
    invoices = {"INV-1001": "paid", "INV-1002": "unpaid", "INV-1004": "in progress"}
    tool = InvoiceLookup(invoices)
    return InvoiceAssistant("TestBot", "Test instructions", tool)


def test_tool_lookup_found_and_missing():
    tool = InvoiceLookup({"INV-1001": "paid"})
    assert tool.find_invoice_id("What about INV-1001?") == "INV-1001"
    assert tool.find_status("INV-1001") == "paid"
    assert tool.find_status("INV-9999") is None


def test_status_lookup_uses_tool():
    bot = make_bot()
    reply = bot.respond("What is the status of INV-1002?")
    assert reply == "Invoice INV-1002 is unpaid."


def test_missing_invoice_gets_helpful_reply():
    bot = make_bot()
    reply = bot.respond("Check INV-9999 please")
    assert "couldn't find any record" in reply


def test_history_records_every_turn():
    bot = make_bot()
    bot.respond("hello")
    bot.respond("status of INV-1001")
    assert len(bot.history) == 4
    assert bot.history[0]["role"] == "user"
    assert bot.history[1]["role"] == "assistant"


def test_human_handoff_for_change_request():
    bot = make_bot()
    reply = bot.respond("Please refund INV-1002")
    assert "passing you to a billing specialist" in reply


def test_unknown_request_is_safe():
    bot = make_bot()
    reply = bot.respond("Do you validate parking?")
    assert "not sure how to help" in reply
