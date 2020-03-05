from tokens import Token
from compiler import *


def apply(fn, line):
    return fn(Token.parse_line(line))

def test_term():
    test1 = "7"
    test2 = "(5 + 6)"
    test3 = "package.func(x1, x2)"

    for test in [test1, test2, test3]:
        out, _ = apply(compile_term, test)
        print(out)

def test_fn_call():
    line = "do Output.println();"
    for t in Token.parse_line(line):
        print(t)
    print()
    print(apply(compile_statement, line)[0])

def test_while():
    line ='while (i < length) {' + 'let a[i] = Keyboard.readInt("ENTER THE NEXT NUMBER: ");' + 'let i = i + 1;' + '}'
    print(apply(compile_statement, line)[0])

test_while()