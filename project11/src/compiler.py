from pathlib import Path
from pprint import pprint

from commons.utils import parse_args, strip_whitespace
from jack.grammar import parse_jack_class
from jack.tokens import tokenize
from jack.symboltable import SymbolTable 


def main(paths: Iterator[Tuple[Path, Path]]):
    """ wire up argument and file parsing to run code parser """
    for (input_path, output_path) in paths:
        with open(input_path) as input_file, open(output_path) as output_file:
            parse_tree = parse_jack_class(tokenize(strip_whitespace(input_file)))
            table = SymbolTable.populate_from(parse_tree)
            print(table)


if __name__ == "__main__":
    main(parse_directory_args(
        description = "Compiles each <X>.jack file in the input directory and saves it to an <X>.vm file in the same directory.",
        src_pattern = ".jack", 
        dst_pattern = ".vm"
    ))
