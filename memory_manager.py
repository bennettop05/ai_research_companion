class ConversationMemory:
    def __init__(self):
        self.history = []

    def add(self, question, answer):
        self.history.append({"q": question, "a": answer})

    def get(self):
        context = ""
        for turn in self.history:
            context += f"User: {turn['q']}\nAI: {turn['a']}\n"
        return context

    def clear(self):
        self.history = []
