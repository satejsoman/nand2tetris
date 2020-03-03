import re
from xml.etree.ElementTree import Element, tostring

class TokenSequence():
    pass 

class Class(TokenSequence): pass 
class ClassVarDec(TokenSequence): pass 
class Type(TokenSequence): pass 
class SubroutineDec(TokenSequence): pass 
class ParameterList(TokenSequence): pass 
class SubroutineBody(TokenSequence): pass 
class VarDec(TokenSequence): pass 

class Statement(TokenSequence): pass 
class If(Statement): pass 
class Let(Statement): pass 
class While(Statement): pass 
class Do(Statement): pass 
class Return(Statement): pass 