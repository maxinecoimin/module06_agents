# my_toolbox.py
# Author: Maxine Coimin


class Toolbox:
    """Every tool request from the model comes through here and is checked."""

    def __init__(self, invoice_tool, change_queue):
        """Hold the tools the model is allowed to ask for."""
        self.invoice_tool = invoice_tool
        self.change_queue = change_queue

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.invoice_tool.look_up_invoice,
            self.change_queue.request_address_change,
        ]

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        if name == "look_up_invoice":
            invoice_id = self.clean(arguments, "invoice_id")
            if invoice_id == "":
                return "The invoice ID is missing. Ask the customer for it."
            if not self.customer_said(history, invoice_id):
                return "The customer has not given that invoice ID. Ask them for it."
            return self.invoice_tool.look_up_invoice(invoice_id)
        if name == "request_address_change":
            invoice_id = self.clean(arguments, "invoice_id")
            new_address = self.clean(arguments, "new_address")
            if invoice_id == "" or new_address == "":
                return "The invoice ID and the new address are both needed."
            if not self.customer_said(history, invoice_id):
                return "The customer has not given that invoice ID. Ask them for it."
            if not self.customer_said(history, new_address):
                return "The customer has not given that address. Ask them for it."
            return self.change_queue.request_address_change(invoice_id, new_address)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Return True if text appears in a message the customer typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
