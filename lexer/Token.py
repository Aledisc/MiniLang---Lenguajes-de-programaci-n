class Token:
    def __init__(self, type_, lexeme, literal=None, line=1):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.lexeme!r}, {self.literal})"
