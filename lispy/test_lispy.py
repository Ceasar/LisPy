import pytest

from analysis import interpret
from synthesis import Environment as Env


@pytest.fixture(params=["2", "(+ 2 2)"])
def program(request):
    return request.param


@pytest.fixture()
def tokens(program):
    return lex(program)

@pytest.fixture()
def environment():
    return Env(("x",), (10,))


def test_evaluate_constant_literal():
    assert interpret("12").evaluate() == 12


def test_evaluate_if_true():
    assert interpret("(if 1 2 3)").evaluate() == 2


def test_evaluate_if_false():
    assert interpret("(if 0 2 3)").evaluate() == 3


def test_evaluate_define():
    assert interpret("(begin (define x 2) x)").evaluate() == 2


def test_evaluate_set():
    assert interpret("(begin (define x 2) (set! x 3) x)").evaluate() == 3
