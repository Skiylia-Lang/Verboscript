# this will deal with all character lexing

# fetch any inbuilt python functions

# fetch our code

# Global variables
tokenType = [# Single Character tokens
             "TOKEN_LEFT_PAREN", "TOKEN_RIGHT_PAREN",
             "TOKEN_DOT", "TOKEN_COMMA",
             # Operations tokens
             "TOKEN_MINUS", "TOKEN_PLUS", "TOKEN_SLASH", "TOKEN_STAR",
             # Literal tokens
             "TOKEN_IDENTIFIER", "TOKEN_STRING", "TOKEN_NUMBER",
             # Language keywords
             "TOKEN_SHOW",
             # Miscellaneous
             "TOKEN_NEWLINE", "TOKEN_INDENT",
             "TOKEN_ERROR", "TOKEN_EOF", ]

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

# check if a character is a digit
def isDigit(char):
    return ("0" <= char <= "9")

# check if a character is alphabetical
def isAlpha(char):
    # check if the character is between a and z, or is an underscore
    return ("a" <= char.lower() <= "z") or (char == "_")

# check for alphanumerics
def isAlphaNumeric(char):
    return ("0" <= char <= "9") or ("a" <= char.lower() <= "z") or (char == "_")

# function to compute if we are at the end of the file
def atEnd():
    return lexer.source[lexer.current] == "\0"

# function to fetch the next character
def advance():
    # increment the current position
    lexer.current += 1
    # and return the previous character
    return lexer.source[lexer.current - 1]

# function to peek a the next character without consuming it
def peek():
    return lexer.source[lexer.current]

# function to see if the expected character apears
def match(exp):
    # check we aren't at the end of the file
    if atEnd():
        return False
    # if it isn't what we expect
    if lexer.source[lexer.current] != exp:
        return False
    # if it is what we expected, increment and return
    lexer.current += 1
    return True

# function to match multiple
def multimatch(chars):
    # check we aren't at the end of the file
    if atEnd():
        return False
    # begin itterating through the chars
    for x in range(len(chars)):
        # if the current isn't what we expect
        if lexer.source[lexer.current + x] != chars[x]:
            return False
    # if it is what we expected, increment and return
    lexer.current += len(chars)
    return True

# function to create a token from nothing
def makeToken(ttype):
    # grab a token using the current state of the lexer
    return Token(ttype, lexer.source[lexer.start : lexer.current], lexer.line)

# function to create an error token
def errorToken(message):
    # grab a token using the current state of the lexer
    return Token("TOKEN_ERROR", message, lexer.line)

# function to return a string
def string(quoteType='"'):
    # keep going until we find the terminating mark
    while (peek() != quoteType) and not atEnd():
        # if we have a newline, skip it
        if peek() == "\n":
            # increment the line counter
            lexer.line += 1
        # and advance to the next token
        advance()
    # if we hit the end, we need an error
    if atEnd():
        return errorToken("Unterminated string.")
    # otherwise, consume the closing quote, and return the token
    advance()
    return makeToken(TOKEN_STRING)

# create a number token
def number():
    # while we have digits
    while isDigit(peek()):
        # advance
        advance()
    # if we have any allowed punctuation, and the character after is a digit too
    if (peek() in ["."]) and isDigit(peekNext()):
        # consume the punctuation
        advance()
        # and consume the rest of the number
        while isDigit(peek()):
            advance()
    # return the number token
    return makeToken("TOKEN_NUMBER")

# check if a keyword matches the input
def checkKeyword(string, token):
    # check that the string math is the same as the lexer source at this point
    if lexer.source[lexer.start: lexer.current] == string:
        return token
    # otherwise, return the default
    return "TOKEN_IDENTIFIER"

# check for the identifier type
def identifierType():
    # fetch the first character we are lexing
    c = lexer.source[lexer.start]
    if c == "s":
        return checkKeyword("show", "TOKEN_SHOW")
    # currently we only deal with identifiers
    return "TOKEN_IDENTIFIER"

# create an identifier token
def identifier():
    # continue while we have Alpha Numeric characters
    while isAlphaNumeric(peek()):
        advance()
    #return the identifier
    return makeToken(identifierType())

# scan for a token
def scanToken():
    # update the start and current positions
    lexer.start = lexer.current
    # check if we are at the end of the file
    if (atEnd()):
        return makeToken("TOKEN_EOF")
    # Check the next character
    c = advance()
    # identifiers
    if isAlpha(c):
        return identifier()
    # Numbers
    if isDigit(c):
        return number()
    # Whitespace and return characters
    if c == " ":
        # if we have a 4-whitespace gap
        if multimatch("   "):
            # then make an indet token
            return makeToken("TOKEN_INDENT")
        # otherwise skip the whitespace
    elif c == "\t":
        return makeToken("TOKEN_INDENT")
    elif c == "\n":
        # increment the line count
        lexer.line += 1
        return makeToken("TOKEN_NEWLINE")
    # Single width characters
    elif c == "(":
        return makeToken("TOKEN_LEFT_PAREN")
    elif c == ")":
        return makeToken("TOKEN_RIGHT_PAREN")
    elif c == ".":
        return makeToken("TOKEN_DOT")
    elif c == ",":
        return makeToken("TOKEN_COMMA")
    # Operations
    elif c == "+":
        return makeToken("TOKEN_PLUS")
    elif c == "-":
        return makeToken("TOKEN_MINUS")
    elif c == "*":
        return makeToken("TOKEN_STAR")
    elif c == "/":
        return makeToken("TOKEN_SLASH")
    # Forced string matches
    elif c == "'":
        return string("'")
    elif c == '"':
        return string('"')
    else:
        # if we found a token we don't recognise
        return errorToken("Unexpected Character")

# create our lexer
lexer = Lexer()
