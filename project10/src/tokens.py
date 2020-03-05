import re
from typing import Iterator

ESCAPE_GLYPHS = {"<" : "&lt;", ">" : "&gt;", "&" : "&amp;"}

class Token: 
    """ node in a parse tree """
    def __init__(self, value: str = ""):
        self.text     = value
        self.children = []
        self.nodetype = self.get_nodetype()

    def __eq__(self, other):
        if isinstance(other, str):
            return self.text == other 
        return self.nodetype == other.nodetype and self.text == other.text

    def __hash__(self):
        return self.text.__hash__()

    @classmethod
    def get_nodetype(cls) -> str:
        return cls.__name__[0].lower() + cls.__name__[1:]

    def __iter__(self):
        return iter(self.children)

    def __str__(self):
        return "\n".join(self.render())

    def __repr__(self):
        return "<{}> {} </{}>".format(self.nodetype, self.text if self.text else "[{}]".format(len(self.children)), self.nodetype)

    def render(self, indent_level: int = 0) -> Iterator[str]:
        indent = "  " * indent_level
        if self.children or not self.text:
            yield "{}<{}>".format(indent, self.nodetype)
            for child in self.children:
                yield from child.render(indent_level + 1)
            yield "{}</{}>".format(indent, self.nodetype)
        elif self.text:
            yield "{}<{}> {} </{}>".format(indent, self.nodetype, ESCAPE_GLYPHS.get(self.text, self.text), self.nodetype)

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
    @classmethod
    def get_nodetype(cls) -> str:
        return super(Statement, cls).get_nodetype() + "Statement"

# lexical and grammatical elements
class Symbol          (Token): elements = {*"{}()[].,;+-*/&=|<>~"}
class Keyword         (Token): elements = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null",  "this", "let", "do", "if", "else", "while", "return"}
class StringConstant  (Token): pattern  = re.compile("^\"(.*)\"$")
class IntegerConstant (Token): pattern  = re.compile("^\d+$")
class Identifier      (Token): ...
class Term            (Token): ...
class Type            (Token): ...
class Class           (Token): ...
class VarDec          (Token): ...
class Expression      (Token): ...
class Statements      (Token): ...
class ClassVarDec     (Token): ...
class ParameterList   (Token): ...
class SubroutineDec   (Token): ...
class SubroutineBody  (Token): ...
class ExpressionList  (Token): ...
class Do          (Statement): ...
class If          (Statement): ...
class Let         (Statement): ...
class While       (Statement): ...
class Return      (Statement): ...


SPLIT_PATTERN = "|".join("({})".format(re.escape(_)) for _ in {" "}.union(set(Symbol.elements)))

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

def parse_line(line: str) -> Iterator[Token]:
    # handle quotes with special pattern since they contain spaces and symbols
    for quoted in re.split(r'(".*")', line):
        if quoted.startswith('"'):
            yield StringConstant(quoted.replace('"', ''))
        else:
            yield from map(dispatch, (_ for _ in re.split(SPLIT_PATTERN, quoted) if _ and _ != " "))

Token.parse_line = staticmethod(parse_line)
