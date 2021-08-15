# this will house the virtual machine that executes bytecode

# fetch any inbuilt python functions

# fetch our code

# Global variables

# Lexer class
class Lexer:
    def __init__(self, start=0, current=0, line=1):
        # the starting character
        self.start = start
        # the current character
        self.current = current
        # define the current line of source code
        self.line = line
