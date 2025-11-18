# Expresiones (Expr) y declaraciones (Stmt)
class Expr: pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Literal(Expr):
    def __init__(self, value):
        self.value = value

class Variable(Expr):
    def __init__(self, name):
        self.name = name

class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

# Statements
class Stmt: pass

class Print(Stmt):
    def __init__(self, expr):
        self.expr = expr

class VarDecl(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

class IfStmt(Stmt):
    def __init__(self, condition, then_branch):
        self.condition = condition
        self.then_branch = then_branch
