from lexer.Lexer import Lexer
from parser.Parser import Parser
from interpreter.Interpreter import Interpreter

sample = '''
inicio
    a = 5;
    b = a + 3 * (2 + 1);
    imprimir(a);
    imprimir(b);
    si b > 10 entonces
        imprimir(b);
    fin_si
    b = b - 1;
    imprimir(b)
fin
'''

def run_source(src):
    lexer = Lexer(src)
    tokens = lexer.scan_tokens()
    # print('TOKENS:', tokens)
    parser = Parser(tokens)
    program = parser.parse()  # list of statements
    interpreter = Interpreter()
    interpreter.interpret(program)

if __name__ == '__main__':
    run_source(sample)
