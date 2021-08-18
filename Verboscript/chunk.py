# script that will deal with manipulating chunks of bytecode

# fetch any inbuilt python functions

# fetch our code
from common import *
from value import *

# Global variables
OpCodes = {"OP_CONSTANT",
           # Booleans
           "OP_TRUE",
           "OP_FALSE",
           "OP_NONE",
           # Binary operations
           "OP_ADD",
           "OP_SUBTRACT",
           "OP_MULTIPLY",
           "OP_DIVIDE",
           # Unary operations
           "OP_NEGATE",
           # Miscellaneous
           "OP_RETURN",
           }

# the chunk class
class Chunk:
    def __init__(self):
        # the chunk begins with nothing
        self.count = 0
        # with an empty bytecode array
        self.code = list()
        # and no position information
        self.lines = list()
        self.chars = list()
        # and no local constants
        self.constants = ValueArray()

# write a byte to a chunk
def writeChunk(chunk, byte, line, char=0):
    # append the byte to the chunk
    chunk.code.append(byte)
    # add its position information
    chunk.lines.append(line)
    chunk.chars.append(char)
    # and increase the count
    chunk.count += 1

# add a constant to a chunk
def addConstant(chunk, value):
    # write it to the array
    writeValueArray(chunk.constants, value)
    # and return the index of the constant for later use
    return chunk.constants.count - 1
