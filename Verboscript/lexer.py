# this will deal with all character lexing

# fetch any inbuilt python functions

# fetch our code

# Global variables

# Lexer class
class Lexer:
    # begins with an empty source file
    source = ""
    # initialisation function
    def __init__(self, start=0, current=0, line=1):
        # the starting character
        self.start = start
        # the current character
        self.current = current
        # define the current line of source code
        self.line = line

# initialise a lexer by providing source code
def initLexer(source):
    lexer.source = source

# create our lexer
lexer = Lexer()
