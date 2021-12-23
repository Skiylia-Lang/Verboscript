# this will house the virtual machine that executes bytecode

# fetch any inbuilt python functions
import operator as op

# fetch our code
from chunk import *
from common import *
from compiler import *
from debug import *

# Global variables
interpretResult = {"INTERPRET_OK",
                   "INTERPRET_COMPILE_ERROR",
                   "INTERPRET_RUNTIME_ERROR",
                   }

# define the virtual machine class
class VM:
    def __init__(self, chunk):
        # store the current chunk to work on
        self.chunk = chunk
        # the instruction pointer
        self.ip = 0
        # and the stack
        self.stack = list()

# show an error message
def runtimeError(format, *args):
    # fetch the current token responsibe
    line, char = vm.chunk.lines[vm.ip - 1], vm.chunk.chars[vm.ip - 1]
    # and print an error message
    print("[line {}, char {}] Error".format(line, char))
    # reset the vm stack
    #vm.stack = list()

# startup the vm
def initVM(chunk=""):
    if not chunk:
        chunk = Chunk()
    vm.__init__(chunk)

# function to read the current byte, and increase the instruction pointer
def readByte():
    # increment the instruction pointer
    vm.ip += 1
    # and return the previous byte
    return vm.chunk.code[vm.ip - 1]

# function to read a constant
def readConstant():
    # fetch the constant id, and return the constant at that point
    return vm.chunk.constants.values[readByte()]

# function for binary operations
def BINARY_OP(valueType, op):
    # check if we have two numbers on top of the stack
    if (not isNum(peek(0))) or (not isNum(peek(1))):
        runtimeError("Operands must be numbers.")
        return "INTERPRET_RUNTIME_ERROR"
    # fetch the two operands (in reverse order because stack)
    b = asNum(pop())
    a = asNum(pop())
    # and push the operation result, using the op function
    push(valueType(op(a, b)))

# function to run a chunk
def run():
    if DEBUG_TRACE_EXECUTION:
        print("\n== {} ==".format("Code Execution"))
    #continue looping
    while True:
        # check if we are debugging stuff
        if DEBUG_TRACE_EXECUTION:
            if vm.stack:
                # print a blank space and clarifier
                printn("   stack:")
                # iterate through and print the stack
                for x in vm.stack:
                    printn("[ {} ]".format(formatValue(x)))
                # and show a default print to get onto a newline
                print()
            # and disasemble each instruction
            disasembleInstruction(vm.chunk, vm.ip)
        # fetch the instruction
        instruct = readByte()
        # check the byte type is a valid opcode
        if instruct in OpCodes:
            if instruct == "OP_CONSTANT":
                # fetch the constant
                const = readConstant()
                # push the value to the stack
                push(const)
            elif instruct == "OP_NONE":
                # push none to the stack
                push(noneVal())
            elif instruct == "OP_FALSE":
                # push false to the stack
                push(boolVal(False))
            elif instruct == "OP_TRUE":
                # push true to the stack
                push(boolVal(True))
            elif instruct == "OP_EQUAL":
                # fetch the two operands
                b = pop()
                a = pop()
                # and compare them
                push(boolVal(valuesEqual(a, b)))
            elif instruct == "OP_GREATER":
                # binary operation of greater than
                BINARY_OP(boolVal, op.gt)
            elif instruct == "OP_LESS":
                # binary operation of less than
                BINARY_OP(boolVal, op.lt)
            elif instruct == "OP_ADD":
                # do the binary operation with addition
                BINARY_OP(numVal, op.add)
            elif instruct == "OP_SUBTRACT":
                # do the binary operation with addition
                BINARY_OP(numVal, op.sub)
            elif instruct == "OP_MULTIPLY":
                # do the binary operation with addition
                BINARY_OP(numVal, op.mul)
            elif instruct == "OP_DIVIDE":
                # do the binary operation with addition
                BINARY_OP(numVal, op.truediv)
            elif instruct == "OP_NOT":
                # negate a truthy
                push(boolVal(isFalsey(pop())))
            elif instruct == "OP_NEGATE":
                # ensure we have a Number
                if not isNum(peek(0)):
                    runtimeError("Operand must be a number.")
                    return "INTERPRET_RUNTIME_ERROR"
                # fetch the value on top of the stack, negate it, and push it back
                push(numVal(-asNum(pop())))
            elif instruct == "OP_RETURN":
                # show whatever is on top of the stack for now
                print(formatValue(pop()))
                # and return an interpret okay message
                return "INTERPRET_OK"

# interpret a chunk using the virtual machine
def interpret(source):
    # create an empty chunk
    chunk = Chunk()
    # attempt to compile
    if not compile(source, chunk):
        # if it failed, throw an error
        return "INTERPRET_COMPILE_ERROR"
    # otherwise, start the compilation
    initVM(chunk)
    # fetch the result
    result = run()
    # and return it
    return result

# push to the stack
def push(value):
    vm.stack.append(value)

# and pop from the stack
def pop():
    return vm.stack.pop()

# peek at the top of the stack without removing or adding information
def peek(dist=0):
    return vm.stack[-int(1+dist)]

# check if a thing is falsey
def isFalsey(value):
    # ensue the value is boolean, and not null
    return isNone(value) or (isBool(value) and not asBool(value))

# and create the virtual machine
vm = VM(Chunk())
