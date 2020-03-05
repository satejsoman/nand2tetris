from typing import Iterator

from stream import Stream
from tokens import *

""" set of mutually recursive functions implementing Jack grammar rules """ 

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
    return {"if": compile_if, "do": compile_do, "let": compile_let, "while": compile_while, "return": compile_return}[stream.peek()](stream)

def compile_do(stream: Stream[Token]) -> Token:  # do <term> ; 
    return Do() + (stream.next(), *compile_term(stream), stream.next()) 

def compile_let(stream: Stream[Token]) -> Token: # let <var> ([expr])? = expr ; 
    return Let() + stream.next(2) + ((stream.next(), compile_expression(stream), stream.next()) if stream.peek() == "[" else ()) + (stream.next(), compile_expression(stream), stream.next())

def compile_while(stream: Stream[Token]) -> Token:
    return While() + (*stream.next(2), compile_expression(stream), *stream.next(2), compile_statements(stream), stream.next())

def compile_return(stream: Stream[Token]) -> Token:
    return (Return() + stream.next()) + (stream.next() if stream.peek() == ";" else ((compile_expression(stream), stream.next())))
        
def compile_if(stream: Stream[Token]) -> Token:
    node = If() + (*stream.next(2), compile_expression(stream), *stream.next(2), compile_statements(stream), stream.next())
    return node + ((stream.next(2) + (compile_statements(stream), stream.next())) if stream.peek() == "else" else ())

def compile_expression(stream: Stream[Token]) -> Token: # term (op term)*
    return Expression() + compile_term(stream) + ((stream.next(), compile_term(stream)) if stream.peek() in {*"=+-*/&|<>"} else ())

def compile_expression_list(stream: Stream[Token]) -> Token:
    node = ExpressionList()
    while stream.peek() != ")":
        node += stream.next() if stream.peek() == "," else compile_expression(stream)
    return node

def compile_term(stream: Stream[Token]) -> Token:
    token = stream.next()
    node = Term() + token
    if isinstance(token, Identifier):
        token = stream.peek()
        if   token == "[": # array entry
            node +=  (stream.next(), compile_expression(stream), stream.next())       # [ expr ]
        elif token == "(": # subroutine call
            node +=  (stream.next(), compile_expression_list(stream), stream.next())  # ( exprlist )
        elif token == ".": # qualified subroutine call 
            node += (*stream.next(3), compile_expression_list(stream), stream.next()) # . <identifier> ( exprlist )
    elif token == "(":
        node += (compile_expression(stream), stream.next()) # ( expr )
    elif token == "-" or token == "~": # unary operator
        node += compile_term(stream)
    return node
