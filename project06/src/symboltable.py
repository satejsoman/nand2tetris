from typing import Dict

from instruction import Instruction, Label, Symbol


class SymbolTable():
    """ wrapper over a dictionary with convenience methods for adding labels vs symbols """

    def __init__(self):
        self.symbols: Dict[str, int] = {
            "R0"     : 0,
            "R1"     : 1,
            "R2"     : 2,
            "R3"     : 3,
            "R4"     : 4,
            "R5"     : 5,
            "R6"     : 6,
            "R7"     : 7,
            "R8"     : 8,
            "R9"     : 9,
            "R10"    : 10,
            "R11"    : 11,
            "R12"    : 12,
            "R13"    : 13,
            "R14"    : 14,
            "R15"    : 15,
            "SCREEN" : 16384,
            "KBD"    : 24576,
            "SP"     : 0,
            "LCL"    : 1,
            "ARG"    : 2,
            "THIS"   : 3,
            "THAT"   : 4
        }
        self.next_address = 16

    def put_symbol(self, symbol: Symbol):
        self.symbols[symbol.value] = self.next_address
        self.next_address += 1

    def put_label(self, label: Label, address: int):
        self.symbols[label.value] = address

    def __getitem__(self, symbol: Symbol) -> int:
        return self.symbols[symbol.value]

    def __contains__(self, symbol: Symbol) -> bool:
        return symbol.value in self.symbols
