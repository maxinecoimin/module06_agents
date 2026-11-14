# my_main.py
# Author: Maxine Coimin

from change_queue import ChangeQueue
from faq_ollama_model import OllamaModel
from my_assistant import InvoiceAssistant
from my_tool import InvoiceLookup
from my_toolbox import Toolbox

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """ You are Ayo, a friendly FAQ assistant for retrospective invoices. 
You can look up the status of an invoice and request an address change. 
You cannot take payments or cancel invoices.
Only provide information that is explicitly stated in the invoice records. Do not make up any information.
If the customer asks about payments, refunds, or cancellations, you must hand them off to a human agent.
If you do not know the answer, say you are not sure and hand them off to a human agent. Do not make up an answer.
"""

INVOICES = {
    "INV-1001": {"status": "paid", "billing_address": "123 Business St, BeeTown, USA"},
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

invoice_tool = InvoiceLookup(INVOICES)
change_queue = ChangeQueue(invoice_tool)
tools = Toolbox(invoice_tool, change_queue)
model = OllamaModel(MODEL_NAME)
bot = InvoiceAssistant("Ayo", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(bot.history)}")

print("Staff review")
for request in change_queue.waiting():
    number = request["number"]
    print(f"Request {number}: {request['invoice_id']} to {request['new_address']}")
    answer = input("Approve? yes or no: ")
    if answer == "yes":
        print(change_queue.approve(number))
    else:
        print(change_queue.reject(number))

for invoice_id in INVOICES:
    print(invoice_id, INVOICES[invoice_id]["billing_address"])
