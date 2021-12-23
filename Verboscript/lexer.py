# this will deal with all character lexing

# fetch any inbuilt python functions

# fetch our code
from common import *

# Global variables
tokenType = [# Single Character tokens
             "TOKEN_LEFT_PAREN", "TOKEN_RIGHT_PAREN",
             "TOKEN_DOT", "TOKEN_COMMA", "TOKEN_EQUAL",
             # Logical operations
             "TOKEN_EQUAL_EQUAL", "TOKEN_GREATER", "TOKEN_LESS", "TOKEN_NOT",
             # Operations tokens
             "TOKEN_MINUS", "TOKEN_PLUS", "TOKEN_SLASH", "TOKEN_STAR",
             # Literal tokens
             "TOKEN_IDENTIFIER", "TOKEN_STRING", "TOKEN_NUMBER",
             # Language keywords
             "TOKEN_FALSE", "TOKEN_NONE", "TOKEN_SHOW", "TOKEN_TRUE",
             # Miscellaneous
             "TOKEN_NEWLINE", "TOKEN_INDENT",
             "TOKEN_ERROR", "TOKEN_EOF", ]

# Token class
class Token:
    # initialisation function
    def __init__(self, typeName, literal, line, char=0):
        # define the token type
        self.type = tokenType.index(typeName)
        self.typeName = typeName
        # the literal token stuff
        self.literal = literal
        # and location that this token is found at
        self.line = line
        self.char = char

# Lexer class
class Lexer:
    # initialisation function
    def __init__(self, start=0, current=0, line=1, char=1):
        # the starting character
        self.start = start
        # the current character
        self.current = current
        # define the current line and character location of source code
        self.line = line
        self.char = char
        # begins with an empty source file
        source = ""
        # which has zero length
        sourcelen = 0

# initialise a lexer by providing source code
def initLexer(source):
    # restart the lexer
    lexer.__init__()
    # define the source
    lexer.source = source
    # and the source length, so we don't have to recompute it each time
    lexer.sourcelen = len(source)

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
def atEnd(offset = 0):
    return (lexer.current + offset) >= lexer.sourcelen

# function to compute if we are at the end of the file from the start, rather than current
def atEndFromStart(offset = 0):
    return (lexer.start + offset) >= lexer.sourcelen

# function to fetch the next character
def advance():
    # increment the current position
    lexer.current += 1
    lexer.char += 1
    # and return the previous character
    return lexer.source[lexer.current - 1]

# function to peek a the next character without consuming it
def peek(offset = 0):
    #print(lexer.current, offset)
    if atEnd(offset):
        return "\0"
    return lexer.source[lexer.current + offset]

# function to peek a the character as measured from the start, rather than current, of a token
def peekstart(offset = 0):
    #print(lexer.current, offset)
    if atEnd(offset):
        return "\0"
    return lexer.source[lexer.start + offset]

# function to see if the expected character apears
def match(exp):
    # check we aren't at the end of the file
    if atEnd():
        return False
    # if it isn't what we expect
    if peek() != exp:
        return False
    # if it is what we expected, increment and return
    lexer.current += 1
    return True

# function to check if a string appears since the start token
def matchchars(chars, pos=-1):
    # if we were not given a position, use the current
    if pos < 0:
        pos = lexer.current
    # check we aren't at the end of the file
    if atEndFromStart(len(chars)):
        return False
    # begin itterating through the chars
    for cou, val in enumerate(chars):
     if lexer.source[pos + cou] != val:
         return False
    # if it is what we expected, return true
    return True

# function to match multiple
def multimatch(chars):
    # check for a match
    matched = matchchars(chars)
    # if we had a match
    if matched:
        # then increment the current position
        lexer.current += len(chars)
    # return the true / false match
    return matched

# skip any whitespace that does not contribute to an indent
def skipWhitespace():
    # keep looping
    while True:
        # if the current character is a space
        if peek() == " ":
            # consume it
            advance()
            # and start the loop again
            continue
        # otherwise, stop
        return

# function to create a token from nothing
def makeToken(ttype):
    # grab a token using the current state of the lexer
    return Token(ttype, lexer.source[lexer.start : lexer.current], lexer.line, lexer.char - (lexer.current - lexer.start))

# function to create an error token
def errorToken(message):
    # grab a token using the current state of the lexer
    return Token("TOKEN_ERROR", message, lexer.line)

# function to return a string
def string(quoteType='"'):
    # keep going until we find the terminating mark
    while not atEnd() and (peek() != quoteType):
        # if we have a newline, skip it
        if peek() == "\n":
            # increment the line count, and reset the character count
            lexer.line += 1
            lexer.char = 1
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
    if (peek() in ["."]) and isDigit(peek(1)):
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
    if lexer.source[lexer.start : lexer.current] == string:
        return token
    # otherwise, return the default
    return "TOKEN_IDENTIFIER"

# check if a string of keywords match the input
def checkKeywordWithSpace(string, token):
    # check that the string sequence matches, and has a space afterwards
    if lexer.source[lexer.start : lexer.start + len(string) + 1] == string+" ":
        # jump the current position of the lexer forward to the end of the match
        lexer.current = lexer.start + len(string)
        # and return the token
        return token
    # otherwise, return the first keyword as an identifier
    return "TOKEN_IDENTIFIER"

# check for the identifier type
def identifierType():
    # fetch the first character we are lexing
    c = peekstart()
    nxt = peekstart(1)
    #check for tokens by matching their strings
    if c == "a":
        return checkKeyword("add", "TOKEN_PLUS")
    elif c == "e":
        # match for the unique first to filter it out
        if matchchars("equals", lexer.start):
            return checkKeyword("equals", "TOKEN_EQUAL_EQUAL")
        if matchchars("equal to", lexer.start):
            return checkKeywordWithSpace("equal to", "TOKEN_EQUAL_EQUAL")
    elif c == "f":
        return checkKeyword("false", "TOKEN_FALSE")
    elif c == "g":
        return checkKeywordWithSpace("greater than", "TOKEN_GREATER")
    elif c == "l":
        return checkKeywordWithSpace("less than", "TOKEN_LESS")
    elif c == "m":
        return checkKeyword("minus", "TOKEN_MINUS")
    elif c == "n":
        if nxt == "o":
            if peekstart(2) == "t":
                return checkKeyword("not", "TOKEN_NOT")
            return checkKeyword("none", "TOKEN_NONE")
    elif c == "o":
        return checkKeyword("over", "TOKEN_SLASH")
    elif c == "s":
        return checkKeyword("show", "TOKEN_SHOW")
    elif c == "t":
        if nxt == "r":
            return checkKeyword("true", "TOKEN_TRUE")
        elif nxt == "i":
            return checkKeyword("times", "TOKEN_STAR")
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
    # Skip any non-indenting whitepsace
    skipWhitespace()
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
    # indent and return characters
    if c == "\t":
        return makeToken("TOKEN_INDENT")
    elif c == "\n":
        # increment the line count, and reset the character count
        lexer.line += 1
        lexer.char = 1
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
    elif c == "!":
        return makeToken("TOKEN_NOT")
    elif c == ">":
        return makeToken("TOKEN_GREATER")
    elif c == "<":
        return makeToken("TOKEN_LESS")
    # Double width characters
    elif c == "=":
        # check for a following equality
        if peek() == "=":
            return makeToken("TOKEN_EQUAL_EQUAL")
        return makeToken("TOKEN_EQUAL")
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
