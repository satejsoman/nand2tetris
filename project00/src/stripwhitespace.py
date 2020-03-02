#!python3

import argparse
import re
import sys
from pathlib import Path
from typing import Tuple

# define comment patterns
LINE_COMMENT_DELIMITER        = "//"
BLOCK_COMMENT_START_DELIMITER = "/*"
BLOCK_COMMENT_END_DELIMITER   = "*/"


def process_line(line: str, block_comment_active: bool = False) -> Tuple[str, bool]:
    """process a given line and decide whether or not to emit a stripped version of it"""
    
    # check if we're processing a block comment - if we are, return fast 
    if block_comment_active:
        if BLOCK_COMMENT_END_DELIMITER not in line: 
            return ("", True)
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

    return line.strip(), block_comment_active


def parse_args() -> Tuple[Path, Path]:
    """parse input path and construct output path"""
    parser = argparse.ArgumentParser(description="Strip whitespace out of *.in files and save to *.out files.")
    parser.add_argument("input_path",  help="path to input file")
    args = parser.parse_args()
    input_path = Path(args.input_path)
    output_path = input_path.parent/input_path.name.replace(".in", ".out")
    return (input_path, output_path)


def main(input_path: Path, output_path: Path) -> None:
    block_comment_active = False
    with open(input_path) as input_file, open(output_path, 'w') as output_file:
        for line in input_file:
            result, block_comment_active = process_line(line, block_comment_active) 
            if result: # use None equivalence of empty string to avoid printing 
                print(result, file=output_file)

if __name__ == "__main__":
    main(*parse_args())
