# Project 0: Programming Best Practices 

## How to compile/run
The file `src/stripwhitespaces.py` is a Python3 program that takes a single filename (ending with "*.in") and saves the formatted contents of that file in the same directory as the input file, with the output extension changed to ".out". The only dependencies are on the Python3 standard library, so a vanilla install of Python3 or a brand new `conda`/`virtualenv` environment is all that is needed to run the program:

    `python3 src/stripwhitespaces.py myCoolProgram.in` 

For usage help, run:

    `python3 src/stripwhitespaces.py -h` 

## What works/doesn't work 
    - works:
        - stripping out empty lines
        - stripping out multi-line block comments
        - stripping out per-line comments 
