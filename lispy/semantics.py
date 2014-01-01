from context import Context



def do_if(context, test, consequence, alternative):
    result = (consequence if test.evaluate(context) else alternative)
    return result.evaluate(context)

def do_define(context, name, value):
    try:
        context[name.operator] = lambda *args: (
            value.evaluate(Context(name.operands, args, context)))
    except AttributeError:
        context[name] = value.evaluate(context)

def do_begin(context, *expressions):
    for expression in expressions:
        value = expression.evaluate(context)
    return value


BUILTINS = {
    "if": do_if,
    "define": do_define,
    "set!": do_define,
    "begin": do_begin,
}


