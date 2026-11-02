# my_main.py
# Author: Maxine Coimin

from my_assistant import InvoiceAssistant
from my_tool import InvoiceLookup

INVOICES = {
    "INV-1001": "paid",
    "INV-1002": "unpaid",
    "INV-1003": "paid",
    "INV-1004": "in progress",
}

invoice_tool = InvoiceLookup(INVOICES)
bot = InvoiceAssistant(
    "Ayo",
    "You are a friendly FAQ assistant for retrospective invoices.",
    invoice_tool,
)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")
