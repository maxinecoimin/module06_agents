# main.py
# Author: Maxine Coimin

from chatbot import SupportChatbot
from ollama_model import OllamaModel
from order_tool import OrderLookup
from stock_tool import StockLookup

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Sunny, a support assistant for Bayside Outfitters.
Answer all questions in one short sentence.
The store hours are 10 am to 7 pm every day for all locations.
Shipping takes 3 to 5 business days no matter where the order is shipped from.
Sale items cannot be returned.
Returns are accepted within 30 days with a receipt.
Only state facts that appear in these instructions.
If you do not know, say you do not know and offer to pass the customer to a human agent."""

ORDERS = {
    "A100": "shipped",
    "A101": "processing",
    "A102": "delivered",
}

STOCK = {
    "skirt": 10,
    "crop top": 5,
    "shorts": 0,
}

order_tool = OrderLookup(ORDERS)
stock_tool = StockLookup(STOCK)
model = OllamaModel(MODEL_NAME)
bot = SupportChatbot(
    "Sunny", "I can help you with your orders.", order_tool, stock_tool, model
)

print("Welcome to the support chatbot. Type 'quit' to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Message history: {len(bot.history)}")
