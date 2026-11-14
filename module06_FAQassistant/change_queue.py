# change_queue.py
# Author: Maxine Coimin


class ChangeQueue:
    """Changes waiting for a person to approve. Nothing changes until they do."""

    def __init__(self, invoice_tool):
        """Start with no requests. Approved changes go through the invoice tool."""
        self.invoice_tool = invoice_tool
        self.requests = []

    def request_address_change(self, invoice_id, new_address):
        """Ask staff to change the billing address on one invoice. Staff must approve it.

        Args:
            invoice_id: The invoice ID, like INV-100.
            new_address: The full new billing address.
        """
        invoice_id = invoice_id.upper()
        if self.invoice_tool.find_status(invoice_id) is None:
            return "No invoice with that ID was found. Invoice IDs look like INV-100."
        number = len(self.requests) + 1
        request = {
            "number": number,
            "invoice_id": invoice_id,
            "new_address": new_address,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to staff. The address has not changed yet."

    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Return the request with this number, or None."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve one waiting request and make the change."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.invoice_tool.change_address(request["invoice_id"], request["new_address"])
        return f"Request {number} approved."

    def reject(self, number):
        """Reject one waiting request. Nothing changes."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
