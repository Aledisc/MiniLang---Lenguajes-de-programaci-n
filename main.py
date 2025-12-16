from lexer.Lexer import Lexer
from parser.Parser import Parser
from interpreter.Interpreter import Interpreter

sample = '''
inicio
    imprimir("====================================");
    imprimir("        DEMOSTRACION MINILANG        ");
    imprimir("====================================");
    imprimir("");
    imprimir("prueba de variables y expresiones");
    imprimir("");
    
    a = 5;
    b = a + 3 * (2 + 1);
    imprimir("Resultado a:");
    imprimir(a);
    imprimir("Resultado b:");
    imprimir(b);
    
    imprimir("");
    imprimir(">>Manejo de condicionales");
    
    si b > 10 entonces
        imprimir("b es mayor que 10");
    fin_si
    
    imprimir("");
    imprimir(">>Prueba de self-assignment with update");
    imprimir("Imprimiendo b");
    imprimir(b);
    imprimir("");
    b = b - 1;
    imprimir("Resultado de b - 1:");
    imprimir(b);
    
    imprimir("");
    imprimir(">>Prueba de strings y concatenacion");
    c = "ya manejo variables tipo string";
    imprimir(c);
    imprimir("y puedo imprimir tanto strings simples");
    imprimir("asi como" + " concatenacion de strings");

    imprimir("");
    imprimir(">>Prueba de manejo de funciones");
    imprimir("Definimos suma(x,y), luego hacemos suma(1,2)"); 
    func suma(x, y) {
        return x + y;
    }
    resultado = suma(1,2);
    imprimir(resultado);
fin
'''



def run_source(src):
    lexer = Lexer(src)
    tokens = lexer.scan_tokens()
    # print('TOKENS:', tokens)
    parser = Parser(tokens)
    program = parser.parse()  # que hubo parse
    interpreter = Interpreter()
    interpreter.interpret(program)

if __name__ == '__main__':
    run_source(sample)
