from lispy.analysis.syntax import Grammar


def test_valid_grammar():
    g = Grammar(dict([
        ('$', [['<subject>', '<verb-phrase>', '<object>']]),
        ('<subject>', [['This'], ['Computers'], ['I']]),
        ('<verb-phrase>', [['<adverb>', '<verb>'], ['<verb>']]),
        ('<adverb>', [['never']]),
        ('<verb>', [['is'], ['run'], ['am'], ['tell']]),
        ('<object>', [['the', '<noun>'], ['a', '<noun>'], ['<noun>']]),
        ('<noun>', [['university'], ['world'], ['cheese'], ['lies']]),
    ]))
    assert g.is_valid(iter("This is a university".split()))


def test_invalid_grammar():
    g = Grammar(dict([
        ('$', [['<subject>', '<verb-phrase>', '<object>']]),
        ('<subject>', [['This'], ['Computers'], ['I']]),
        ('<verb-phrase>', [['<adverb>', '<verb>'], ['<verb>']]),
        ('<adverb>', [['never']]),
        ('<verb>', [['is'], ['run'], ['am'], ['tell']]),
        ('<object>', [['the', '<noun>'], ['a', '<noun>'], ['<noun>']]),
        ('<noun>', [['university'], ['world'], ['cheese'], ['lies']]),
    ]))
    assert not g.is_valid(iter("This is not a university".split()))


def test_lisp_grammar():
    g = Grammar(dict([
        ('$', [['<expression>']]),
        ('<expression>', [['<atom>'],
                          ['do', '<expression>', '<expression>'],
                          [':=', '<symbol>', '<expression>'],
                          ['(', '<expression>', ')'],
                          ]),
        ('<atom>', [['<symbol>'], ['<number>']]),
        ('<symbol>', [['x']]),
        ('<number>', [['1']]),
    ]))
    assert g.is_valid(iter("do ( := x 1 ) x".split()))
