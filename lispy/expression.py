from context import Context


class Atom(object):
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        try:
            return self.name == other.name
        except AttributeError:
            return False

    def __neq__(self, other):
        return not self == other

    def __str__(self):
        return "`%s`" % str(self.name)

    def __repr__(self):
        return str(self)


class Combination(object):
    def __init__(self, elements):
        self._elements = elements

    @property
    def elements(self):
        return self._elements

    @property
    def operator(self):
        return self.elements[0]

    @property
    def operands(self):
        return self.elements[1:]

    def __eq__(self, other):
        try:
            return self.elements == other.elements
        except AttributeError:
            return False

    def __neq__(self, other):
        return not self == other

    def __str__(self):
        return "(%s)" % " ".join(str(e) for e in self.elements)

    def __repr__(self):
        return str(self)
