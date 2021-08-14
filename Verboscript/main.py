# the main file that will (eventually) host everything needed.

# fetch any inbuilt python functions

# fetch our code
from chunk import *
from debug import *

# main function
def main():
    # testing suite
    chunk = Chunk()
    writeChunk(chunk, "OP_RETURN")

    disassembleChunk(chunk, "Test")
    freeChunk(chunk)
    return 0

main()
