# script that will deal with manipulating chunks of bytecode

# fetch any inbuilt python functions

# fetch our code
from value import *

# Global variables
OpCodes = {"OP_CONSTANT",
           "OP_NEGATE",
           "OP_RETURN",
           }

# the chunk class
class Chunk:
    def __init__(self):
        # the chunk begins with nothing
        self.count = 0
        # with an empty bytecode array
        self.code = list()
        # and no line information
        self.lines = list()
        # and no local constants
        self.constants = ValueArray()

# write a byte to a chunk
def writeChunk(chunk, byte, line):
    # append the byte to the chunk
    chunk.code.append(byte)
    # add its line information
    chunk.lines.append(line)
    # and increase the count
    chunk.count += 1

# add a constant to a chunk
def addConstant(chunk, value):
    # write it to the array
    writeValueArray(chunk.constants, value)
    # and return the index of the constant for later use
    return chunk.constants.count - 1
