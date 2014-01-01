"""
Tool for evaluating an abstract syntax tree.

The synthesis part constructs the desired target program from the intermediate
representation and the information in the symbol table.
"""

# TODO: If we are super lazy about evaluation and stored function needs to be
# called with what arguments, we can figure out what to memoize


class Environment(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        if var in self:
            return self
        else:
            if self.outer:
                return self.outer.find(var)
            else:
                raise NameError("name '%s' is not defined" % var)


def evaluate(exp, env=None):
    """
    Evaluate a program.

    >>> evaluate(1)
    1
    >>> evaluate(['define 'x', 1])
    >>> evaluate(['do', ['define 'x', 1], 'x'])
    1
    >>> evaluate(['if', ['==', 0, 0], 1, 2])
    1
    >>> evaluate(['if', ['==', 0, 1], 1, 2])
    2
    """
    if env is None:
        env = Environment()

    # variable reference
    if isinstance(exp, str):
        return [] if exp == "[]" else env.find(exp)[exp]
    # constant literal
    elif not isinstance(exp, list):
        return exp
    else:
        operator, args = exp[0], exp[1:]
        # conditional
        if operator == "if":
            test, conseq, alt = args
            return evaluate(conseq if evaluate(test, env) else alt, env)
        # definition
        elif operator == "define":
            variable, expression = args
            env[variable] = evaluate(expression, env)
        elif operator == "set!":
            variable, expression = args
            env[variable] = evaluate(expression, env)
        # procedure
        elif operator == "\\":
            (_, vars, exp) = exp
            return lambda *args: evaluate(exp, Environment(vars, args, env))
        # sequencing
        elif operator == "do":
            for expr in args:
                val = evaluate(expr, env)
            return val
        # quotation
        elif operator == "quote":
            return args
        elif operator == "begin":
            e = None
            for arg in args:
                e = evaluate(arg, env)
            return e
        # procedure call
        else:
            f = evaluate(operator, env)
            xargs = list(evaluate(arg, env) for arg in args)
            return f(*xargs)
