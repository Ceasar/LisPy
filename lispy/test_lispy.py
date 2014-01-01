import operator

import pytest

from interpreter import interpret
from context import Context


@pytest.fixture(params=["2", "(+ 2 2)"])
def program(request):
    return request.param


@pytest.fixture()
def tokens(program):
    return lex(program)

@pytest.fixture()
def context():
    return Context(["*"], [operator.mul])


def test_evaluate_constant_literal():
    assert interpret("12") == 12


def test_evaluate_if_true():
    assert interpret("(if 1 2 3)") == 2


def test_evaluate_if_false():
    assert interpret("(if 0 2 3)") == 3


def test_evaluate_define():
    assert interpret("(begin (define x 2) x)") == 2


def test_evaluate_set():
    assert interpret("(begin (define x 2) (set! x 3) x)") == 3


def test_define_procedure(context):
    program = "(begin (define (square x) (* x x)) (square 10))"
    assert interpret(program, context) == 100
