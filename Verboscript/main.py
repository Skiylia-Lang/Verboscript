# the main file that will (eventually) host everything needed.

# fetch any inbuilt python functions

# fetch our code
from OpCodes import *
from chunk import *

# global variables


# main function
def main():
    chunk = initChunk()
    writeChunk(chunk, "OP_RETURN")
    print(chunk)
    freeChunk(chunk)
    print(chunk)
    return 0

main()
