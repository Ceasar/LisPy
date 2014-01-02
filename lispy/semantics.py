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


def _reduce(expression, context):
    if type(expression) == Atom:
        try:
            return context.find(expression)[expression]
        except NameError:
            return expression
    elif type(expression) == Function:
        return expression
    elif len(expression.elements) == 0:
        return expression
    else:
        if expression.operator == Atom("define"):
            try:
                signature, body = expression.operands
                name, parameters = signature.operator, signature.operands
                context[name] = Function(parameters, body)
                return name
            except AttributeError:
                name, value = expression.operands
                context[name] = value
                return name
        elif expression.operator == Atom("if"):
            test, consequence, alternative = expression.operands
            return consequence if reduce(test, context) == TRUE else alternative
        elif all(type(element) in (Atom, Function) for element in expression.operands): 
            if expression.operator == Atom("begin"):
                return expression.operands[-1]
            elif expression.operator == Atom(":"):
                x, xs = expression.operands
                ys = evaluate(xs, context)
                ys.append(evaluate(x, context))
                return ys
            elif expression.operator == Atom("+"):
                i, j = expression.operands
                result = str(evaluate_one(i) + evaluate_one(j))
                return Atom(result)
            elif expression.operator == Atom("-"):
                i, j = expression.operands
                result = str(evaluate_one(i) - evaluate_one(j))
                return Atom(result)
            elif expression.operator == Atom("*"):
                i, j = expression.operands
                result = str(evaluate_one(i) * evaluate_one(j))
                return Atom(result)
            elif expression.operator == Atom("=="):
                x, y = expression.operands
                if x == y:
                    return TRUE
                else:
                    return FALSE
            else:
                try:
                    procedure = context.find(expression.operator)[expression.operator]
                except NameError:
                    procedure = expression.operator
                return procedure(*expression.operands)
        else:
            return Combination([_reduce(element, context)
                                for element in expression.elements])
        
def reduce(expression, context):
    last_expression = expression
    while True:
        expression = _reduce(expression, context)
        if expression == last_expression:
            return expression
        last_expression = expression


def evaluate_one(expression):
    if type(expression) == Atom:
        return int(expression.name)
    else:
        return expression.elements

def evaluate(expression, context):
    reduced = reduce(expression, context)
    return evaluate_one(reduced)
