from parser.AST import *
from lexer.TokenType import TokenType
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.env = __import__('interpreter.Environment', fromlist=['Environment']).Environment()
        self.functions = {}

    def interpret(self, statements):
        for s in statements:
            self.execute(s)

    def execute(self, stmt):
        if isinstance(stmt, FunctionDecl):
            self.functions[stmt.name.lexeme] = stmt
            return

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
        if isinstance(stmt, ReturnStmt):
            value = None
            if stmt.value:
                value = self.evaluate(stmt.value)
            raise ReturnException(value)

        self.evaluate(stmt)
        if isinstance(stmt, FunctionDecl):
            self.functions[stmt.name.lexeme] = stmt
            return

        if isinstance(expr, FunctionCall):
            return self.call_function(expr)

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

            # STRING + STRING → concatenación
            if op == TokenType.PLUS:
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                raise Exception("No se pueden sumar string y número. Usa solo strings o solo números.")

            # STRING no soporta -, *, /
            if op in (TokenType.MINUS, TokenType.STAR, TokenType.SLASH):
                if isinstance(left, str) or isinstance(right, str):
                    raise Exception("No se pueden aplicar operadores aritméticos a strings.")
                if op == TokenType.MINUS: return left - right
                if op == TokenType.STAR: return left * right
                if op == TokenType.SLASH: return left / right

            # Comparaciones
            if op in (TokenType.GT, TokenType.LT, TokenType.GE, TokenType.LE):
                if isinstance(left, str) or isinstance(right, str):
                    raise Exception("Comparación inválida entre strings y números.")
                if op == TokenType.GT: return left > right
                if op == TokenType.LT: return left < right
                if op == TokenType.GE: return left >= right
                if op == TokenType.LE: return left <= right

            if op == TokenType.EQ:
                return left == right
            if op == TokenType.NEQ:
                return left != right

        if isinstance(expr, FunctionCall):
            return self.call_function(expr)

    def call_function(self, call):
        fn = self.functions.get(call.name.lexeme)
        if not fn:
            raise Exception("Función no definida")

        if len(call.args) != len(fn.params):
            raise Exception("Cantidad incorrecta de argumentos")

        prev_env = self.env
        local_env = self.env.create_child()
        self.env = local_env

        for param, arg in zip(fn.params, call.args):
            local_env.define(param.lexeme, self.evaluate(arg))

        try:
            for stmt in fn.body:
                self.execute(stmt)
        except ReturnException as r:
            self.env = prev_env
            return r.value

        self.env = prev_env
        return None
