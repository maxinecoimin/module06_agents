# main.py
# Author: Maxine Coimin

from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup

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
bot = SupportChatbot("Sunny", "I can help you with your orders.", order_tool, stock_tool)

print("Welcome to the support chatbot. Type 'quit' to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{bot.name}: {bot.respond(user_message)}")
    user_message = input("You: ")

print(f"Message history: {len(bot.history)}")

