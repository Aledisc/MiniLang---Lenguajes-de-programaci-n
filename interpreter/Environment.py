class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent  # entorno padre (None si es global)

    def define(self, name, value):
        self.values[name] = value

    def get(self, token):
        name = token.lexeme
        if name in self.values:
            return self.values[name]
        if self.parent is not None:
            return self.parent.get(token)
        raise Exception(f"Variable '{name}' no definida.")

    def assign(self, token, value):
        name = token.lexeme
        if name in self.values:
            self.values[name] = value
            return
        if self.parent is not None:
            self.parent.assign(token, value)
            return
        raise Exception(f"Variable '{name}' no definida.")

    def create_child(self):
        return Environment(parent=self)
