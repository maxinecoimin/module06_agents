# my_tool.py
# Author: Maxine Coimin


class InvoiceLookup:
    """A tool that knows about invoices. It knows nothing about chatting."""

    def __init__(self, invoices):
        """Store the invoices this tool can look up."""
        self.invoices = invoices

    def find_invoice_id(self, text):
        """Return the first known invoice ID mentioned in text, or None."""
        text = text.upper()
        for invoice_id in self.invoices:
            if invoice_id in text:
                return invoice_id
        return None

    def find_status(self, invoice_id):
        """Return the status of one invoice, or None if there is no such invoice."""
        if invoice_id in self.invoices:
            return self.invoices[invoice_id]
        return None

    def look_up_invoice(self, invoice_id):
        """Look up the status of one invoice.

        Args:
            invoice_id: The invoice ID, like INV-1001.
        """
        invoice_id = invoice_id.strip().upper()
        if invoice_id not in self.invoices:
            return "No invoice with that ID was found. Invoice IDs look like INV-1001."
        return f"Invoice {invoice_id} is {self.invoices[invoice_id]['status']}."

    def request_address_change(self, invoice_id, new_address):
        """Request to change the billing address on one invoice. Only an approval calls this."""
        self.invoices[invoice_id]["billing_address"] = new_address

    def change_address(self, invoice_id, new_address):
        """Request to change the billing address on one invoice. Only an approval calls this."""
        self.invoices[invoice_id]["billing_address"] = new_address
