class ConversationMemory:
    def __init__(self):
        self.memory = []

    def add(self, question, answer):
        self.memory.append({"q": question, "a": answer})
        if len(self.memory) > 3:
            self.memory.pop(0)

    def get(self):
        return "\n".join([f"Q: {m['q']}\nA: {m['a']}" for m in self.memory])
