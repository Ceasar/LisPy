"""
Syntax Analysis
"""
from collections import deque

import lispy.expression as expr


class Grammar(object):
    """
    A grammar is a tool for describing the syntax of a language.
    """
    def __init__(self, rules, start="$"):
        self.rules = rules
        self.parse_table = self._parse_table

    def is_valid(self, corpus):
        try:
            self.parse(corpus)
        except SyntaxError:
            return False
        else:
            return True

    @property
    def _parse_table(self):
        parse_table = {}

        def terminals(nonterminal):
            rv = {}
            for replacement in self.rules[nonterminal]:
                first = replacement[0]
                if self.is_terminal(first):
                    rv[first] = replacement
                else:
                    for k, v in terminals(first).items():
                        rv[k] = replacement
            return rv

        for nonterminal in self.rules:
            for terminal, replacement in terminals(nonterminal).items():
                parse_table[nonterminal, terminal] = replacement

        return parse_table

    def is_terminal(self, string):
        return not string.startswith('<')

    def parse(self, token_stream):
        """
        Attempt to construct a parse tree from a corpus.
        """
        working_string = deque(['$'])
        look_ahead = next(token_stream)
        while len(working_string) > 0:
            print working_string
            top = working_string.popleft()
            if look_ahead == top:
                try:
                    look_ahead = next(token_stream)
                except StopIteration:
                    return len(working_string) == 0
            else:
                try:
                    replacement = self.parse_table[top, look_ahead]
                except KeyError:
                    raise SyntaxError('No replacement for (%s, %s)' %
                                      (top, look_ahead))
                else:
                    working_string.extendleft(reversed(replacement))


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
    token = next(tokens)
    if isinstance(token, int):
        return expr.Literal(token)
    elif token == '\\':
        return expr.Function(parse(tokens), parse(tokens))
    elif token == ':=':
        name = next(tokens)
        return expr.Definition(name, parse(tokens))
    elif token == 'if':
        return expr.Conditional(parse(tokens), parse(tokens), parse(tokens))
    elif token == 'do':
        xs = []
        while True:
            try:
                v = parse(tokens)
            except StopIteration:
                break
            else:
                xs.append(v)
        return expr.Sequence(*xs)
    elif token == '(':
        buff = []
        count = 0
        for token in tokens:
            if token == '(':
                count += 1
            if token == ')':
                if count == 0:
                    break
                else:
                    count -= 1
            buff.append(token)
        return parse(iter(buff))
    else:
        return expr.Reference(token)

# print(parse(iter(['(', 'do', '(', ':=', 'x', 1, ')', 'x', ')'])))
# print(parse(iter(['(', 'if', '(', '==', 0, 0, ')', 1, 2, ')'])))
