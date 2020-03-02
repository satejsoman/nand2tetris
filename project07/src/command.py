from typing import List, Iterator

STATIC = "STATIC"
JUMPNO = "JUMPNO"

load   = ["@SP", "A=M-1"]
unload = ["@SP", "M=M-1"]

class Logical:
    def translate(self) -> List[str]:
        return (
            load                            + 
            ["D=M", "A=A-1", self.op]       + 
            (["M=D"] if self.write else []) +
            unload
        )

class Negate:
    def translate(self) -> List[str]:
        return load + [self.op] 

class Comparison:
    def translate(self) -> List[str]:
        return (
            load + [
                "D=M",
                "A=A-1",
                "D=M-D",
                "@IF_JUMPNO",
                "D;" + self.op
            ] + load + [
                "A=A-1",
                "M=0",
                "@ELSE_JUMPNO",
                "0;JMP",
                "(IF_JUMPNO)"
            ] + load + [
                "A=A-1",
                "M=-1",
                "(ELSE_JUMPNO)"
            ] + unload
        )

class Add(Logical):   op, write = "D=D+M", True
class Sub(Logical):   op, write = "D=M-D", True
class And(Logical):   op, write = "M=D&M", False
class Or(Logical):    op, write = "M=D|M", False 
class Not(Negate):    op = "M=!M"
class Neg(Negate):    op = "M=-M"
class Eq(Comparison): op = "JEQ" 
class Gt(Comparison): op = "JGT"
class Lt(Comparison): op = "JLT"

class MemoryAccess:
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
    
    @staticmethod
    def to_dest(dest: str) -> List[str]:
        return [
            # store appropriate value
            "D=" + dest, "@SP", "A=M", "M=D",
            # increment stack pointer 
            "@SP", "M=M+1"
        ]

    def translate(self) -> List[str]:
        # resolve registers based on standard mapping
        if self.segment in MemoryAccess.registers.keys(): 
            register, dest = MemoryAccess.registers[self.segment]
            return [
                "@"    + str(self.index),
                "D=A",
                "@"    + register,
                "A=D+" + dest
            ] + Push.to_dest("M")
        else: 
            label, dest = ("@", "A") if self.segment == "constant" else ("@STATIC.", "M")
            return [label + str(self.index)] + Push.to_dest(dest)

class Pop(MemoryAccess):
    # from page 103, the pop command is implemented by first decrementing
    # sp and then returning the value stored in the top positions

    def translate(self) -> List[str]:
        # load offset 
        commands = ["@" + self.index, "D=A"]

        # resolve segments based on standard mapping 
        if self.segment in MemoryAccess.registers.keys(): 
            register, dest = MemoryAccess.registers[self.segment]
            commands += [
                "@"     + register,
                "D=D+"  + dest,
                "@13",
                "M=D" ] + load + [
                "D=M",
                "@13",
                "A=M"
            ]
        else: # segment must be static since we can't pop a constant 
            commands += load + ["D=M", "@STATIC." + str(self.index)]

        # write to address and decrement stack pointer 
        return commands + ["M=D"] + unload

class Translator():
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
    def __init__(self, filename: str):
        self.filename = filename 
        self.jumpcount = 0

    def translate(self, line: str) -> Iterator[str]:
        yield "// " + line # commented out line to translate, as suggested by N+S

        cmd, *args = line.split()
        for template in Translator.constuctors[cmd](*args).translate():
            if STATIC in template:
                template = template.replace(STATIC, self.filename)
            if JUMPNO in template:
                template = template.replace(JUMPNO, str(self.jumpcount))
                self.jumpcount += 1
            yield template

        yield "" # empty line 
