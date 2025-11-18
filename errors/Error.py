class LangError(Exception):
    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line
