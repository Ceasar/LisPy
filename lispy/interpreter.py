import operator as op

from analysis import lex, parse
from context import Context
from expression import Atom
from semantics import evaluate



def interpret(program, context=None):
    if context is None:
        context = Context()
    return evaluate(parse(lex(program)), context)

def append(xs, x):
    return []

GLOBAL_ENV = Context()
GLOBAL_ENV.update({
    Atom(':'): append,
})
