import re
from typing import Iterator
from xml.etree.ElementTree import Element, tostring

# class Token(Element):
#     """ subclass of XML element to expedite serializing Jack tokens """
#     def __init__(self, val = ""):
#         super().__init__(self.__class__.__name__[0].lower() + self.__class__.__name__[1:])
#         self.text = " {} ".format(val)

#     def __str__(self):
#         return tostring(self).decode("ascii")

#     def __eq__(self, other):
#         return self.tag == other.tag and self.text == other.text

class Token: 
    def __init__(self, value: str = ""):
        self.text     = value
        self.children = []

    def tag(self) -> str:
        return self.__class__.__name__[0].lower() + self.__class__.__name__[1:]

    def __iter__(self):
        return iter(self.children)

    def __str__(self):
        return "\n".join(self.render())

    def __repr__(self):
        tag = self.tag()
        return "<{}> {} </{}>".format(tag, self.text if self.text else "[{}]".format(len(self.children)), tag)

    def render(self, indent_level: int = 0) -> Iterator[str]:
        tag = self.tag()
        indent = "  " * indent_level
        if self.children:
            yield "{}<{}>".format(indent,tag)
            for child in self.children:
                yield from child.render(indent_level + 1)
            yield "{}</{}>".format(indent,tag)
        elif self.text:
            yield "{}<{}> {} </{}>".format(indent, tag, self.text, tag)

    def append(self, other):
        self.children.append(other)

    def __add__(self, other):
        if isinstance(other, Token):
            self.append(other)
        elif isinstance(other, (tuple, list)):
            for elem in other:
                self.append(elem)
        return self

class Statement(Token): 
    def tag(self) -> str:
        return self.__class__.__name__[0].lower() + self.__class__.__name__[1:] + "Statement"

class Symbol          (Token): elements = {*"{}()[].,;+-*/&=|<>~"}
class Keyword         (Token): elements = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null",  "this", "let", "do", "if", "else", "while", "return"}
class StringConstant  (Token): pattern  = re.compile("^\"(.*)\"$")
class IntegerConstant (Token): pattern  = re.compile("^\d+$")
class Identifier      (Token): pass
class Term            (Token): pass
class Type            (Token): pass
class Class           (Token): pass
class VarDec          (Token): pass
class Expression      (Token): pass
class Statements      (Token): pass
class ClassVarDec     (Token): pass
class ParameterList   (Token): pass
class SubroutineDec   (Token): pass
class SubroutineBody  (Token): pass
class ExpressionList  (Token): pass
class Do          (Statement): pass
class If          (Statement): pass
class Let         (Statement): pass
class While       (Statement): pass
class Return      (Statement): pass

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
    # handle quotes with special pattern since they contain spaces and symbols
    for quoted in re.split(r'(".*")', line):
        if quoted.startswith('"'):
            yield StringConstant(quoted.replace('"', ''))
        else:
            yield from map(dispatch, (_ for _ in re.split(SPLIT_PATTERN, quoted) if _ and _ != " "))

Token.parse_line = staticmethod(parse_line)