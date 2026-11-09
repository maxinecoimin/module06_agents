# echo_model.py - Exercise 2
# Author: Maxine Coimin


class EchoModel:
    """A model that repeats the last message. It needs no AI and no internet."""

    def reply(self, instructions, history):
        """Return the last message with a few words in front of it."""
        last_message = history[-1]["content"]
        return f"You said: {last_message}"
