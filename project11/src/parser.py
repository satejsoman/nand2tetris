from pathlib import Path

from commons.utils import parse_args, strip_whitespace
from jack.grammar import parse_jack_class
from jack.tokens import tokenize


def main(input_path: Path, output_path: Path):
    """ wire up argument and file parsing to run code parser """
    with open(input_path) as input_file, open(output_path, 'w') as output_file:
        print(parse_jack_class(tokenize(strip_whitespace(input_file))), file = output_file)

if __name__ == "__main__":
    main(*parse_file_args(
        description = "Parses a <X>.jack file and saves it to an <X>.xml file in the same directory.",
        src_pattern = ".jack", 
        dst_pattern = ".xml"
    ))
