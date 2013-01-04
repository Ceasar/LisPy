import math
import operator as op


Symbol = str


class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        return self if var in self else self.outer.find(var)


GLOBAL_ENV = Env()
GLOBAL_ENV.update(vars(math))
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
      '=': op.eq,
      'equal?': op.eq,
      'eq?': op.is_,
      'length': len,
      'cons': lambda x, y: [x] + y,
      'car': lambda x: x[0],
      'cdr': lambda x: x[1:],
      'append': op.add,
      'list': lambda *x: list(x),
      'list?': lambda x: isinstance(x, list),
      'null?': lambda x: x == [],
      'symbol?': lambda x: isinstance(x, Symbol)
      }
)


def parse(s):
    "Read a Scheme expression from a string."
    tokens = s.replace('(', ' ( ').replace(')', ' ) ').split()
    return _read_from(tokens)


def _read_from(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(_read_from(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        # Numbers become numbers; every other token is a symbol.
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return Symbol(token)


def eval(exp, env=GLOBAL_ENV):
    """Evaluate a program."""
    # variable reference
    if isinstance(exp, Symbol):
        return env.find(exp)[exp]
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
        elif keyword == "define":
            var, expr = args
            env[var] = eval(expr)
        # assignment
        elif keyword == "set!":
            var, expr = args
            env.find(var)[var] = eval(expr)
        # procedure
        elif keyword == "lambda":
            (_, vars, exp) = exp
            return lambda *args: eval(exp, Env(vars, args, env))
        # sequencing
        elif keyword == "begin":
            for expr in args:
                val = eval(expr, env)
            return val
        # quotation
        elif keyword == "quote":
            return args
        # procedure call
        else:
            return eval(keyword)(*(eval(arg) for arg in args))


def to_string(exp):
    "Convert a Python object back into a Lisp-readable string."
    return '(' + ' '.join(map(to_string, exp)) + ')' \
            if isinstance(exp, list) else str(exp)


def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        parsed = parse(raw_input(prompt))
        try:
            val = eval(parsed)
        except Exception as e:
            print e
        else:
            if val is not None:
                print to_string(val)


if __name__ == "__main__":
    repl()
