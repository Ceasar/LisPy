"""
Helper functions for analyzing a source program.

The analysis part breaks up the source program into constituent pieces and
imposes a grammatical structure on them. It then uses this structure to create
an intermediate representation of the source program. If the analysis part
detects that the source program is either syntactically ill formed or
semantically unsound, then it must provide informative messages, so the user
can take corrective action. The analysis part also collects information about
the source program and stores it in a data structure called a symbol table,
which is passed along with the intermediate representation to the synthesis
part.
"""
from expression import Atom, Combination


def lex(s):
    """
    Parse tokens from a string.

    A token is either a parenthesis or a string.

    >>> list(lex("(:= x 1)"))
    ['(', ':=', 'x', 1, ')']
    >>> list(lex("(do (:= x 1) x)"))
    ['(', 'do', '(', ':=', 'x', 1, ')', 'x', ')']
    >>> list(lex("(if (== 0 0) 1 2)"))
    ['(', 'if', '(', '==', 0, 0, ')', 1, 2, ')']
    """
    tokens = s.replace('(', ' ( ').replace(')', ' ) ').split()

    # Numbers become numbers; every other token is a symbol.
    for token in tokens:
        if token in ('(', ')'):
            yield token
        else:
            yield Atom(token)


def _parse_expression(tokens):
    elements = []
    for token in tokens:
        if token == '(':
            elements.append(_parse_expression(tokens))
        elif token == ')':
            break
        else:
            elements.append(token)
    return Combination(elements)

def parse(tokens):
    """"
    Read an expression from a sequence of tokens.

    >>> parse(iter([1]))
    1
    >>> parse(iter(['(', ':=', 'x', 1, ')']))
    [':=', 'x', 1]
    >>> parse(iter(['(', 'do', '(', ':=', 'x', 1, ')', 'x', ')']))
    ['do', [':=', 'x', 1], 'x']
    >>> parse(iter(['(', 'if', '(', '==', 0, 0, ')', 1, 2, ')']))
    ['if', ['==', 0, 0], 1, 2]
    """
    return _parse_expression(tokens).elements[0]
