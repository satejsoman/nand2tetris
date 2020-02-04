import re 
from typing import Dict

# static definitions
AINSTRUCTION_DELIMITER = "@"
CINSTRUCTION_PATTERN   = re.compile(r"((?P<dest>.*)=)?(?P<comp>.{,3})((;(?P<jump>J.*))|$)")
LABEL_DELIMITER        = "("

COMP_VALUES = { 
    # a = 0 values 
    "0"   : "0101010",
    "1"   : "0111111",
    "-1"  : "0111010",
    "D"   : "0001100",
    "A"   : "0110000",
    "!D"  : "0001101",
    "!A"  : "0110001",
    "-D"  : "0001111",
    "-A"  : "0110011",
    "D+1" : "0011111",
    "A+1" : "0110111",
    "D-1" : "0001110",
    "A-1" : "0110010",
    "D+A" : "0000010",
    "D-A" : "0010011",
    "A-D" : "0000111",
    "D&A" : "0000000",
    "D|A" : "0010101",
    # a = 1 values 
    "M"   : "1110000",
    "!M"  : "1110001",
    "-M"  : "1110011",
    "M+1" : "1110111",
    "M-1" : "1110010",
    "D+M" : "1000010",
    "D-M" : "1010011",
    "M-D" : "1000111",
    "D&M" : "1000000",
    "D|M" : "1010101"
}

DEST_VALUES = {
    "NULL": "000",
    "M"   : "001",
    "D"   : "010",
    "MD"  : "011",
    "A"   : "100",
    "AM"  : "101",
    "AD"  : "110",
    "AMD" : "111"
}

JUMP_VALUES = {
    "NULL": "000",
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111"
}

class Instruction:
    """ base class for parsed instructions """
    header = ""

    @staticmethod
    def parse(line: str):
        # dispatch subtype by delimiters 
        if line.startswith(AINSTRUCTION_DELIMITER):
            if line[1:].isnumeric():
                return AInstruction.parse(line)
            else: 
                return Symbol.parse(line)
        elif line.startswith(LABEL_DELIMITER):
            return Label.parse(line)
        return CInstruction.parse(line)

    def body(self) -> str:
        return ""

    def __str__(self) -> str:
        return "{}{}".format(self.header, self.body())

class AInstruction(Instruction):
    header = "0"

    def __init__(self, address: int):
        self.address = address

    @staticmethod
    def parse(line: str) -> Instruction:
        return AInstruction(int(line[1:]))
    
    def body(self) -> str:
        return "{0:015b}".format(self.address)


class CInstruction(Instruction):
    header = "111"
    
    def __init__(self, comp: str, dest: str, jump: str):
        self.comp = comp
        self.dest = dest
        self.jump = jump 

    @staticmethod
    def parse(line: str) -> Instruction:
        match = CINSTRUCTION_PATTERN.match(line)
        if match:
            return CInstruction(match.group("comp"), match.group("dest"), match.group("jump"))
        return CInstruction("", "", "")
    
    def body(self) -> str:
        return "".join(
            table[value if value else "NULL"] 
            for (table, value) 
            in zip((COMP_VALUES, DEST_VALUES, JUMP_VALUES), (self.comp, self.dest, self.jump)))


class PseudoInstruction(Instruction):
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return self.value


class Label(PseudoInstruction):
    @staticmethod
    def parse(line: str) -> Instruction:
        return Label(line[1:-1]) 


class Symbol(PseudoInstruction):
    @staticmethod
    def parse(line: str) -> Instruction:
        return Symbol(line[1:]) 


# Cs = [
#     "D=M",
#     "D;JLE",
#     "M=D",
#     "D=A",
#     "M=D",
#     "A=M",
#     "M=-1",
#     "D=M",
#     "D=D+A",
#     "M=D",
#     "MD=M-1",
#     "D;JGT",
#     "0;JMP"
# ]

# for C in Cs:
#     print(C, "\t", Instruction.parse(C))