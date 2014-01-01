from synthesis import Environment



def do_if(environment, test, consequence, alternative):
    result = (consequence if test.evaluate(environment) else alternative)
    return result.evaluate(environment)

def do_define(environment, name, value):
    environment[name.value] = value.evaluate(environment)

def do_begin(environment, *expressions):
    for expression in expressions:
        value = expression.evaluate(environment)
    return value


BUILTINS = {
    "if": do_if,
    "define": do_define,
    "set!": do_define,
    "begin": do_begin,
}


class Atom(object):
    def __init__(self, value):
        self.value = value

    def evaluate(self, environment=None):
        if environment is None:
            environment = Environment()

        # variable reference
        if isinstance(self.value, str):
            return environment.find(self.value)[self.value]
        # constant literal
        else:
            return self.value

    def __eq__(self, other):
        return self.value == other

    def __str__(self):
        return str(self.value)

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

    @property
    def is_atom(self):
        return len(self.operands) == 0

    def __str__(self):
        return "(%s)" % " ".join(str(e) for e in self.elements)

    def __repr__(self):
        return str(self)

    def evaluate(self, environment=None):
        if environment is None:
            environment = Environment()

        try:
            return BUILTINS[self.operator.value](environment, *self.operands)
        except KeyError:
            procedure = self.operator.evaluate(environment)
            arguments = (operand.evaluate(environment) for operand in self.operands)
            return procedure(*arguments)
