# the main file that will (eventually) host everything needed.

# fetch any inbuilt python functions
import os, sys

# fetch our code
from chunk import *
from common import *
from debug import *
from vm import *

# the repl (Read, Evaluate, Print, Loop.)
def repl():
    # loop indefinitely
    while True:
        # fetch the input
        inp = input("> ")
        # if we didn't recieve anything
        if not inp:
            # then just quit
            break
        #else, try to interpret the input
        interpret(inp)

# read the contents of a file
def readFile(path):
    # check the file exists
    if not os.path.exists(path):
        print("File '{}' does not exist".format(path))
        sys.exit(74)
    # open the file
    with open(path, "r") as f:
        #fetch the source code
        source = f.read()
    # and return the source code
    return source

# add the ability to run files
def runFile(path):
    # ensure we have a fileextension
    if "." not in path:
        print("No file extension given for '{}'".format(path))
        sys.exit(2)
    # ensure we have the correct filetype
    ext = path.split(".")[-1]
    if ext != "vrbo":
        print("Non-Verboscript file extension '.{}'".format(ext))
        sys.exit(11)
    # fetch the source code
    source = readFile(path)
    # fetch the results
    result = interpret(source)
    # and check for exit codes
    if result == "INTERPRET_COMPILE_ERROR":
        sys.exit(65)
    if result == "INTERPRET_RUNTIME_ERROR":
        sys.exit(70)

# main function
def main(*args):
    # set the argument length
    argc = len(args)
    # spin up the vm
    initVM()
    #check if any arguments were passed
    if argc == 1:
        repl()
    elif argc == 2:
        runFile(args[1])
    else:
        print("Usage: verboscript [path]")
        sys.exit(64)
    return 0

main("verboscript")
