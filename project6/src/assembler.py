#!python3

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Iterator, Tuple

from instruction import AInstruction, Instruction, Label, Symbol
from symboltable import SymbolTable

# define comment patterns
LINE_COMMENT_DELIMITER        = "//"
BLOCK_COMMENT_START_DELIMITER = "/*"
BLOCK_COMMENT_END_DELIMITER   = "*/"


def parse_args() -> Tuple[Path, Path]:
    """parse input path and construct output path"""
    parser = argparse.ArgumentParser(description="Assembles a *.asm file and saves it to an *.hack file in the same folder.")
    parser.add_argument("input_path", help="path to input file")
    args = parser.parse_args()
    input_path = Path(args.input_path)
    output_path = input_path.parent/input_path.name.replace(".asm", ".hack")
    return (input_path, output_path)


def preprocess_line(line: str, block_comment_active: bool = False) -> Tuple[str, bool]:
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


def preprocess_file(input_file: Iterator[str]) -> Iterator[str]:
    """ zeroth pass: strip out comments and whitespace  """
    block_comment_active = False
    for line in input_file:
        result, block_comment_active = preprocess_line(line, block_comment_active) 
        if result: # use None equivalence of empty string to avoid emitting empty lines 
            yield result


def handle_labels(table: SymbolTable, instructions: Iterator[str]) -> Iterator[Instruction]:
    """ first pass: populate symbol table with labels"""
    instruction_number = 0
    for line in instructions:
        parsed = Instruction.parse(line)
        if isinstance(parsed, Label):
            table.put_label(parsed, instruction_number)
        else:
            instruction_number += 1
            yield parsed 


def handle_symbols(table: SymbolTable, instructions: Iterator[Instruction]) -> Iterator[Instruction]:
    """ second pass: resolve symbols """
    for instruction in list(instructions): # force incoming iterator to exhaust itself first so symbol table properly built
        if isinstance(instruction, Symbol):
            if instruction not in table:
                table.put_symbol(instruction)
            yield AInstruction(table[instruction])
        else:
            yield instruction


def main(input_path: Path, output_path: Path):
    """ wire up argument and file parsing to run assembler """
    with open(input_path) as input_file, open(output_path, 'w') as output_file: 
        stripped = preprocess_file(input_file)
        symbol_table = SymbolTable()
        instruction_stream = handle_labels(symbol_table, stripped)
        for instruction in handle_symbols(symbol_table, instruction_stream):
            print(instruction, file=output_file)


if __name__ == "__main__":
    main(*parse_args())
