import operator as op

from analysis import lex, parse
from context import Context
from expression import Atom
from semantics import evaluate



def interpret(program, context=None):
    if context is None:
        context = Context()
    return evaluate(parse(lex(program)), context)

GLOBAL_ENV = Context()
