# MiniLang (Proyecto básico)
Proyecto mínimo de un mini lenguaje en Python.

**Características**
- Palabras reservadas (español): inicio, fin, si, entonces, fin_si, imprimir
- Asignaciones: `x = 5;`
- Expresiones aritméticas: `+ - * /` y paréntesis
- Impresión: `imprimir(x);`
- Condicional simple: `si x > 3 entonces ... fin_si`

**Estructura de carpetas**
- lexer/: Token, TokenType, Lexer
- parser/: AST, Parser
- interpreter/: Environment, Interpreter
- errors/: Error
- main.py: ejemplo de uso

Lee `main.py` para ver un ejemplo de programa MiniLang y cómo ejecutarlo.
