from collections import deque

from expression import Atom
from context import Context



def do_if(context, test, consequence, alternative):
    result = (consequence if evaluate(test, context) else alternative)
    return evaluate(result, context)

def do_define(context, name, value):
    try:
        def f(*args):
            return  evaluate(value, Context(name.operands, args, context))
        f.__name__ = str(name.operator)
        context[name.operator] = f
    except AttributeError:
        context[name] = evaluate(value, context)

def do_begin(context, *expressions):
    for expression in expressions:
        value = evaluate(expression, context)
    return value


BUILTINS = {
    "if": do_if,
    "define": do_define,
    "set!": do_define,
    "begin": do_begin,
}


def get_value(expression, context):
    if type(expression) == Atom:
        try:
            return int(expression.name)
        except ValueError:
            try:
                return float(expression.name)
            except ValueError:
                return context.find(expression.name)[expression.name]
    else:
        if len(expression.elements) == 0:
            return []
        try:
            return BUILTINS[expression.operator.name](context, *expression.operands)
        except KeyError:
            raise ValueError("not a value")

def evaluate(expression, context):
    expressions = deque([expression])
    values = deque()
    while expressions:
        expression = expressions.popleft()
        try:
            value = get_value(expression, context)
        except ValueError:
            expressions.extendleft(expression.elements)
        else:
            values.appendleft(value)
    arguments = deque()
    while len(values) > 1:
        value = values.pop()
        if callable(value):
            procedure = value
            print procedure, arguments
            values.append(procedure(*arguments))
            arguments.clear()
        else:
            arguments.appendleft(value)
    if arguments:
        return values[0](*arguments)
    else:
        return values[0]


"""
def evaluate(expression, context):
    if type(expression) == Atom:
        try:
            return int(expression.name)
        except ValueError:
            try:
                return float(expression.name)
            except ValueError:
                return context.find(expression.name)[expression.name]
    else:
        if len(expression.elements) == 0:
            return []
        try:
            return BUILTINS[expression.operator.name](context, *expression.operands)
        except KeyError:
            values = evaluate((element for element in expression.elements), context)
            procedure = values[0]
            arguments = values[1:]
            return procedure(*arguments)
"""
