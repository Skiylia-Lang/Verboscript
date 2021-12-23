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
    def __init__(self, valueType="VAL_NONE", value=None):
        # the value starts as null
        self.valueType = valueType
        self.value = value

# the constant class
class ValueArray:
    def __init__(self):
        # the valueArray begins with nothing
        self.count = 0
        self.values = list()

# create a number
def numVal(value):
    return Value("VAL_NUMBER", value)

# create a boolean
def boolVal(value):
    return Value("VAL_BOOL", value)

# create a number
def noneVal():
    return Value("VAL_NONE", None)

# return as a number
def asNum(value):
    return float(value.value)

# return as a boolean
def asBool(value):
    return bool(value.value)

# Check if a value has a certain typing
def isNum(value):
    return value.valueType == "VAL_NUMBER"

# Check if a value has a certain typing
def isBool(value):
    return value.valueType == "VAL_BOOL"

# Check if a value has a certain typing
def isNone(value):
    return value.valueType == "VAL_NONE"

# extract a numerical value
def formatValue(value):
    # fetch the value type
    valtype = value.valueType
    if valtype == "VAL_BOOL":
        return "true" if asBool(value) else "false"
    elif valtype == "VAL_NONE":
        return "None"
    elif valtype == "VAL_NUMBER":
        return asNum(value)

# extract an equality between two values
def valuesEqual(a, b):
    # if they have different types, they're not strictly equal
    if a.valueType != b.valueType:
        return False
    # otherwise, check for types
    if a.valueType == "VAL_BOOL":
        return asBool(a) == asBool(b)
    elif a.valueType == "VAL_NONE":
        return True
    elif a.valueType == "VAL_NUMBER":
        return asNum(a) == asNum(b)
    # false if nothing else
    return False

# write a value to a valueArray
def writeValueArray(valueArray, value):
    # append the byte to the chunk
    valueArray.values.append(value)
    # and increase the count
    valueArray.count += 1
