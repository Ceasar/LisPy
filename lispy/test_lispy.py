import pytest

from analysis import interpret
from synthesis import Environment as Env, evaluate


@pytest.fixture(params=["2", "(+ 2 2)"])
def program(request):
    return request.param


@pytest.fixture()
def tokens(program):
    return lex(program)

@pytest.fixture()
def environment():
    return Env(("x",), (10,))


def test_evaluate_variable_reference(environment):
    assert evaluate("x", environment) == 10


def test_evaluate_constant_literal():
    assert evaluate(interpret("12")) == 12


def test_evaluate_if_true():
    assert evaluate(interpret("(if 1 2 3)")) == 2


def test_evaluate_if_false():
    assert evaluate(interpret("(if 0 2 3)")) == 3


def test_evaluate_define():
    assert evaluate(interpret("(begin (define x 2) x)")) == 2


def test_evaluate_set():
    assert evaluate(interpret("(begin (define x 2) (set! x 3) x)")) == 3
