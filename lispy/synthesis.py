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


def eval(exp, env):
    """
    Evaluate a program.

    >>> eval(1)
    1
    >>> eval([':=', 'x', 1])
    >>> eval(['do', [':=', 'x', 1], 'x'])
    1
    >>> eval(['if', ['==', 0, 0], 1, 2])
    1
    >>> eval(['if', ['==', 0, 1], 1, 2])
    2
    """
    # variable reference
    if isinstance(exp, str):
        return [] if exp == "[]" else env.find(exp)[exp]
    # constant literal
    elif not isinstance(exp, list):
        return exp
    else:
        keyword, args = exp[0], exp[1:]
        # conditional
        if keyword == "if":
            test, conseq, alt = args
            return eval(conseq if eval(test, env) else alt, env)
        # definition
        elif keyword == ":=":
            var, expr = args
            env[var] = eval(expr, env)
        # procedure
        elif keyword == "\\":
            (_, vars, exp) = exp
            return lambda *args: eval(exp, Environment(vars, args, env))
        # sequencing
        elif keyword == "do":
            for expr in args:
                val = eval(expr, env)
            return val
        # quotation
        elif keyword == "quote":
            return args
        # procedure call
        else:
            f = eval(keyword, env)
            xargs = list(eval(arg, env) for arg in args)
            return f(*xargs)
