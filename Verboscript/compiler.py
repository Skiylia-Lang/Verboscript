# this will house the compiler, that will take source code and spit out bytecode

# fetch any inbuilt python functions

# fetch our code
from common import printn
from lexer import initLexer, scanToken

# Global variables
class Parser:
    # store the current token
    current = ""
    # and the previous
    previous = ""

parser = Parser()

# show an error message
def errorAt(token, message):
    printn("[line {}, char {}] Error".format(token.line, token.char))

# a general error handler for the previous token
def error(message):
    errorAt(parser.previous, message)

# error at the current locations
def errorAtCurrent(message):
    # show an error at the current token
    errorAt(parser.current, message)


# advance through the token stream
def advance():
    # update the parser start location
    parser.previous = parser.current
    # keep looping through the token stream
    while True:
        #fetch the next token
        parser.current = scanToken()
        # check we don't have an error
        if parser.current.type != "TOKEN_ERROR":
            break
        # otherwise, throw an error
        errorAtCurrent(parser.current.start)

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
