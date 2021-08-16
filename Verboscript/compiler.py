# this will house the compiler, that will take source code and spit out bytecode

# fetch any inbuilt python functions

# fetch our code
from common import printn
from chunk import *
from lexer import initLexer, scanToken

# Global variables
class Parser:
    # store the current token
    current = ""
    # and the previous
    previous = ""
    # an error flag
    hadError = False
    # and the panic flag
    panicMode = False

# Create the parser
parser = Parser()

# and the compiling chunk
globals()["compilingChunk"] = ""

# show an error message
def errorAt(token, message):
    # if we already had an error, don't report this one too (as it may be due to the first error, rather than an actual problem)
    if parser.panicMode:
        return
    # tell the parser to panic
    parser.panicMode = True
    # show the token location
    printn("[line {}, char {}] Error".format(token.line, token.char))
    # if we had an EOF token,
    if token.type == "TOKEN_EOF":
        # add the "at end to the end of the error message"
        printn("at end")
    elif token.type == "TOKEN_ERROR":
        # do nothing
        a=0
    else:
        # show the token literal
        printn("at '{}',".format(token.literal))
    # and print the message
    print(message)
    # and update the error flag of the parser
    parser.hadError = True

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

# consume the next token
def consume(type, message):
    # check if we have the correct token
    if parser.current.type == type:
        # then advance
        advance()
        # and exit this function
        return
    # otherwise, throw an error
    errorAtCurrent(message)

# emit a byte into the current chunk
def emitByte(byte):
    # write the byte to the compiling chunk
    writeChunk(compilingChunk, byte, parser.previous.line, parser.previous.char)

# emit multiple bytes
def emitBytes(*bytes):
    # iterate through the supplied bytes
    for byte in bytes:
        # and emit each one
        emitByte(byte)

# emit a return byte
def emitReturn():
    emitByte("OP_RETURN")

# handle the safe shutdown of the compiler
def endCompiler():
    emitReturn()

# compile source code to bytecode
def compile(source, chunk):
    # initialise our lexer
    initLexer(source)
    # and update the current chunk we are compiling
    compilingChunk = chunk
    # clear all parser errors
    parser.panicMode = False
    parser.hadError = False
    # consume the first character to prime the compiler
    advance()
    # parse a single expression
    expression()
    # and consume the EOF token
    consume("TOKEN_EOF", "Expected end of expression.")
    # end the compilers process
    endCompiler()
    # and return if the parser had an error
    return not parser.hadError
