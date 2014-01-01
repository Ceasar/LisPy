from synthesis import Environment



def do_if(environment, test, consequence, alternative):
    result = (consequence if test.evaluate(environment) else alternative)
    return result.evaluate(environment)

def do_define(environment, name, value):
    try:
        environment[name.operator] = lambda *args: (
            value.evaluate(Environment(name.operands, args, environment)))
    except AttributeError:
        environment[name] = value.evaluate(environment)

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
    def __init__(self, name):
        self.name = name

    def evaluate(self, environment=None):
        if environment is None:
            environment = Environment()
        try:
            return environment.find(self.name)[self.name]
        except NameError:
            try:
                return int(self.name)
            except NameError:
                return float(self.name)

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
            return BUILTINS[self.operator.name](environment, *self.operands)
        except KeyError:
            procedure = self.operator.evaluate(environment)
            arguments = (operand.evaluate(environment) for operand in self.operands)
            return procedure(*arguments)
