from collections import deque

from expression import Atom, Combination
from context import Context


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


def evaluate_one(expression, context):
    if type(expression) == Atom:
        try:
            return int(expression.name)
        except ValueError:
            try:
                return float(expression.name)
            except ValueError:
                return context.find(expression)[expression]
    else:
        if len(expression.elements) == 0:
            return []
        elif expression.operator == Atom("define"):
            try:
                signature, body = expression.operands
                name, parameters = signature.operator, signature.operands
                context[name] = Function(parameters, body)
            except AttributeError:
                name, value = expression.operands
                context[name] = value
        elif expression.operator == Atom("begin"):
            for e in expression.operands:
                val = evaluate(e, context)
            return val
        elif expression.operator == Atom(":"):
            x, xs = expression.operands
            ys = evaluate(xs, context)
            ys.append(evaluate(x, context))
            return ys
        elif expression.operator == Atom("if"):
            test, consequence, alternative = expression.operands
            return consequence if evaluate(test, context) else alternative
        elif expression.operator == Atom("+"):
            i, j = expression.operands
            result = str(evaluate(i, context) + evaluate(j, context))
            return Atom(result)
        elif expression.operator == Atom("*"):
            i, j = expression.operands
            result = str(evaluate(i, context) * evaluate(j, context))
            return Atom(result)
        elif expression.operator == Atom("=="):
            x, y = expression.operands
            if evaluate(x, context) == evaluate(y, context):
                return TRUE
            else:
                return FALSE
        else:
            procedure = context[expression.operator]
            return procedure(*expression.operands)

def evaluate(expression, context):
    # TODO: Do this in a more robust way
    while True:
        if expression is None or type(expression) in (int, list):
            return expression
        else:
            # print "=" * 80
            # print expression
            expression = evaluate_one(expression, context)
