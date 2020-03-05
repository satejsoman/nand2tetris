from typing import Iterator

from stream import Stream
from tokens import *


def compile_jack(stream: Iterator[Token]) -> Token:
    return compile_class(Stream(stream))

def compile_class(stream: Stream[Token]) -> Token:
    node = Class() + stream.next(3) # class <name> {
    while stream.peek() in {"static", "field"}:
        node += compile_class_var_dec(stream)
    while stream.peek() != "}":
        node += compile_subroutine_dec(stream)
    return node + stream.next()

def compile_class_var_dec(stream: Stream[Token]) -> Token:
    node = ClassVarDec() + stream.next(3) # (static/field) <type> <varname>
    while stream.peek() != ";": 
        node += stream.next()
    return node + stream.next()

def compile_subroutine_dec(stream: Stream[Token]) -> Token:
    node = SubroutineDec()
    while stream.peek() != "(":
        node += stream.next() # <fn type> <return type> <fn name>
    return node + (stream.next(), compile_parameter_list(stream), stream.next(), compile_subroutine_body(stream)) # <param list> ) { body }

def compile_parameter_list(stream: Stream[Token]) -> Token:
    node = ParameterList()
    while stream.peek() != ")":
        node += stream.next()
    return node 

def compile_subroutine_body(stream: Stream[Token]) -> Token:
    node = SubroutineBody() + stream.next() # {
    while stream.peek() == Keyword("var"):
        node += compile_var_dec(stream)
    return node + (compile_statements(stream), stream.next()) # <statements> }

def compile_var_dec(stream: Stream[Token]) -> Token:
    node = VarDec() + stream.next(3) # var <type> <name>
    while stream.peek() != ";":
        node += (stream.next(), stream.next()) # , <varname> 
    return node + stream.next() # ";"

def compile_statements(stream: Stream[Token]) -> Token:
    node = Statements()
    while stream.peek() != "}": 
        node += compile_statement(stream)
    return node

def compile_statement(stream: Stream[Token]) -> Token:
    return { 
        "if"    : compile_if,
        "do"    : compile_do,
        "let"   : compile_let,
        "while" : compile_while,
        "return": compile_return,
    }[stream.peek()](stream)

def compile_do(stream: Stream[Token]) -> Token:
    node = Do() + stream.next() # do keyword 
    for subnode in compile_term(stream): # pull in inner node from Term node 
        node += subnode
    return node + stream.next() # ";"

def compile_let(stream: Stream[Token]) -> Token:
    node = Let() + stream.next(2) # let <varname>
    if stream.peek() == "[": # array index 
        node += (stream.next(), compile_expression(stream), stream.next()) # [ expr ]
    return node + (stream.next(), compile_expression(stream), stream.next()) # = expresstion ; 

def compile_while(stream: Stream[Token]) -> Token:
    return While() + (
        *stream.next(2), compile_expression(stream), *stream.next(2), # while ( expr ) {
        compile_statements(stream), stream.next())                    # statements }

def compile_return(stream: Stream[Token]) -> Token:
    node = Return() + stream.next()
    if stream.peek() == ";": # bare return
       return node + stream.next()
    return node + (compile_expression(stream), stream.next())
        
def compile_if(stream: Stream[Token]) -> Token:
    node = If() + (
        *stream.next(2), compile_expression(stream), *stream.next(2), # if ( expr ) {
        compile_statements(stream), stream.next())                    # statements }
    if stream.peek().text == "else":
        node += (stream.next(2) + (compile_statements(stream), stream.next())) # else { statements }
    return node

def compile_expression(stream: Stream[Token]) -> Token:
    node = Expression() + compile_term(stream)
    if stream.peek() in {*"=+-*/&|<>"}: # handle binary op
        return node + (stream.next(), compile_term(stream))
    return node

def compile_expression_list(stream: Stream[Token]) -> Token:
    node = ExpressionList()
    while stream.peek() != ")":
        if stream.peek() == ",":
            node += stream.next()
        else: 
            node += compile_expression(stream)
    return node

def compile_term(stream: Stream[Token]) -> Token:
    node = Term()
    token = stream.peek()
    if isinstance(token, Identifier):
        node += stream.next()
        token = stream.peek()
        if   token == "[": # array entry
            node += (stream.next(), compile_expression(stream), stream.next()) # [ expr ]
        elif token == "(": # subroutine call
            node += (stream.next(), compile_expression_list(stream), stream.next()) # ( exprlist )
        elif token == ".": # qualified subroutine call 
            node += stream.next(3) + (compile_expression_list(stream), stream.next()) # . <identifier> ( exprlist )
    elif token == "(":
        node += (stream.next(), compile_expression(stream), stream.next()) # ( expr )
    elif token == "-" or token == "~": # unary operator
        node += (stream.next(), compile_term(stream))
    elif (isinstance(token, (IntegerConstant, StringConstant)) or 
         (isinstance(token, Keyword) and token in {"true", "false", "null", "this"})):
        node += stream.next()
    return node
