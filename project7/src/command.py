from typing import List, Tuple

STATIC = "STATIC"
JUMPNO = "JUMPNO"

class Command():
    load   = ["@SP", "A=M-1"]
    unload = ["@SP", "M=M-1"]

    @staticmethod
    def translate(line: str) -> List[str]:
        cmd, *args = line.split()
        return (
            ["// " + line ] + # commented out line to translate, as suggested by N+S
            constuctors[cmd](*args).translate() + # translation
            [""] # empty line 
        )

class Logical(Command):
    op = ""
    write = False

    def translate(self) -> List[str]:
        return (
            self.load                       + 
            ["D=M", "A=A-1", self.op]       + 
            (["M=D"] if self.write else []) +
            self.unload
        )

class Add(Logical):
    op = "D=D+M"
    write = True 

class Sub(Logical):
    op = "D=M-D"
    write = True 

class And(Logical):
    op = "M=D&M"

class Or(Logical):
    op = "M=D|M"

class Negate(Logical):
    op = ""
    def translate(self) -> List[str]:
        return self.load + [self.op] 

class Not(Negate):
    op = "M=!M"

class Neg(Negate):
    op = "M=-M"

class Comparison(Logical):
    op = ""
    def translate(self) -> List[str]:
        return (
            self.load + [
                "D=M",
                "A=A-1",
                "D=M-D",
                "@IF_JUMPNO",
                "D;" + self.op
            ] + self.load + [
                "A=A-1",
                "M=0",
                "@ELSE_JUMPNO",
                "0;JMP",
                "(IF_JUMPNO)"
            ] + self.load + [
                "A=A-1",
                "M=-1",
                "(ELSE_JUMPNO)"
            ] + self.unload
        )

class Eq(Comparison):
    op = "JEQ" 

class Gt(Comparison):
    op = "JGT"

class Lt(Comparison):
    op = "JLT"

class MemoryAccess(Command):
    registers = {
        "local"   : ("LCL",  "M"),
        "argument": ("ARG",  "M"),
        "this"    : ("THIS", "M"),
        "that"    : ("THAT", "M"),
        "pointer" : ("3",    "A"),
        "temp"    : ("5",    "A")
    }

    def __init__(self, segment, index):
        self.segment = segment
        self.index   = index

class Push(MemoryAccess):
    # from page 103, the push command is implemented by first storing x 
    # at the array entry pointed to by sp and then incrementing sp 
    
    def push(self, dest: str) -> List[str]:
        return [
            # store appropriate value
            "D=" + dest,
            "@SP",
            "A=M",
            "M=D",

            # increment stack pointer 
            "@SP",
            "M=M+1"
        ]

    def translate(self) -> List[str]:
        # resolve registers based on standard mapping
        if self.segment in ("local", "argument", "this", "that", "pointer", "temp"): 
            register, dest = MemoryAccess.registers[self.segment]
            return [
                "@" + str(self.index),
                "D=A",
                "@"    + register,
                "A=D+" + dest
            ] + self.push("M")
        elif self.segment == "constant":
            return ["@" + str(self.index)]        + self.push("A")
        else: #segment == static 
            return ["@STATIC." + str(self.index)] + self.push("M")
        
class Pop(MemoryAccess):
    # from page 103, the pop command is implemented by first decrementing
    # sp and then returning the value stored in the top positions

    def translate(self) -> List[str]:
        # load offset 
        commands = [
            "@" + self.index,
            "D=A"
        ]

        # resolve segments based on standard mapping 
        if self.segment in ("local", "argument", "this", "that", "pointer", "temp"): 
            register, dest = MemoryAccess.registers[self.segment]
            commands += [
                "@"    + register,
                "D=D+" + dest,
                "@13",
                "M=D",
                "@SP",
                "A=M-1",
                "D=M",
                "@13",
                "A=M",
            ]
        else: # segment must be static since we can't pop a constant 
            commands += [
                "@SP",
                "A=M-1",
                "D=M", 
                "@STATIC." + str(self.index)
            ]

        # write to address and decrement stack pointer 
        return commands + [
            "M=D",
            "@SP",
            "M=M-1"
        ]

constuctors = { 
    "add" : Add,
    "sub" : Sub,
    "neg" : Neg,
    "eq"  : Eq,
    "gt"  : Gt, 
    "lt"  : Lt, 
    "and" : And,
    "or"  : Or, 
    "not" : Not, 
    "pop" : Pop, 
    "push": Push 
}
