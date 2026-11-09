# mock_model.py
# Author: Maxine Coimin


class MockModel:
    """A support chatbot. Rules handle what must be right. A model handles the rest."""

    def reply(self, instructions, history):
        """Return a fixed reply based on the last message in the history."""
        last_message = history[-1]["content"].lower()
        if "hello" in last_message:
            return "Hello! How can I help you today?"
        return "I'm not sure how to help with that. I can check an order or stock."
