from argparse import ArgumentParser
from pathlib import Path
from typing import Iterator, Tuple

LINE_COMMENT, BLOCK_COMMENT_START, BLOCK_COMMENT_END = "//", "/*", "*/"

def parse_args(description: str, src_pattern: str, dst_pattern) -> Tuple[Path, Path]:
    """ parse arguments and return appropriate paths """
    parser = ArgumentParser(description=description)
    parser.add_argument("input_path", help="path to input file")
    input_path = Path(parser.parse_args().input_path).resolve()
    return (input_path, input_path.parent/input_path.name.replace(src_pattern, dst_pattern))

def strip_whitespace(input_file: Iterator[str]) -> Iterator[str]:
    """ strip out comments and whitespace  """
    block_comment_active = False
    for line in input_file:
        if block_comment_active: # check if we're processing a block comment - if we are, return fast
            if BLOCK_COMMENT_END in line:
                block_comment_active, line = False, line.split(BLOCK_COMMENT_END)[1]
            else:
                continue
        else: 
            if BLOCK_COMMENT_START in line:
                block_comment_active = BLOCK_COMMENT_END not in line
                line = line.split(BLOCK_COMMENT_START)[0]
            else: # at this point, we only need to look for line comments
                line = line.split(LINE_COMMENT)[0]
        stripped = line.strip()
        if stripped: # use None equivalence of empty string to avoid emitting empty lines
            yield stripped
