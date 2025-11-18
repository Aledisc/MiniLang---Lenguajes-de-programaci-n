from enum import Enum

class TokenType(Enum):
    # Single-character tokens
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    SLASH = '/'
    ASSIGN = '='
    SEMICOLON = ';'
    LPAREN = '('
    RPAREN = ')'

    # One or two character
    GT = '>'
    LT = '<'
    EQ = '=='
    NEQ = '!='
    GE = '>='
    LE = '<='

    # Literals
    IDENTIFIER = 'IDENTIFIER'
    NUMBER = 'NUMBER'

    # Keywords (spanish)
    INICIO = 'INICIO'
    FIN = 'FIN'
    SI = 'SI'
    ENTONCES = 'ENTONCES'
    FIN_SI = 'FIN_SI'
    IMPRIMIR = 'IMPRIMIR'

    EOF = 'EOF'
