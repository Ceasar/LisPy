from expression import Atom
from context import Context



def do_if(context, test, consequence, alternative):
    result = (consequence if evaluate(test, context) else alternative)
    return evaluate(result, context)

def do_define(context, name, value):
    try:
        context[name.operator] = lambda *args: (
            evaluate(value, Context(name.operands, args, context)))
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
            procedure = evaluate(expression.operator, context)
            arguments = (evaluate(operand, context) for operand in expression.operands)
            return procedure(*arguments)
