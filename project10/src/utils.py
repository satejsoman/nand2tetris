from typing import Tuple 

LINE_COMMENT_DELIMITER        = "//"
BLOCK_COMMENT_START_DELIMITER = "/*"
BLOCK_COMMENT_END_DELIMITER   = "*/"

def parse_args(description: str, src_pattern: str, dst_pattern) -> Tuple[Path, Path]:
    """ parse arguments and return appropriate paths """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input_path", help="path to input file")
    input_path = Path(parser.parse_args().input_path).resolve()
    return (input_path, input_path.parent/input_path.name.replace(src_pattern, dst_pattern))

def strip_whitespace(input_file: Iterator[str]) -> Iterator[str]:
    """ strip out comments and whitespace  """
    block_comment_active = False
    for line in input_file:
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
        # use None equivalence of empty string to avoid emitting empty lines
        if stripped:
            yield stripped