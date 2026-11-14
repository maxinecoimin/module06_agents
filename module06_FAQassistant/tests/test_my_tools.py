# test_my_tools.py
# Author: Maxine Coimin

from change_queue import ChangeQueue
from my_tool import InvoiceLookup
from my_toolbox import Toolbox


def make_tools():
    """Build fresh tools with two invoices for each test."""
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
    return Toolbox(invoice_tool, ChangeQueue(invoice_tool))


def customer(text):
    """Build a history that holds one customer message."""
    return [{"role": "user", "content": text}]


def test_look_up_known_invoice():
    tools = make_tools()
    assert tools.invoice_tool.look_up_invoice("INV-1001") == "Invoice INV-1001 is paid."


def test_request_waits_and_changes_nothing():
    tools = make_tools()
    tools.change_queue.request_address_change(
        "INV-1001", "9 Pine Street, SomeTown, USA"
    )
    assert tools.change_queue.waiting()[0]["status"] == "waiting"
    assert (
        tools.invoice_tool.invoices["INV-1001"]["billing_address"]
        == "123 Business St, BeeTown, USA"
    )


def test_approve_makes_the_change_once():
    tools = make_tools()
    tools.change_queue.request_address_change(
        "INV-1001", "9 Pine Street, SomeTown, USA"
    )
    assert tools.change_queue.approve(1) == "Request 1 approved."
    assert (
        tools.invoice_tool.invoices["INV-1001"]["billing_address"]
        == "9 Pine Street, SomeTown, USA"
    )
    assert tools.change_queue.approve(1) == "Request 1 is already approved."


def test_order_id_must_come_from_the_customer():
    tools = make_tools()
    reply = tools.run(
        "look_up_invoice", {"invoice_id": "INV-1001"}, customer("Where is my invoice?")
    )
    assert "has not given that invoice ID" in reply
