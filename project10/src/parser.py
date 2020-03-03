
from utils import parse_args, strip_whitespace
from tokenizer import tokenize

def main(input_path: Path, output_path: Path):
    """ wire up argument and file parsing to run code parser """
    for token in tokenize(strip_whitespace(input_path)):
        pass 

if __name__ == "__main__":
    main(*parse_args(
        description = "Parses a <X>.jack file and saves it to an <X>.xml file in the same directory.",
        src_pattern = ".jack", 
        dst_pattern = ".xml"
    ))