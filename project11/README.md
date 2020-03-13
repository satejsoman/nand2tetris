# Project 10: Tokenizer and Parser
tokenizes and parses Jack source code to create syntax trees 

## overview/structure

### entry points
- `parser.py` is a Python 3 project that takes in a valid *.jack file and produces the corresponding *.xml file in the input file's directory
- `tokenizer.py` is a Python 3 project that takes in a valid *.jack file and produces the corresponding *T.xml file in the input file's directory

### utilities 
- `stream.py` implements an iterator with a look-ahead ability
- `utils.py` contains common functions for setting up the parser and tokenizer 
- `tokens.py` enumerate the lexical elements of the Jack programming language
- `grammar.py` contains mutually-recursive functions implementing the grammar rules of the Jack programming language

## how to run 
neither the parser nor tokenizer have dependencies outside the Python3 standard library.
the files `tokens.py`, `grammar.py`, `utils.py`, and `stream.py` must be in the same directory as `parser.py` and `tokenizer.py`, however.

### tokenizer usage: 
    `python3 tokenizer.py <input_path>.jack` 

### parser usage: 
    `python3 parser.py <input_path>.jack` 

### help messages: 
running either program with the `-h` flag or without an input file path produces a message like: 
```
    usage: tokenizer.py [-h] input_path

    Tokenizes a <X>.jack file and saves it to an <X>T.xml file in the same
    directory.

    positional arguments:
    input_path  path to input file

    optional arguments:
    -h, --help  show this help message and exit
```