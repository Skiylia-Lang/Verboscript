# this will house the compiler, that will take source code and spit out bytecode

# fetch any inbuilt python functions

# fetch our code
from lexer import initLexer

# Global variables

# advance through the token stream
def advance():
    # update the parser start location
    parser.previous = parser.current
    

# compile source code to bytecode
def compile(source, chunk):
    #initialise our lexer
    initLexer(source)
    # consume the first character to prime the compiler
    advance()
    # parse a single expression
    expression()
    # and consume the EOF token
    consume("TOKEN_EOF", "Expected end of expression.")
