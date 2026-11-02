# my_tool.py
# Author: Maxine Coimin


class InvoiceLookup:
    """A tool that knows about invoices. It knows nothing about chatting."""

    def __init__(self, invoices):
        """Store the invoices this tool can look up."""
        self.invoices = invoices

    def find_invoice_id(self, text):
        """Return the first known invoice ID mentioned in text, or None."""
        for invoice_id in self.invoices:
            if invoice_id in text.upper():
                return invoice_id
        return None

    def find_status(self, invoice_id):
        """Return the status of one invoice, or None if there is no such invoice."""
        if invoice_id in self.invoices:
            return self.invoices[invoice_id]
        return None
