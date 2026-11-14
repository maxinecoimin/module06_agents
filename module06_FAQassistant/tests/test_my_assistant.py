# tests/test_my_assistant.py
# Author: Maxine Coimin

from change_queue import ChangeQueue
from fake_model import FakeModel
from my_assistant import InvoiceAssistant
from my_tool import InvoiceLookup
from my_toolbox import Toolbox


def make_bot(model):
    invoices = {
        "INV-1001": {
            "status": "paid",
            "billing_address": "123 Business St, BeeTown, USA",
        },
        "INV-1002": {
            "status": "unpaid",
            "billing_address": "456 Corporate Ave, CeeTown, USA",
        },
        "INV-1003": {
            "status": "paid",
            "billing_address": "789 Industrial Blvd, EyeTown, USA",
        },
        "INV-1004": {
            "status": "in progress",
            "billing_address": "321 Commercial Rd, ComTown, USA",
        },
    }
    invoice_tool = InvoiceLookup(invoices)
    tools = Toolbox(invoice_tool, ChangeQueue(invoice_tool))
    return InvoiceAssistant("Ayo", "Be helpful", tools, model)


def ask_for_tool(name, arguments):
    """Build the decision a model returns when it wants a tool."""
    return {"tool": name, "arguments": arguments}


def test_made_up_address_is_refused():
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change",
                {"invoice_id": "INV-1001", "new_address": "123 Main St, AnyTown, USA"},
            ),
            {"text": "What is the new address?"},
        ]
    )
    bot = make_bot(model)
    bot.respond("Please change the address on invoice INV-1001")
    assert "has not given that address" in bot.history[1]["content"]
    assert bot.tools.change_queue.waiting() == []


def test_address_change_waits_for_staff():
    model = FakeModel(
        [
            ask_for_tool(
                "request_address_change",
                {
                    "invoice_id": "INV-1001",
                    "new_address": "9 Pine Street, SomeTown, USA",
                },
            ),
            {"text": "Sent to staff."},
        ]
    )
    bot = make_bot(model)
    bot.respond(
        "Change the address on invoice INV-1001 to 9 Pine Street, SomeTown, USA"
    )
    assert len(bot.tools.change_queue.waiting()) == 1
    assert (
        bot.tools.invoice_tool.invoices["INV-1001"]["billing_address"]
        == "123 Business St, BeeTown, USA"
    )


def test_payment_question_never_reaches_the_model():
    bot = make_bot(FakeModel([]))
    assert "human" in bot.respond("Can I pay with a different card?")
