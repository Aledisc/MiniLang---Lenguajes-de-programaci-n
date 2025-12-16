import re
from .Token import Token
from .TokenType import TokenType
from errors.Error import LangError

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            'inicio': TokenType.INICIO,
            'fin': TokenType.FIN,
            'si': TokenType.SI,
            'entonces': TokenType.ENTONCES,
            'fin_si': TokenType.FIN_SI,
            'imprimir': TokenType.IMPRIMIR,
            "func": TokenType.FUNC,
            "return": TokenType.RETURN,

        }

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        ch = self.source[self.current]
        self.current += 1
        return ch

    def add_token(self, type_, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))

    def match(self, expected):
        if self.is_at_end(): return False
        if self.source[self.current] != expected: return False
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end(): return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == '"':
            self.string()
            return

        if c in ' \r\t':
            return
        if c == '\n':
            self.line += 1
            return
        if c.isdigit():
            self.number()
            return
        if c.isalpha() or c == '_':
            self.identifier()
            return
        if c == '+':
            self.add_token(TokenType.PLUS); return
        if c == '-':
            self.add_token(TokenType.MINUS); return
        if c == '*':
            self.add_token(TokenType.STAR); return
        if c == '/':
            self.add_token(TokenType.SLASH); return
        if c == ';':
            self.add_token(TokenType.SEMICOLON); return
        if c == '(':
            self.add_token(TokenType.LPAREN); return
        if c == ')':
            self.add_token(TokenType.RPAREN); return
        if c == '=':
            if self.match('='):
                self.add_token(TokenType.EQ); return
            else:
                self.add_token(TokenType.ASSIGN); return
        if c == '!':
            if self.match('='):
                self.add_token(TokenType.NEQ); return
            raise LangError(f"Unexpected character '!' at line {self.line}")
        if c == '>':
            if self.match('='):
                self.add_token(TokenType.GE); return
            self.add_token(TokenType.GT); return
        if c == '<':
            if self.match('='):
                self.add_token(TokenType.LE); return
            self.add_token(TokenType.LT); return
        if c == '{':
            self.add_token(TokenType.LLAVE_IZQ); return
        if c == '}':
            self.add_token(TokenType.LLAVE_DER); return
        if c == ',':
            self.add_token(TokenType.COMMA); return

        # Unknown char
        raise LangError(f"Unexpected character '{c}' at line {self.line}")

    def number(self):
        while self.peek().isdigit():
            self.advance()
        # no support for decimals yet
        value = int(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        ttype = self.keywords.get(text, TokenType.IDENTIFIER)
        self.tokens.append(Token(ttype, text, None, self.line))

    def string(self):
        value = ""
        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == '\n':
                self.line += 1
            value += self.advance()
        if self.is_at_end():
            raise LangError(f"String sin cerrar en la línea {self.line}")

        self.advance()  # cerrar comillas
        self.add_token(TokenType.STRING, value)

