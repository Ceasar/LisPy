from environment import Environment


class Literal(object):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value

    def __repr__(self):
        return "(Literal %s)" % self.value


class Reference(object):
    def __init__(self, name):
        self.name = name

    def eval(self, env):
        return env.find(self.name)

    def __repr__(self):
        return "(Reference %s)" % self.name


class Definition(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def eval(self, env):
        env[self.name] = self.expression.eval(env)

    def __repr__(self):
        return "(Definition %s %s)" % (self.name, self.expression)


# TODO: This is really just a function
class Conditional(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def eval(self, env):
        if self.condition.eval(env):
            return self.conseqeunce.eval(env)
        else:
            return self.alternative.eval(env)

    def __repr__(self):
        return "(If %s %s %s)" % (self.condition, self.consequence, self.alternative)


class Function(object):
    def __init__(self, parameters, expression):
        self.parameters = parameters
        self.expression = expression

    def eval(self, env):
        return lambda *args: self.expression.eval(Environment(self.parameters,
                                                              args, env))


class Sequence(object):
    def __init__(self, *expressions):
        print expressions
        self.expressions = expressions

    def eval(self, env):
        for expression in self.expressions:
            val = expression.eval(env)
        return val

    def __repr__(self):
        return "(Sequence %s)" % (self.expressions,)


class Application(object):
    def __init__(self, function, *args):
        self.function = function
        self.args = args

    def eval(self, env):
        f = self.function.eval(env)
        args = list(arg.eval(env) for arg in self.args)
        return f(*args)
