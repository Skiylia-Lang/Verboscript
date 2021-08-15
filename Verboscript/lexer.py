# this will deal with all character lexing

# fetch any inbuilt python functions

# fetch our code

# Global variables
tokenType = [# Single character tokens
             "TOKEN_MINUS", "TOKEN_PLUS", "TOKEN_SLASH", "TOKEN_STAR",
             # Literals
             "TOKEN_NUMBER",
             # Miscellaneous
             "TOKEN_EOF",]

# Token class
class Token:
    # initialisation function
    def __init__(self, typeName, start, length, line):
        # define the token type
        self.type = tokenType.index(typeName)
        self.typeName = typeName
        # the start coordinate and length
        self.start = start
        self.length = length
        # and the line that this token is found on
        self.line = line

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
