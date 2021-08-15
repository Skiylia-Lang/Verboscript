# this will deal with all character lexing

# fetch any inbuilt python functions

# fetch our code

# Global variables
tokenType = [# Single character tokens
             "TOKEN_MINUS", "TOKEN_PLUS", "TOKEN_SLASH", "TOKEN_STAR",
             # Literals
             "TOKEN_NUMBER",
             # Miscellaneous
             "TOKEN_ERROR", "TOKEN_EOF",]

# Token class
class Token:
    # initialisation function
    def __init__(self, typeName, literal, line):
        # define the token type
        self.type = tokenType.index(typeName)
        self.typeName = typeName
        # the literal token stuff
        self.literal
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

# function to compute if we are at the end of the file
def atEnd():
    return lexer.source[lexer.current] == "\0"

# function to create a token from nothing
def makeToken(ttype):
    # grab a token using the current state of the lexer
    return Token(ttype, lexer.source[lexer.start : lexer.current - lexer.start], lexer.line)

# function to create an error token
def errorToken(message):
    # grab a token using the current state of the lexer
    return Token("TOKEN_ERROR", message, lexer.line)

# scan for a token
def scanToken():
    # update the start and current positions
    lexer.start = lexer.current
    # check if we are at the end of the file
    if (atEnd()):
        return makeToken("TOKEN_EOF")
    # and if we found a token we don't recognise
    return errorToken("Unexpected Character")

# create our lexer
lexer = Lexer()
