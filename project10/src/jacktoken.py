import re
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

class Token(Element):
    """ subclass of XML element to expedite serializing Jack tokens """
    def __init__(self, val = ""):
        super().__init__(self.__class__.__name__[0].lower() + self.__class__.__name__[1:])
        self.text = " {} ".format(val)

    def __str__(self):
        return tostring(self).decode("ascii")

class Keyword(Token):         elements = set(["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null",  "this", "let", "do", "if", "else", "while", "return"])
class Symbol(Token):          elements = set(r"{}()[].,;+-*/&|<>=~") 
class IntegerConstant(Token): pattern = re.compile("^\d+$")
class StringConstant(Token):  pattern = re.compile("^\"(.*)\"$")
class Identifier(Token):      pass 

class Delimiter(Token):
    def __init__(self, label):
        self.label = label
    
    def __str__(self):
        return "<{}>".format(self.label)

def dispatch(text: str) -> Token:
    if text in Keyword.elements:
        return Keyword(text)
    elif text in Symbol.elements:
        return Symbol(text)
    integer_constant_match = IntegerConstant.pattern.match(text)
    if integer_constant_match:
        return IntegerConstant(str(integer_constant_match.group())) 
    # no need to check for string constant because parse_line handles that separately
    return Identifier(text)

SPLIT_PATTERN = "|".join("({})".format(re.escape(_)) for _ in {" "}.union(set(Symbol.elements)))
def parse_line(line: str) -> Iterator[Token]:
    for quoted in re.split(r'(".*")', line):
        if quoted.startswith('"'):
            yield StringConstant(quoted)
        else:
            yield from map(dispatch, (_ for _ in re.split(SPLIT_PATTERN, quoted) if _ and _ != " "))

Token.parse_line = staticmethod(parse_line)
Token.START = Delimiter("tokens")
Token.STOP  = Delimiter("/tokens")