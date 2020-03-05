from pathlib import Path
from typing import Iterator, Union

from tokens import Token
from utils import parse_args, strip_whitespace

def tokenize(stream: Iterator[str]) -> Iterator[Token]:
    for line in stream: 
        yield from Token.parse_line(line)

def wrapped_tokenize(stream: Iterator[str]) -> Iterator[Union[Token, str]]:
    yield "<tokens>"
    yield from tokenize(stream)
    yield "</tokens>" 

def main(input_path: Path, output_path: Path):
    """ wire up argument and file parsing to run tokenizer """
    with open(input_path) as input_file, open(output_path, 'w') as output_file:
        for token in wrapped_tokenize(strip_whitespace(input_file)):
            print(token, file=output_file)

if __name__ == "__main__":
    main(*parse_args(
        description = "Tokenizes a <X>.jack file and saves it to an <X>T.xml file in the same directory.",
        src_pattern = ".jack", 
        dst_pattern = "T.xml"
    ))
