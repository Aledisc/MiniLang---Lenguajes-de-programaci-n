from parser.AST import *
from lexer.TokenType import TokenType

class Interpreter:
    def __init__(self):
        self.env = __import__('interpreter.Environment', fromlist=['Environment']).Environment()

    def interpret(self, statements):
        for s in statements:
            self.execute(s)

    def execute(self, stmt):
        if isinstance(stmt, list):
            for st in stmt:
                self.execute(st)
            return
        if isinstance(stmt, Print):
            v = self.evaluate(stmt.expr)
            print(v)
            return
        if isinstance(stmt, VarDecl):
            name = stmt.name
            value = None
            if stmt.initializer is not None:
                value = self.evaluate(stmt.initializer)
            self.env.define(name.lexeme, value)
            return
        if isinstance(stmt, IfStmt):
            cond = self.evaluate(stmt.condition)
            if cond:
                for inner in stmt.then_branch:
                    self.execute(inner)
            return
        # expression-stmt fallback: evaluate expression (useful for side effects)
        self.evaluate(stmt)

    def evaluate(self, expr):
        if isinstance(expr, Literal):
            return expr.value
        if isinstance(expr, Variable):
            val = self.env.get(expr.name)
            return val
        if isinstance(expr, Assign):
            value = self.evaluate(expr.value)
            self.env.assign(expr.name, value)
            return value
        if isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            op = expr.operator.type
            # arithmetic
            if op == TokenType.PLUS: return left + right
            if op == TokenType.MINUS: return left - right
            if op == TokenType.STAR: return left * right
            if op == TokenType.SLASH: return left / right
            # comparisons (return booleans)
            if op == TokenType.GT: return left > right
            if op == TokenType.LT: return left < right
            if op == TokenType.GE: return left >= right
            if op == TokenType.LE: return left <= right
            if op == TokenType.EQ: return left == right
            if op == TokenType.NEQ: return left != right
        raise Exception('Expresión no evaluable') 
