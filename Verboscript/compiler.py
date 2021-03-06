# this will house the compiler, that will take source code and spit out bytecode

# fetch any inbuilt python functions

# fetch our code
from common import printn
from chunk import *
from debug import *
from lexer import initLexer, scanToken

# Global variables

# the precedence table
Precedence = ["PREC_NONE",
              "PREC_ASSIGNMENT", # =
              "PREC_TERM", # + -
              "PREC_FACTOR", # * /
              "PREC_UNARY", # -
              "PREC_PRIMARY",]

# Parser rule struct
class parseRule:
    def __init__(self, prefix, infix, precedence):
        self.prefix = prefix
        self.infix = infix
        self.prec = precedence

# The parser struct
class Parser:
    def __init__(self):
        # store the current token
        self.current = ""
        # and the previous
        self.previous = ""
        # an error flag
        self.hadError = False
        # and the panic flag
        self.panicMode = False
        # and the currently compiling chunk
        self.compilingChunk = Chunk()

# restart the parser
def initParser(chunk):
    parser.__init__()
    parser.compilingChunk = chunk

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
    if token.typeName == "TOKEN_EOF":
        # add the "at end to the end of the error message"
        printn("at end")
    elif token.typeName == "TOKEN_ERROR":
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
        if parser.current.typeName != "TOKEN_ERROR":
            break
        # otherwise, throw an error
        errorAtCurrent(parser.current.start)

# consume the next token
def consume(typeName, message):
    # check if we have the correct token
    if parser.current.typeName == typeName:
        # then advance
        advance()
        # and exit this function
        return
    # otherwise, throw an error
    errorAtCurrent(message)

# emit a byte into the current chunk
def emitByte(byte):
    # write the byte to the compiling chunk
    writeChunk(parser.compilingChunk, byte, parser.previous.line, parser.previous.char)

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
    const = addConstant(parser.compilingChunk, value)
    # and return the value
    return const

# add a constant to the chunk
def emitConstant(value):
    # emit the bytes needed
    emitBytes("OP_CONSTANT", makeConstant(value))

# handle the safe shutdown of the compiler
def endCompiler():
    # emit a return byte
    emitReturn()
    # if the compiler is emiting code
    if DEBUG_PRINT_CODE:
        # if we didn't have an error
        if not parser.hadError:
            # then show the chunk
            disassembleChunk(parser.compilingChunk, "Code")

# handle parentheses for groupings
def grouping():
    # fetch the internal expression
    expression()
    # and consume the closing bracket
    consume("TOKEN_RIGHT_PAREN", "Expected ')' after expression.")

# deal with numeric tokens
def number():
    # fetch the value
    value = float(parser.previous.literal)
    # and emit the number into the chunk
    emitConstant(value)

# unary operations
def unary():
    # fetch the operation
    optype = parser.previous.typeName
    # compile the operand as a unary
    parsePrecedence("PREC_UNARY")
    # and emit the operator
    if optype == "TOKEN_MINUS":
        emitByte("OP_NEGATE")
    # otherwise, nothing
    return

# binary operations
def binary():
    # fetch the operation type
    optype = parser.previous.typeName
    # and the rul for the operation
    rule = getRule(optype).prec
    # sort out the precedence (binary expressions are left associative, so we ensure the precedence is one higher)
    parsePrecedence(Precedence[Precedence.index(rule) + 1])
    # and emit the operator
    if optype == "TOKEN_PLUS":
        emitByte("OP_ADD")
    elif optype == "TOKEN_MINUS":
        emitByte("OP_SUBTRACT")
    elif optype == "TOKEN_STAR":
        emitByte("OP_MULTIPLY")
    elif optype == "TOKEN_SLASH":
        emitByte("OP_DIVIDE")
    # otherwise, nothing
    return

# interpret a single expression
def expression():
    parsePrecedence("PREC_ASSIGNMENT")

# Precedence rules table
Rules = {# Token: [prefix, infix, precedence]
         "TOKEN_LEFT_PAREN":  parseRule(grouping, None,   "PREC_NONE"),
         "TOKEN_RIGHT_PAREN": parseRule(None,     None,   "PREC_NONE"),
         "TOKEN_COMMA":       parseRule(None,     None,   "PREC_NONE"),
         "TOKEN_DOT":         parseRule(None,     None,   "PREC_NONE"),
         # Operations
         "TOKEN_MINUS":       parseRule(unary,    binary, "PREC_TERM"),
         "TOKEN_PLUS":        parseRule(None,     binary, "PREC_TERM"),
         "TOKEN_SLASH":       parseRule(None,     binary, "PREC_FACTOR"),
         "TOKEN_STAR":        parseRule(None,     binary, "PREC_FACTOR"),
         # Literals
         "TOKEN_STRING":      parseRule(None,     None,   "PREC_NONE"),
         "TOKEN_NUMBER":      parseRule(number,   None,   "PREC_NONE"),
         # Keywords
         "TOKEN_SHOW":        parseRule(None,     None,   "PREC_NONE"),
         # Miscellaneous
         "TOKEN_ERROR":       parseRule(None,     None,   "PREC_NONE"),
         "TOKEN_EOF":         parseRule(None,     None,   "PREC_NONE"),
         "TOKEN_INDENT":      parseRule(None,     None,   "PREC_NONE"),
         "TOKEN_NEWLINE":     parseRule(None,     None,   "PREC_NONE"),
         }

# deal with operations that have different precedence
def parsePrecedence(precedence):
    # fetch the next token
    advance()
    # fetch the prefix rule
    prefRule = getRule(parser.previous.typeName).prefix
    # if we didn't have one
    if not prefRule:
        error("Expect expression")
        return
    # Otherwise, execute the prefix rule
    prefRule()
    # ensure we have a lower precedence
    while (precedence <= getRule(parser.current.typeName).prec):
        # fetch the infix rule
        infRule = getRule(parser.current.typeName).infix
        # and execute it if found
        if infRule:
            advance()
            infRule()
        # stop the loop if we didn't have a rule
        break

# fetch the precedence rule
def getRule(token):
    # return the rule given the token
    return Rules[token]

# compile source code to bytecode
def compile(source, chunk):
    # initialise our lexer
    initLexer(source)
    # and our parser
    initParser(chunk)
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


# create the parser
parser = Parser()
