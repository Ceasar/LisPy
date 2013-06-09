import logging
import operator as op

# TODO: If we are super lazy about evaluation and stored function needs to be
# called with what arguments, we can figure out what to memoize

Symbol = str


class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        logging.info("new dict", parms, args)
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


GLOBAL_ENV = Env()
GLOBAL_ENV.update(
    {'+': op.add,
     '-': op.sub,
     '*': op.mul,
     '/': op.div,
     'not': op.not_,
     '>': op.gt,
     '<': op.lt,
     '>=': op.ge,
     '<=': op.le,
     '==': op.eq,
     '/=': op.ne,
     'eq?': op.is_,
     'length': len,
     ':': lambda x, y: [x] + y,
     'head': lambda x: x[0],
     'tail': lambda x: x[1:],
     'append': op.add,
     'list': lambda *x: list(x),
     'list?': lambda x: isinstance(x, list),
     'null?': lambda x: x == [],
     'symbol?': lambda x: isinstance(x, Symbol),
     'map': lambda f, xs: [f(x) for x in xs],
     }
)


def lex(s):
    """
    Parse tokens from a string.

    A token is either a parenthesis or a string.

    >>> list(lex("(:= x 1)"))
    ['(', ':=', 'x', 1, ')']
    >>> list(lex("(do (:= x 1) x)"))
    ['(', 'do', '(', ':=', 'x', 1, ')', 'x', ')']
    >>> list(lex("(if (== 0 0) 1 2)"))
    ['(', 'if', '(', '==', 0, 0, ')', 1, 2, ')']
    """
    tokens = s.replace('(', ' ( ').replace(')', ' ) ').split()

    # Numbers become numbers; every other token is a symbol.
    for token in tokens:
        try:
            yield int(token)
        except ValueError:
            try:
                yield float(token)
            except ValueError:
                yield token


def parse(tokens):
    """"
    Read an expression from a sequence of tokens.

    >>> parse(iter([1]))
    1
    >>> parse(iter(['(', ':=', 'x', 1, ')']))
    [':=', 'x', 1]
    >>> parse(iter(['(', 'do', '(', ':=', 'x', 1, ')', 'x', ')']))
    ['do', [':=', 'x', 1], 'x']
    >>> parse(iter(['(', 'if', '(', '==', 0, 0, ')', 1, 2, ')']))
    ['if', ['==', 0, 0], 1, 2]
    """
    def scan(tokens):
        for token in tokens:
            if token == '(':
                yield list(scan(tokens))
            elif token == ')':
                break
            else:
                yield token
    return next(scan(tokens))


def eval(exp, env=GLOBAL_ENV):
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
    if __debug__:
        if env == GLOBAL_ENV:
            logging.info("eval", exp)
        else:
            logging.info("eval", exp, env)

    # variable reference
    if isinstance(exp, Symbol):
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
            logging.info("running func", vars, exp)
            return lambda *args: eval(exp, Env(vars, args, env))
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


def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    return ("[%s]" % ','.join(map(to_string, exp))
            if isinstance(exp, list) else str(exp))


def run(program):
    return eval(parse(lex(program)))


def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = run(raw_input(prompt))
        if val is not None:
            print to_string(val)


if __name__ == "__main__":
    import doctest
    import sys

    doctest.testmod()

    if len(sys.argv) == 1:
        repl()
    else:
        with open(sys.argv[1]) as f:
            print run(f.read())
