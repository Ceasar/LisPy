import operator as op

from context import Context
from interpreter import interpret


GLOBAL_ENV = Context()
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
     'symbol?': lambda x: isinstance(x, str),
     'map': lambda f, xs: [f(x) for x in xs],
     }
)


def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    return ("[%s]" % ','.join(map(to_string, exp))
            if isinstance(exp, list) else str(exp))


def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        try:
            val = interpret(raw_input(prompt), GLOBAL_ENV)
        except (EOFError, SystemExit):
            break
        except (Exception, KeyboardInterrupt) as e:
            print e
        else:
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
            print interpret(f.read(), GLOBAL_ENV)
