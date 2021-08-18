# script that will deal with manipulating constant arrays

# fetch any inbuilt python functions

# fetch our code
from common import *

# A list of allowed value types
valueType = ["VAL_BOOL",
             "VAL_NONE",
             "VAL_NUMBER",]

# the base class that represents a value
class Value():
    def __init__(self, value=None):
        # the value starts as null
        self.valueType = "VAL_NONE"
        self.value = value

# the constant class
class ValueArray:
    def __init__(self):
        # the valueArray begins with nothing
        self.count = 0
        self.values = list()

# create a number
def asNum(value):
    return Value(float(value))

# create a boolean
def asBool(value):
    return Value(bool(value))

# Check if a value has a certain typing
def isNum(value):
    return value.valueType == "VAL_NUMBER"

# Check if a value has a certain typing
def isBool(value):
    return value.valueType == "VAL_BOOL"

# Check if a value has a certain typing
def isNone(value):
    return value.valueType == "VAL_NONE"

# write a value to a valueArray
def writeValueArray(valueArray, value):
    # append the byte to the chunk
    valueArray.values.append(value)
    # and increase the count
    valueArray.count += 1
