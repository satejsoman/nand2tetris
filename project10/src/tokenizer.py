import argparse
from pathlib import Path
from typing import Iterator, Tuple

from jacktoken import Token

LINE_COMMENT_DELIMITER        = "//"
BLOCK_COMMENT_START_DELIMITER = "/*"
BLOCK_COMMENT_END_DELIMITER   = "*/"

def parse_args() -> Tuple[Path, Path]:
    """ parse arguments and return appropriate paths """
    parser = argparse.ArgumentParser(description="Tokenizes a <X>.jack file and saves it to an <X>T.xml file in the same directory.")
    parser.add_argument("input_path", help="path to input file")
    input_path = Path(parser.parse_args().input_path).resolve()
    return (input_path, input_path.parent/input_path.name.replace(".jack", "T.xml"))

def strip_whitespace(input_file: Iterator[str]) -> Iterator[str]:
    """ strip out comments and whitespace  """
    block_comment_active = False
    for line in input_file:
        # print("L0", line, flush=False)
        # check if we're processing a block comment - if we are, return fast
        if block_comment_active:
            if BLOCK_COMMENT_END_DELIMITER not in line:
                continue
            else:
                block_comment_active = False
                line = line.split(BLOCK_COMMENT_END_DELIMITER)[1]
        else: 
            if BLOCK_COMMENT_START_DELIMITER in line:
                block_comment_active = BLOCK_COMMENT_END_DELIMITER not in line
                line = line.split(BLOCK_COMMENT_START_DELIMITER)[0]
            # at this point, we only need to look for line comments
            else: 
                line = line.split(LINE_COMMENT_DELIMITER)[0]
        stripped = line.strip()
        # print("LS", line, stripped)
        # use None equivalence of empty string to avoid emitting empty lines
        if stripped:
            yield stripped

def tokenize(stream: Iterator[str]) -> Iterator[Token]:
    yield Token.START 
    for line in stream: 
        yield from Token.parse_line(line)
    yield Token.STOP 

def main(input_path: Path, output_path: Path):
    """ wire up argument and file parsing to run tokenizer """
    with open(input_path) as input_file, open(output_path, 'w') as output_file:
        for token in tokenize(strip_whitespace(input_file)):
            print(token, file=output_file)

if __name__ == "__main__":
    main(*parse_args())
