from typing import Iterator

from commons.stream import Stream
from .tokens import *

""" set of mutually recursive functions implementing Jack grammar rules """ 

def parse_jack_class(stream: Iterator[Token]) -> Token:
    return class_(Stream(stream))

def class_(stream: Stream[Token]) -> Token:
    node = Class() + stream.next(3) # class <name> {
    while stream.peek() in {"static", "field"}:
        node += class_var_dec(stream)
    while stream.peek() != "}":
        node += subroutine_dec(stream)
    return node + stream.next()

def class_var_dec(stream: Stream[Token]) -> Token:
    node = ClassVarDec() + stream.next(3) # (static/field) <type> <varname>
    while stream.peek() != ";": 
        node += stream.next()
    return node + stream.next()

def subroutine_dec(stream: Stream[Token]) -> Token:
    node = SubroutineDec()
    while stream.peek() != "(":
        node += stream.next() # <fn type> <return type> <fn name>
    return node + (stream.next(), parameter_list(stream), stream.next(), subroutine_body(stream)) # <param list> ) { body }

def parameter_list(stream: Stream[Token]) -> Token:
    node = ParameterList()
    while stream.peek() != ")":
        node += stream.next()
    return node 

def subroutine_body(stream: Stream[Token]) -> Token:
    node = SubroutineBody() + stream.next() # {
    while stream.peek() == Keyword("var"):
        node += var_dec(stream)
    return node + (statements(stream), stream.next()) # <statements> }

def var_dec(stream: Stream[Token]) -> Token:
    node = VarDec() + stream.next(3) # var <type> <name>
    while stream.peek() != ";":
        node += (stream.next(), stream.next()) # , <varname> 
    return node + stream.next() # ";"

def statements(stream: Stream[Token]) -> Token:
    node = Statements()
    while stream.peek() != "}": 
        node += statement(stream)
    return node

def statement(stream: Stream[Token]) -> Token:
    return {
        "do"    : do,
        "if"    : if_,
        "let"   : let,
        "while" : while_,
        "return": return_
    }[stream.peek()](stream)

def do(stream: Stream[Token]) -> Token:  # do <term> ; 
    return Do() + (stream.next(), *term(stream), stream.next()) 

def let(stream: Stream[Token]) -> Token: # let <var> ([expr])? = expr ; 
    node = Let() + stream.next(2) 
    if stream.peek() == "[":
        node += (stream.next(), expression(stream), stream.next())
    return node + (stream.next(), expression(stream), stream.next())

def while_(stream: Stream[Token]) -> Token:
    return While((*stream.next(2), expression(stream), *stream.next(2), statements(stream), stream.next()))

def return_(stream: Stream[Token]) -> Token:
    node = Return() + stream.next()
    if stream.peek() != ";":
        node += expression(stream)
    return node + stream.next()
        
def if_(stream: Stream[Token]) -> Token:
    node = If() + (*stream.next(2), expression(stream), *stream.next(2), statements(stream), stream.next())
    if stream.peek() == "else":
        node += (*stream.next(2), statements(stream), stream.next())
    return node 

def expression(stream: Stream[Token]) -> Token: # term (op term)*
    node = Expression() + term(stream) 
    if stream.peek() in {*"=+-*/&|<>"}:
        node += (stream.next(), term(stream))
    return node 

def expression_list(stream: Stream[Token]) -> Token:
    node = ExpressionList()
    while stream.peek() != ")":
        node += stream.next() if stream.peek() == "," else expression(stream)
    return node

def term(stream: Stream[Token]) -> Token:
    token = stream.next()
    node = Term() + token
    if isinstance(token, Identifier):
        token = stream.peek()
        if   token == "[": # array entry
            node +=  (stream.next(), expression(stream), stream.next())       # [ expr ]
        elif token == "(": # subroutine call
            node +=  (stream.next(), expression_list(stream), stream.next())  # ( exprlist )
        elif token == ".": # qualified subroutine call 
            node += (*stream.next(3), expression_list(stream), stream.next()) # . <identifier> ( exprlist )
    elif token == "(":
        node += (expression(stream), stream.next()) # ( expr )
    elif token == "-" or token == "~": # unary operator
        node += term(stream)
    return node
