# my_assistant.py
# Author: Maxine Coimin

HANDOFF_WORDS = ["refund", "cancel", "change", "pay", "update"]


class InvoiceAssistant:
    """An invoice assistant. It does not use AI, just the rules"""

    def __init__(self, name, instructions, invoice_tool):
        """Set up one assistant with its own name, instructions, tool, and history."""
        self.name = name
        self.instructions = instructions
        self.invoice_tool = invoice_tool
        self.history = []

    def respond(self, user_message):
        """Record the user's message, choose a reply, record it, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Choose a reply with keyword rules. This is the mock part."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't change invoices or take payments here. I'm passing you to a billing specialist."
        if "invoice" in text or "status" in text or "INV-" in text.upper():
            return self.invoice_reply(user_message)
        if "hello" in text or "hi" in text:
            return f"Hello! I'm {self.name}. I can check an invoice status for you."
        return "I'm not sure how to help with that. I can check the retrspoctive invoice status."

    def needs_human(self, text):
        """Return True if the message is about something a person must handle."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def invoice_reply(self, user_message):
        """Use the invoice tool to advise status of invoice."""
        invoice_id = self.invoice_tool.find_invoice_id(user_message)

        if invoice_id is None:
            if "INV-" in user_message.upper():
                for word in user_message.upper().split():
                    if "INV-" in word:
                        invoice_id = word.strip(".,;:!?()[]")
                        break
            else:
                return "Which invoice? Please send an invoice ID like INV-1001."

        status = self.invoice_tool.find_status(invoice_id)
        if status is None:
            return f"I couldn't find any record for {invoice_id}. Please double-check the ID."

        return f"Invoice {invoice_id} is {status}."
