from collections import Counter, deque

from .tokens import *

class Scope():
    def __init__(self, name):
        self.name    = name 
        self.counts  = Counter()
        self.entries = dict()

    def __contains__(self, identifier):
        return identifier in self.entries
    
    def __getitem__(self, identifier):
        return self.entries[identifier]

    def __setitem__(self, identifier, type_kind):
        vartype, kind = type_kind
        self.entries[identifier] = (vartype, kind, self.counts[kind])
        self.counts[kind] += 1
        
    def __repr__(self):
        return "Scope({}){}".format(self.name, self.entries)

class SymbolTable():
    def __init__(self):
        self.scopes = deque()
    
    def __contains__(self, identifier):
        return any(identifier in scope for scope in self.scopes)
    
    def __getitem__(self, identifier):
        try:
            return next(scope[identifier] for scope in self.scopes if identifier in scope)
        except StopIteration:
            raise KeyError(identifier)
    
    def __setitem__(self, identifier, type_kind):
        self.scopes[0][identifier] = type_kind

    def __repr__(self):
        return self.scopes.__repr__()

    # use left push/pop to simplify __getitem__; deque access is O(1) at either end
    def push(self, scope_name):
        self.scopes.appendleft(Scope(scope_name))

    def pop(self):
        return self.scopes.popleft() 

    def update(self, tokens: Token):
        if isinstance(token, Class):
            self.push(Scope(children[1].text))
            for child in token.children:
                self.update(child)
        elif isinstance(token, ClassVarDec):
            kind, vartype = token.children[:2]
            for identifier in [t for t in token.children[2:] if isinstance(t, Identifier)]:
                self[identifier] = (vartype, kind)
        elif isinstance(token, SubroutineDec): 
            pass
        elif isinstance(token, VarDec):
            pass 
        elif isinstance(token, ParameterList):
            pass 
        else: 
            pass 

    @staticmethod
    def populate_from(parse_tree: Token):
        table = SymbolTable()
        table.update(parse_tree)
        return table