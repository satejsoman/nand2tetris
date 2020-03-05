from pathlib import Path 

from compiler import compile_jack
from tokenizer import tokenize
from utils import parse_args, strip_whitespace


def main(input_path: Path, output_path: Path):
    """ wire up argument and file parsing to run code parser """
    with open(input_path) as input_file, open(output_path, 'w') as output_file:
        for line in compile_jack(tokenize(strip_whitespace(input_file))).render():
            print(line, file = output_file)

if __name__ == "__main__":
    main(*parse_args(
        description = "Parses a <X>.jack file and saves it to an <X>.xml file in the same directory.",
        src_pattern = ".jack", 
        dst_pattern = ".xml"
    ))
