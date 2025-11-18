class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, token):
        return self.values.get(token.lexeme)

    def assign(self, token, value):
        self.values[token.lexeme] = value
