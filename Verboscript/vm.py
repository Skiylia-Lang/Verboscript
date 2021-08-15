# this will house the virtual machine that executes bytecode

# fetch any inbuilt python functions

# fetch our code
from chunk import *

# define the virtual machine class
class VM:
    def __init__(self):
        self.chunk = Chunk()

# and create the virtual machine
vm = VM()
