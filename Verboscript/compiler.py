# this will house the compiler, that will take source code and spit out bytecode

# fetch any inbuilt python functions

# fetch our code
from common import printn
from chunk import *
from lexer import initLexer, scanToken

# Global variables

# the precedence table
Precedence = ["PREC_NONE",
              "PREC_ASSIGNMENT", # =
              "PREC_TERM", # + -
              "PREC_FACTOR", # * /
              "PREC_UNARY", # -
              "PREC_PRIMARY",]

Rules = {# Token: [prefix, infix, precedence]
         "TOKEN_LEFT_PAREN":  [grouping, None,   "PREC_NONE"],
         "TOKEN_RIGHT_PAREN": [None,     None,   "PREC_NONE"],
         "TOKEN_COMMA":       [None,     None,   "PREC_NONE"],
         "TOKEN_DOT":         [None,     None,   "PREC_NONE"],
         # Operations
         "TOKEN_MINUS":       [unary,    binary, "PREC_TERM"],
         "TOKEN_PLUS":        [None,     binary, "PREC_TERM"],
         "TOKEN_SLASH":       [None,     binary, "PREC_Factor"],
         "TOKEN_STAR":        [None,     binary, "PREC_Factor"],
         # Literals
         "TOKEN_STRING":      [None,     None,   "PREC_NONE"],
         "TOKEN_NUMBER":      [number,   None,   "PREC_NONE"],
         # Keywords
         "TOKEN_SHOW":        [None,     None,   "PREC_NONE"],
         # Miscellaneous
         "TOKEN_ERROR":       [None,     None,   "PREC_NONE"],
         "TOKEN_EOF":         [None,     None,   "PREC_NONE"],
         "TOKEN_INDENT":      [None,     None,   "PREC_NONE"],
         "TOKEN_NEWLINE":     [None,     None,   "PREC_NONE"],
         }

# A parsing rule struct
class ParseRule:
    # the thing before
    prefix = ""
    # the thing after
    infix = ""
    # the precedence
    precedence = ""

# The parser struct
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
compilingChunk

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

# create a constant value
def makeConstant(value):
    # add the constant to the chunk array
    const = addConstant(compilingChunk, value)
    # and return the value
    return const

# add a constant to the chunk
def emitConstant(value):
    # emit the bytes needed
    emitBytes("OP_CONSTANT", makeConstant(value))

# handle the safe shutdown of the compiler
def endCompiler():
    emitReturn()

# handle parentheses for groupings
def grouping():
    # fetch the internal expression
    expression()
    # and consume the closing bracket
    consume("TOKEN_RIGHT_PAREN", "Expected ')' after expression.")

# deal with numeric tokens
def number():
    # fetch the value
    value = float(parser.previous.start)
    # and emit the number into the chunk
    emitConstant(value)

# unary operations
def unary():
    # fetch the operation
    optype = parser.previous.type
    # compile the operand as a unary
    parsePrecedence("PREC_UNARY")
    # and emit the operator
    if optype = "TOKEN_MINUS":
        emitByte("OP_NEGATE")
    # otherwise, nothing
    return

# binary operations
def binary():
    # fetch the operation type
    optype = parser.previous.type
    # and the rul for the operation
    rule = getRule(optype)
    # sort out the precedence (binary expressions are left associative, so we ensure the precedence is one higher)
    parsePrecedence(Precedence[rule + 1])
    # and emit the operator
    if optype = "TOKEN_PLUS":
        emitByte("OP_ADD")
    elif optype = "TOKEN_MINUS":
        emitByte("OP_SUBTRACT")
    elif optype = "TOKEN_STAR":
        emitByte("OP_MULTIPLY")
    elif optype = "TOKEN_SLASH":
        emitByte("OP_DIVIDE")
    # otherwise, nothing
    return


# deal with operations that have different precedence
def parsePrecedence(precedence):
    # fetch the next token
    advance()
    # fetch the prefix rule
    prefRule = getRule(parser.previous.type)[0]
    # if we didn't have one
    if prefRule == None:
        error("Expect expression")
        return
    # Otherwise, execute the prefix rule
    prefRule()
    # ensure we have a lower precedence
    while (precedence <= getRule(parser.current.type)[2]):
        # fetch the next token
        advance()
        # fetch the infix rule
        infRule = getRule(parser.previous.type)[1]
        # and execute it
        infRule()

# fetch the precedence rule
def ParseRule(tokenType):
    # return the rule given the token
    return Rules[tokenType]

# interpret a single expression
def expression():
    parsePrecedence("PREC_ASSIGNMENT")

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
