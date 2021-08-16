# this will house the compiler, that will take source code and spit out bytecode

# fetch any inbuilt python functions

# fetch our code
from common import *
from lexer import *

# Global variables

# compile source code to bytecode
def compile(source):
    #initialise our lexer
    initLexer(source)
    # base line value
    line = -1
    # iterate until done
    while True:
        # create the next token
        token = scanToken()
        # update the line if need be
        if token.line != line:
            # print the token line to the screen
            printn("{:04d}".format(token.line))
            # and update our internal variable
            line = token.line
        else:
            # otherwise, show the carry bar
            printn("   |")
        # print the token I suppose
        print("{:2d} '{}', '{}'".format(token.type, token.literal, token.typeName))
        # and check for an End of file
        if token.typeName == "TOKEN_EOF":
            break
