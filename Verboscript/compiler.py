# this will house the compiler, that will take source code and spit out bytecode

# fetch any inbuilt python functions

# fetch our code
from lexer import *

# Global variables

# compile source code to bytecode
def compile(source):
    #initialise our lexer
    lexer = Lexer(source)
