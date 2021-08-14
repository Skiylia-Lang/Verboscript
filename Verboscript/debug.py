# script that will show some verbose output to maintainers of verboscript.

# fetch any inbuilt python functions

# fetch our code
from OpCodes import OpCodes

# disasemble a chunk to view all the bytecode
def disassembleChunk(chunk, name=""):
    # print the chunk name
    print("== {} ==".format(name))
    # initialise at zero
    offset = 0
    # iterate until we reach the end of the chunk
    while offset < chunk.count:
        # fetch the new offset by disasembling the next instruction
        # (instructions may not all be the same length)
        offset = disasembleInstruction(chunk, offset)

# disasemble a single instruction in a chunk
def disasembleInstruction(chunk, offset):
    # print the offset number without a newline
    print("{:04d} ".format(offset), end="")
    # fetch the instruction
    instruct = chunk.code[offset]
    # check for the instruction
    if instruct in OpCodes:
        # find the instruction type and print
        if instruct == "OP_CONSTANT":
            return constantInstruction(instruct, chunk, offset)
        elif instruct == "OP_RETURN":
            return simpleInstruction(instruct, offset)
    else:
        # otherwise show a mini error
        print("Unknown opcode {}".format(instruct))
        # increment the offset
        return offset + 1

# show an instruction to store a constant to the user
def constantInstruction(name, chunk, offset):
    # fetch the constant value
    const = chunk.code[offset + 1]
    # and print
    print("{:<16s} {:4d} {}".format(name, const, chunk.constants.values[const]))
    # and return the offset
    return offset + 2

# show a simple instruction to the user
def simpleInstruction(name, offset):
    # print the name
    print(name)
    # increment the offset
    return offset + 1
