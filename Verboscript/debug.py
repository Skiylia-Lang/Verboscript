# script that will show some verbose output to maintainers of verboscript.

# fetch any inbuilt python functions

# fetch our code
from chunk import *
from common import *

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
    printn("{:04d}".format(offset))
    # if this instruction is on the same line as the previous
    if (offset > 0) and (chunk.lines[offset] == chunk.lines[offset - 1]):
        # print a line continuation bar
        printn("   |")
    # otherwise print the new line
    else:
        printn("{:04d}".format(chunk.lines[offset]))
    # fetch the instruction
    instruct = chunk.code[offset]
    # check for the instruction
    if instruct in OpCodes:
        # find the instruction type and print
        if instruct in ["OP_CONSTANT"]:
            return constantInstruction(instruct, chunk, offset)
        elif instruct in [#Booleans
                          "OP_NONE", "OP_FALSE", "OP_TRUE",
                          #Mathematical operations
                          "OP_ADD", "OP_SUBTRACT", "OP_MULTIPLY", "OP_DIVIDE", "OP_NEGATE",
                          # Miscellaneous
                          "OP_RETURN"]:
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
    print("{:<16s} {:4d} '{}'".format(name, const, formatValue(chunk.constants.values[const])))
    # and return the offset
    return offset + 2

# show a simple instruction to the user
def simpleInstruction(name, offset):
    # print the name
    print(name)
    # increment the offset
    return offset + 1
