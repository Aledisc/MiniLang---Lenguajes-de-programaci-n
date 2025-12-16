from lexer.TokenType import TokenType
from parser.AST import *
from errors.Error import LangError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type_):
        if self.is_at_end(): return False
        return self.peek().type == type_

    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, type_, msg):
        if self.check(type_):
            return self.advance()
        raise LangError(msg)

    def parse(self):
        # Expect program between INICIO ... FIN
        stmts = []
        if not self.match(TokenType.INICIO):
            raise LangError('Se esperaba palabra reservada "inicio" al inicio del programa.')
        while not self.check(TokenType.FIN) and not self.is_at_end():
            stmts.append(self.declaration())
        self.consume(TokenType.FIN, 'Se esperaba "fin" al final del programa.')
        return stmts

    def declaration(self):
        if self.match(TokenType.FUNC):
            return self.function_decl()
        return self.statement()

    def statement(self):
        if self.match(TokenType.FUNC):
            return self.function_decl()
        if self.match(TokenType.IMPRIMIR):
            return self.print_stmt()
        if self.match(TokenType.SI):
            return self.if_stmt()
        if self.match(TokenType.RETURN):
            value = None
            if not self.check(TokenType.SEMICOLON):
                value = self.expression()
            self.consume(TokenType.SEMICOLON, "Falta ';'")
            return ReturnStmt(value)

        return self.expr_stmt()

    def print_stmt(self):
        # allow imprimir(expr);  or imprimir identificador ;
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Se esperaba ')'")
        else:
            expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Se esperaba ';' en impresión")
        return Print(expr)

    def if_stmt(self):
        condition = self.expression()
        self.consume(TokenType.ENTONCES, "Se esperaba 'entonces' en condicional")
        then_branch = []
        while not self.check(TokenType.FIN_SI) and not self.is_at_end():
            then_branch.append(self.declaration())
        self.consume(TokenType.FIN_SI, "Se esperaba 'fin_si'")
        return IfStmt(condition, then_branch)

    def expr_stmt(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Falta ';' al final de la expresión")
        # assignment detection: if expression is Variable and next was ASSIGN, handled in expression
        if isinstance(expr, Assign):
            return VarDecl(expr.name, expr.value)
        return expr

    # EXPRESSION PARSING (recursive descent): supports comparisons and arithmetic
    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQ, TokenType.NEQ):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GT, TokenType.GE, TokenType.LT, TokenType.LE):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            # represent unary as Binary with left=0 for simplicity
            return Binary(Literal(0), operator, right)
        return self.primary()

    def primary(self):
        # Guardamos el token del identificador si apareciera
        if self.match(TokenType.NUMBER):
            return Literal(self.previous().literal)

        if self.match(TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.IDENTIFIER):
            name = self.previous()

            if self.match(TokenType.LPAREN):
                args = []
                if not self.check(TokenType.RPAREN):
                    args.append(self.expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.expression())
                self.consume(TokenType.RPAREN, "Se esperaba ')'")
                return FunctionCall(name, args)

            if self.match(TokenType.ASSIGN):
                value = self.expression()
                return Assign(name, value)

            return Variable(name)

        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Se esperaba ')'")
            return expr

        raise LangError('Se esperaba una expresión válida.')

    def function_decl(self):
        name = self.consume(TokenType.IDENTIFIER, "Se esperaba nombre de función.")

        self.consume(TokenType.LPAREN, "Se esperaba '('")
        params = []

        if not self.check(TokenType.RPAREN):
            params.append(self.consume(TokenType.IDENTIFIER, "Parámetro esperado"))
            while self.match(TokenType.COMMA):
                params.append(self.consume(TokenType.IDENTIFIER, "Parámetro esperado"))

        self.consume(TokenType.RPAREN, "Se esperaba ')'")
        self.consume(TokenType.LLAVE_IZQ, "Se esperaba '{'")

        body = []
        while not self.check(TokenType.LLAVE_DER):
            body.append(self.declaration())

        self.consume(TokenType.LLAVE_DER, "Se esperaba '}'")

        return FunctionDecl(name, params, body)

