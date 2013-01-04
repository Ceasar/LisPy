from nose.tools import assert_equal, nottest

from lis import parse, eval, Env


skip = nottest


def test_parse():
    program = "(set! twox (* x 2))"
    assert_equal(parse(program), ['set!', 'twox', ['*', 'x', 2]])


def test_parse_atom():
    program = "2"
    assert_equal(parse(program), 2)


def test_eval_variable_reference():
    env = Env(("x",), (10,))
    assert_equal(eval("x", env), 10)


def test_eval_constant_literal():
    assert_equal(eval(12), 12)


def test_eval_if_true():
    assert_equal(eval(["if", 1, 2, 3]), 2)


def test_eval_if_false():
    assert_equal(eval(["if", 0, 2, 3]), 3)


def test_eval_define():
    eval(["define", "x", 2])
    assert_equal(eval("x"), 2)


def test_eval_set():
    eval(["define", "x", 2])
    eval(["set!", "x", 3])
    assert_equal(eval("x"), 3)


@skip
def test_lambda():
    f = eval(["lambda", ["x"], ["x"]])
    assert_equal(f(1), 1)


def test_eval_begin():
    eval(["begin", ["define", "x", 2], "x"])
    assert_equal(eval("x"), 2)
