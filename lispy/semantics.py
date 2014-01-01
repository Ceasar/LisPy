from synthesis import Environment


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

    def get_arguments(self, environment):
        return (operand.evaluate(environment) for operand in self.operands)

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

        # conditional
        if self.operator == "if":
            test, conseq, alt = self.operands
            result = (conseq if test.evaluate(environment) else alt)
            return result.evaluate(environment)
        # definition
        elif self.operator == "define" or self.operator == "set!":
            name, value = self.operands
            environment[name.value] = value.evaluate(environment)
        # procedure
        elif self.operator == "\\":
            (_, vars, self) = self
            eoperands = self.operands
            return lambda *eoperands: self.evaluate(self, Environment(vars, self.operands, environment))
        # sequencing
        elif self.operator == "begin":
            for expr in self.operands:
                val = expr.evaluate(environment)
            return val
        # quotation
        elif self.operator == "quote":
            return self.operands
        # procedure call
        else:
            procedure = self.operator.evaluate(environment)
            return procedure(*self.get_arguments(environment))
