#!python3

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple, Iterator

from command import Translator

# define comment patterns
LINE_COMMENT_DELIMITER        = "//"
BLOCK_COMMENT_START_DELIMITER = "/*"
BLOCK_COMMENT_END_DELIMITER   = "*/"

def parse_args() -> Tuple[Path, Path]:
    """ parse input and yield appropriate paths """
    parser = argparse.ArgumentParser(description="Translates a *.vm file and saves it to an *.asm file in the same directory.")
    parser.add_argument("input_path", help="path to input file")
    input_path = Path(parser.parse_args().input_path)
    return (input_path, input_path.parent/input_path.name.replace(".vm", ".asm"))

def strip_whitespace(input_file: Iterator[str]) -> Iterator[str]:
    """ strip out comments and whitespace  """
    block_comment_active = False
    for line in input_file:
        # check if we're processing a block comment - if we are, return fast
        if block_comment_active:
            if BLOCK_COMMENT_END_DELIMITER not in line:
                continue
            else:
                line = line.split(BLOCK_COMMENT_END_DELIMITER)[1]
                block_comment_active = False
        else: 
            if BLOCK_COMMENT_START_DELIMITER in line:
                line = line.split(BLOCK_COMMENT_START_DELIMITER)[0]
                block_comment_active = True
            # at this point, we only need to look for line comments
            else: 
                line = line.split(LINE_COMMENT_DELIMITER)[0]
        stripped = line.strip()
        # use None equivalence of empty string to avoid emitting empty lines
        if stripped:
            yield stripped

def main(input_path: Path, output_path: Path):
    """ wire up argument and file parsing to run translator """
    translator = Translator(input_path.stem)
    with open(input_path) as input_file, open(output_path, 'w') as output_file:
        for line in strip_whitespace(input_file):
            for command in translator.translate(line):
                print(command, file=output_file)

if __name__ == "__main__":
    main(*parse_args())
