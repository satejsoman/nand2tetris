from collections import ChainMap, Counter, UserDict

from commons.utils import groups_of

from .tokens import *


class Scope(UserDict):
    def __init__(self, name):
        self.name    = name 
        self.counts  = Counter()
        super().__init__(self)

    def __setitem__(self, identifier, type_kind):
        identifier, vartype, kind = (_.text if isinstance(_, Token) else _ for _ in (identifier, *type_kind))
        self.data[identifier] = (vartype, kind, self.counts[kind])
        self.counts[kind] += 1
        
    def __repr__(self):
        return self.data.__repr__()

class SymbolTable():
    def __init__(self):
        self.scopes  = dict()
        self.root    = None
        self.current = None

    def root_context(self, name):
        root_scope        = ChainMap(Scope(name))
        self.root         = root_scope
        self.current      = root_scope
        self.scopes[name] = root_scope

    def new_context(self, name):
        scope             = self.root.new_child(Scope(name))
        self.scopes[name] = scope
        self.current      = scope

    def pop_context(self):
        self.current = self.root # we know there is only 1 level of nesting

    def __setitem__(self, identifier, type_kind):
        self.current.__setitem__(identifier, type_kind)

    def __getitem__(self, identifier):
        self.current.__getitem__(self, identifier)
    
    def __str__(self):
        return "\n".join("{}:{}".format(*kv) for kv in self.scopes.items())

    def update(self, token: Token):
        if isinstance(token, Class):
            self.root_context("class:" + token.children[1].text)
            for child in token.children:
                self.update(child)
        elif isinstance(token, (ClassVarDec, VarDec)):
            kind, vartype, *identifiers = token.children
            for identifier in [i for i in identifiers if isinstance(i, Identifier)]:
                self[identifier] = (vartype, kind)
        elif isinstance(token, SubroutineDec): 
            self.new_context("{}:{}".format(token.children[0].text, token.children[2].text))
            if token.children[0] == "method":
                classname = self.root.maps[-1].name.split(":")[1]
                self["this"] = (classname, "argument")
            # regular function or constructor 
            for child in token.children:
                self.update(child)
            self.pop_context()
        elif isinstance(token, ParameterList):
            for (vartype, identifier, _) in groups_of(token.children, 3):
                self[identifier] = (vartype, "argument")

    @staticmethod
    def populate_from(parse_tree: Token):
        table = SymbolTable()
        table.update(parse_tree)
        return table
