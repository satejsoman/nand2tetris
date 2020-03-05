from typing import Iterator

class Token: 
    def __init__(self, value: str = ""):
        self.text     = value
        self.children = []

    def tag(self) -> str:
        return self.__class__.__name__[0].lower() + self.__class__.__name__[1:]

    def __iter__(self):
        return iter(self.children)

    def __str__(self):
        return "\n".join(self.render())

    def __repr__(self):
        tag = self.tag()
        return "<{}> {} </{}>".format(tag, self.text if self.text else "[{}]".format(len(self.children)), tag)

    def render(self, indent_level: int = 0) -> Iterator[str]:
        tag = self.tag()
        indent = "  " * indent_level
        if self.children:
            yield "{}<{}>".format(indent,tag)
            for child in self.children:
                yield from child.render(indent_level + 1)
            yield "{}</{}>".format(indent,tag)
        elif self.text:
            yield "{}<{}> {} </{}>".format(indent, tag, self.text, tag)

    def append(self, other):
        self.children.append(other)

    def __add__(self, other):
        if isinstance(other, Token):
            self.append(other)
        elif isinstance(other, (tuple, list)):
            for elem in other:
                self.append(elem)
        return self
