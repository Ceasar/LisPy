from collections import deque

from expression import Atom, Combination
from context import Context

def tail_recursive(func):
    """
    Create a tail recursive function.

    The new function will not lengthen the call stack and so avoids issues
    with Python's recursion limit.

    To gain this functionality, the decorated function must be a generator.
    This makes recursive calls lazy.

    NOTE: This is not a decorator. The function must be able to call itself
    directly. Usage should look something like:

        def _fact(n, r=1):
            yield r if n == 0 else _fact(n - 1, n * r)
        fact = tail_recursive(_fact)
    """
    def wrapped(*args, **kwargs):
        g = func(*args, **kwargs)
        try:
            while True:
                g = next(g)
        except TypeError:  # g is not an iterator
            return g
    return wrapped


TRUE = Atom("1")
FALSE = Atom("0")

class Function(object):
    def __init__(self, parameters, body):
        self.parameters = parameters
        self.body = body

    def __call__(self, *args):
        rv = substitute(self.body, Context(self.parameters, args))
        return rv

    def __repr__(self):
        return "%s -> %s" % (self.parameters, self.body)


def get_value(expression, context):
    if type(expression) == Atom:
        try:
            return int(expression.name)
        except ValueError:
            try:
                return float(expression.name)
            except ValueError:
                return context.find(expression.name)[expression.name]
    elif len(expression.elements) == 0:
        return []
    else:
        raise ValueError("not a value")


def substitute(expression, context):
    """Replace all symbols in an expression with their values in context."""
    if type(expression) == Atom:
        try:
            return context.find(expression)[expression]
        except NameError:
            return expression
    else:
        return Combination(list(substitute(element, context)
                                for element in expression.elements))


def _reduce(expression, context):
    if type(expression) == Atom:
        try:
            yield context.find(expression)[expression]
        except NameError:
            yield expression
    elif type(expression) == Function:
        yield expression
    elif len(expression.elements) == 0:
        yield expression
    else:
        if expression.operator == Atom("define"):
            try:
                signature, body = expression.operands
                name, parameters = signature.operator, signature.operands
                context[name] = Function(parameters, body)
                yield name
            except AttributeError:
                name, value = expression.operands
                context[name] = value
                yield name
        elif expression.operator == Atom("if"):
            test, consequence, alternative = expression.operands
            yield consequence if reduce(test, context) == TRUE else alternative
        elif all(type(element) in (Atom, Function) for element in expression.operands): 
            if expression.operator == Atom("begin"):
                yield expression.operands[-1]
            elif expression.operator == Atom(":"):
                x, xs = expression.operands
                ys = evaluate(xs, context)
                ys.append(evaluate(x, context))
                yield ys
            elif expression.operator == Atom("+"):
                i, j = expression.operands
                result = str(evaluate_one(i) + evaluate_one(j))
                yield Atom(result)
            elif expression.operator == Atom("-"):
                i, j = expression.operands
                result = str(evaluate_one(i) - evaluate_one(j))
                yield Atom(result)
            elif expression.operator == Atom("*"):
                i, j = expression.operands
                result = str(evaluate_one(i) * evaluate_one(j))
                yield Atom(result)
            elif expression.operator == Atom("=="):
                x, y = expression.operands
                yield TRUE if x == y else FALSE
            else:
                try:
                    procedure = context.find(expression.operator)[expression.operator]
                except NameError:
                    procedure = expression.operator
                yield _reduce(procedure(*expression.operands), context)
        else:
            yield _reduce(Combination([reduce(element, context)
                                       for element in expression.elements]), context)
reduce = tail_recursive(_reduce)


def evaluate_one(expression):
    if type(expression) == Atom:
        return int(expression.name)
    else:
        return expression.elements

def evaluate(expression, context):
    reduced = reduce(expression, context)
    return evaluate_one(reduced)
