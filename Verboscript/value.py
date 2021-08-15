# script that will deal with manipulating constant arrays

# fetch any inbuilt python functions

# fetch our code

# the constant class
class ValueArray:
    def __init__(self):
        # the valueArray begins with nothing
        self.count = 0
        self.values = list()

# write a value to a valueArray
def writeValueArray(valueArray, value):
    # append the byte to the chunk
    valueArray.values.append(value)
    # and increase the count
    valueArray.count += 1
