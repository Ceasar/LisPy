from analysis import lex, parse
from context import Context


def interpret(program, context=None):
    if context is None:
        context = Context()
    return parse(lex(program)).evaluate(context)
