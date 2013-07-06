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
import string

import expression as expr
import token


def tokenize(lexeme):
    try:
        return token.Number(int(lexeme))
    except:
        if lexeme == "(":
            return token.OpenParens()
        elif lexeme == ")":
            return token.CloseParens()
        else:
            return token.Symbol(lexeme)


def lex(source):
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
    lexemes = s.replace('(', ' ( ').replace(')', ' ) ').split()
    for lexeme in lexemes:
        yield tokenize(lexeme)
