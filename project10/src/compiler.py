from itertools import chain
from typing import Iterator, Tuple

from tokens import *

EOL = Symbol(";")

def push_back(token: Token, stream: Iterator[Token]) -> Iterator[Token]:
    return chain([token], stream)

def compile_jack(stream: Iterator[Token]) -> Token:
    node = compile_class(stream)
    return node 

def compile_class(stream: Iterator[Token]) -> Token:
    node = Class()
    node.append(next(stream)) # class keyword
    node.append(next(stream)) # class name 
    node.append(next(stream)) # opening bracket
    lookahead = next(stream)
    while lookahead.text.strip() in {"static", "field"}:
        child, stream = compile_class_var_dec(push_back(lookahead, stream))
        node.append(child)
        lookahead = next(stream)
    while lookahead != Symbol("}"):
        child, stream = compile_subroutine_dec(push_back(lookahead, stream))
        node.append(child)
        lookahead = next(stream)
    node.append(lookahead)
    return node 

def compile_class_var_dec(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = ClassVarDec()
    token = next(stream)
    if token.text.strip() in {"static", "field"}:
        node.append(token)
    node.append(next(stream)) # type 
    node.append(next(stream)) # varname 
    lookahead = next(stream)
    while lookahead != Symbol(";"):
        #node, lookahead = node + (lookahead, next(stream)), next(stream)
        if lookahead == Symbol(","):
            node.append(lookahead)
        node.append(next(stream))
        lookahead = next(stream)
    node.append(lookahead)
    return (node, stream)

def compile_subroutine_dec(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = SubroutineDec()
    token = next(stream)
    while token != Symbol("("):
        node.append(token)
        token = next(stream)
    node.append(token)
    child, stream = compile_parameter_list(stream)
    node.append(child)
    node.append(next(stream)) # closing paren 
    child, stream = compile_subroutine_body(stream)
    node.append(child)
    return (node, stream) 

def compile_parameter_list(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = ParameterList()
    lookahead = next(stream)
    while lookahead != Symbol(")"):
        node.append(lookahead)
        lookahead = next(stream)
    return (node, push_back(lookahead, stream))

def compile_subroutine_body(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = SubroutineBody() 
    node.append(next(stream)) # opening bracket 
    lookahead = next(stream)
    while lookahead == Keyword("var"):
        child, stream = compile_var_dec(push_back(lookahead, stream))
        node.append(child)
        lookahead = next(stream)
    stream = push_back(lookahead, stream)
    child, stream = compile_statements(stream)
    node.append(child)
    node.append(next(stream)) # closing bracket
    return (node, stream)

def compile_var_dec(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = VarDec()
    node.append(next(stream)) # var keyword
    node.append(next(stream)) # type 
    node.append(next(stream)) # varName 
    lookahead = next(stream)
    while lookahead != Symbol(";"):
        node.append(lookahead)    # comma 
        node.append(next(stream)) # varname 
        lookahead = next(stream)
    node.append(lookahead)
    return (node, stream)

def compile_statements(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = Statements()
    lookahead = next(stream)
    while lookahead != Symbol("}"):
        child, stream = compile_statement(push_back(lookahead, stream))
        node.append(child)
        lookahead = next(stream)
    # while stream.peek() != EOB: 
    #     node += compile_statement(stream)
    # return node
    return (node, push_back(lookahead, stream))

def compile_statement(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    keyword = next(stream)
    return { 
        "if"    : compile_if,
        "do"    : compile_do,
        "let"   : compile_let,
        "while" : compile_while,
        "return": compile_return,
    }[keyword.text.strip()](push_back(keyword, stream))

def compile_do(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = Do()
    node.append(next(stream)) # do keyword
    child, stream = compile_term(stream) # function call
    for grandchild in child: # for grandchild in child.children()
        node.append(grandchild)
    node.append(next(stream)) # EOL
    return (node, stream)

def compile_let(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = Let()
    node.append(next(stream)) # let keyword
    node.append(next(stream)) # var name 
    lookahead = next(stream)
    if lookahead == Symbol("["):
        node.append(lookahead) # opening bracket
        child, stream = compile_expression(stream)
        node.append(child)
        node.append(next(stream)) # closing bracket
    else: 
        stream = push_back(lookahead, stream)
    node.append(next(stream)) # equal sign 
    child, stream = compile_expression(stream)
    node.append(child)
    node.append(next(stream)) # EOL
    return (node, stream)

def compile_while(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = While()
    node.append(next(stream)) # while keyword 
    node.append(next(stream)) # opening parens 
    child, stream = compile_expression(stream)
    node.append(child)
    node.append(next(stream)) # closing parens 
    node.append(next(stream)) # opening bracket
    child, stream = compile_statements(stream) 
    node.append(child)
    node.append(next(stream)) # closing bracket
    return (node, stream)

    # return While() + (
    #     stream << (
    #         next, next, compile_expression, next, next, compile_statements, next
    #     )
    # )

def compile_return(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = Return()
    node.append(next(stream)) # return keyword 
    current = next(stream)
    if current == EOL: # bare return 
        node.append(current)
    else: 
        child, stream = compile_expression(push_back(current, stream))
        node.append(child)
        node.append(next(stream)) # semicolon
    return (node, stream)

    # node = Return() + next(stream)
    # if stream.peak() == EOL:
    #    return node + next(stream)
    # return node + compile_expression(stream) + next(stream)
        
def compile_if(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = If()
    node.append(next(stream)) # if keyword 
    node.append(next(stream)) # opening parens 
    child, stream = compile_expression(stream)
    node.append(child)
    node.append(next(stream)) # closing parens 
    node.append(next(stream)) # opening bracket
    child, stream = compile_statements(stream) 
    node.append(child)
    node.append(next(stream)) # closing bracket

    lookahead = next(stream) # check to see for else clause
    if lookahead.text == " else ":
        node.append(lookahead) # else keyword
        node.append(next(stream)) # opening bracket
        child, stream = compile_statements(stream) 
        node.append(child)
        node.append(next(stream)) # closing bracket
    else: 
        stream = push_back(lookahead, stream)
    return (node, stream)

def compile_expression(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = Expression()
    child, stream = compile_term(stream)
    node.append(child)
    current = next(stream)
    if current.tag == "symbol" and current.text.strip() in {*"=+-*/&|<>"}:
        node.append(current)
        child, stream = compile_term(stream)
        node.append(child)
        return (node, stream)
    else: 
        return (node, push_back(current, stream))

def compile_expression_list(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = ExpressionList()
    lookahead = next(stream)
    while lookahead != Symbol(")"):
        if lookahead == Symbol(","):
            node.append(lookahead)
        else:
            child, stream = compile_expression(push_back(lookahead, stream))
            node.append(child)
        lookahead = next(stream)

    return (node, push_back(lookahead, stream))

def compile_term(stream: Iterator[Token]) -> Tuple[Token, Iterator[Token]]:
    node = Term()
    token = next(stream)
    if token.tag == "identifier":
        node.append(token)
        lookahead = next(stream)
        if lookahead == Symbol("["): # array entry
            node.append(lookahead)
            child, stream = compile_expression(stream)
            node.append(child)
            node.append(next(stream)) # should be Symbol("]")
        elif lookahead == Symbol("("): # subroutine call
            node.append(lookahead)
            child, stream = compile_expression_list(stream)
            node.append(child)
            node.append(next(stream)) # closing bracket
        elif lookahead == Symbol("."): # qualified subroutine call 
            node.append(lookahead) 
            node.append(next(stream)) # identifier 
            node.append(next(stream)) # opening bracket 
            child, stream = compile_expression_list(stream) 
            node.append(child)
            node.append(next(stream)) # closing bracket 
        else:
            stream = push_back(lookahead, stream)
    elif token == Symbol("("):
        node.append(token)
        child, stream = compile_expression(stream)
        node.append(child)
        node.append(next(stream)) # must be a ")"
    elif token == Symbol("-") or token == Symbol("~"):
        node.append(token)
        child, stream = compile_term(stream)
        node.append(child)
    elif (
        (token.tag in {"integerConstant", "stringConstant"}) or 
        (token.tag == "keyword" and token.text.strip() in {"true", "false", "null", "this"})
    ):
        node.append(token)
    return (node, stream) 
