# the main file that will (eventually) host everything needed.

# fetch any inbuilt python functions

# fetch our code
from chunk import *
from common import *
from debug import *
from vm import *

# main function
def main():
    # testing suite
    chunk = Chunk()

    #write a chunk by hand
    constant = addConstant(chunk, 1.5)
    writeChunk(chunk, "OP_CONSTANT", 123)
    writeChunk(chunk, constant, 123)

    constant = addConstant(chunk, 3.7)
    writeChunk(chunk, "OP_CONSTANT", 123)
    writeChunk(chunk, constant, 123)

    writeChunk(chunk, "OP_ADD", 123)

    constant = addConstant(chunk, 5.2)
    writeChunk(chunk, "OP_CONSTANT", 123)
    writeChunk(chunk, constant, 123)

    writeChunk(chunk, "OP_DIVIDE", 123)

    writeChunk(chunk, "OP_NEGATE", 123)

    writeChunk(chunk, "OP_RETURN", 123)

    #show the debug info about the chunk
    disassembleChunk(chunk, "Test chunk")
    # use the virtual machine to interpret a chunk
    interpret(chunk)
    return 0

main()
