class ContextManager:
    def __init__(self):
        self.history = []

    def add_message(self, user_msg, bot_msg):
        self.history.append({"user": user_msg, "bot": bot_msg})
        if len(self.history) > 5:  # keep last 5
            self.history.pop(0)

    def get_context(self):
        context = ""
        for turn in self.history:
            context += f"User: {turn['user']}\nBot: {turn['bot']}\n"
        return context
