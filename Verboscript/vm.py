# this will house the virtual machine that executes bytecode

# fetch any inbuilt python functions

# fetch our code
from OpCodes import *
from chunk import *

# Global variables
interpretResult = {"INTERPRET_OK",
                   "INTERPRET_COMPILE_ERROR",
                   "INTERPRET_RUNTIME_ERROR",
                   }

# define the virtual machine class
class VM:
    def __init__(self):
        # store the current chunk to work on
        self.chunk = Chunk()
        # and the instruction pointer
        self.ip = iter([0])

# function to run a chunk
def run():
    # function to read the current byte, and increase the instruction pointer
    def readByte():
        return next(vm.ip)

    # function to read a constant
    def readConstant():
        # fetch the constant id, and return the constant at that point
        return vm.chunk.constants.values[readByte()]

    #continue looping
    while True:
        # fetch the instruction
        instruct = readByte()
        # check the byte type is a valid opcode
        if instruct in OpCodes:
            if instruct == "OP_CONSTANT":
                # fetch the constant
                const = readConstant()
                # print to the screen
                print(const)
                # and stop the loop
                break
            elif instruct == "OP_RETURN":
                return "INTERPRET_OK"

# interpret a chunk using the virtual machine
def interpret(chunk):
    # set the chunk that the vm will work on
    vm.chunk = chunk
    # and set the instruction pointer
    vm.ip = iter(chunk.code)
    # and return the execution
    return run()

# and create the virtual machine
vm = VM()
