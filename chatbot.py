# chatbot.py
# Author: Maxine Coimin

from mock_model import MockModel


class SupportChatbot:
    def __init__(self, name, instructions, order_tool, stock_tool, model=None):
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        self.stock_tool = stock_tool
        self.model = model if model is not None else MockModel()
        self.history = []

    def respond(self, message):
        return self.choose_reply(message)

    def needs_human(self, text):
        return "address" in text or "human" in text

    def order_reply(self, message):
        import re

        match = re.search(r"A\d+", message.upper())
        if match:
            order_id = match.group()
            status = self.order_tool.find_status(order_id)
            if status:
                return f"Order {order_id} is {status}."
            return "I couldn't find that order."
        return "Please provide your order ID."

    def stock_reply(self, message):
        text = message.lower()
        for item in ["skirt", "crop top", "shorts"]:
            if item in text:
                qty = (
                    self.stock_tool.find_stock(item)
                    if hasattr(self.stock_tool, "find_stock")
                    else None
                )
                if qty is None and hasattr(self.stock_tool, "stock"):
                    qty = self.stock_tool.stock.get(item)
                if qty is None:
                    # fallback to a dict lookup
                    qty = getattr(self.stock_tool, "data", {}).get(item)
                if qty is not None:
                    return f"There are {qty} {item}(s) in stock."
        return "I'm not sure about that item."

    def model_reply(self):
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "I'm not sure, sorry. Please try again in a moment."
        return reply

    def choose_reply(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        text = user_message.lower()
        if self.needs_human(text):
            reply = "I can't help with that here. I'm passing you to a human agent."
        elif "order" in text:
            reply = self.order_reply(user_message)
        elif "stock" in text or "in stock" in text:
            reply = self.stock_reply(user_message)
        else:
            reply = self.model_reply()
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def count_user_messages(self):
        return sum(1 for m in self.history if m["role"] == "user")
