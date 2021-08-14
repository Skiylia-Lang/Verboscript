# script that will deal with manipulating chunks of bytecode

# fetch any inbuilt python functions

# fetch our code
from OpCodes import OpCodes
from value import *

# the chunk class
class Chunk:
    def __init__(self):
        # the chunk begins with nothing
        self.count = 0
        # with an empty bytecode array
        self.code = list()
        # and no local constants
        self.constants = ValueArray()

# write a byte to a chunk
def writeChunk(chunk, byte):
    # append the byte to the chunk
    chunk.code.append(byte)
    # and increase the count
    chunk.count += 1

# completely empty a chunk
def freeChunk(chunk):
    # delete everything
    chunk.__init__()

# add a constant to a chunk
def addConstant(chunk, value):
    # write it to the array
    writeValueArray(chunk.constants, value)
    # and return the index of the constant for later use
    return chunk.constants.count - 1
