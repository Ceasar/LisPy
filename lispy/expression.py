from context import Context
from semantics import BUILTINS


class Atom(object):
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        try:
            return int(self.name)
        except ValueError:
            try:
                return float(self.name)
            except ValueError:
                return context.find(self.name)[self.name]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)


class Combination(object):
    def __init__(self, elements):
        self.elements = elements

    @property
    def operator(self):
        return self.elements[0]

    @property
    def operands(self):
        return self.elements[1:]

    def __str__(self):
        return "(%s)" % " ".join(str(e) for e in self.elements)

    def __repr__(self):
        return str(self)

    def evaluate(self, context):
        if len(self.elements) == 0:
            return []
        try:
            return BUILTINS[self.operator.name](context, *self.operands)
        except KeyError:
            procedure = self.operator.evaluate(context)
            arguments = (operand.evaluate(context) for operand in self.operands)
            return procedure(*arguments)
