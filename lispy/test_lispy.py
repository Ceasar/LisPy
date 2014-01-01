import operator

import pytest

from analysis import parse, lex
from expression import Atom, Combination
from interpreter import interpret, GLOBAL_ENV
from context import Context
from semantics import Function


@pytest.fixture(params=["2", "(+ 2 2)"])
def program(request):
    return request.param


@pytest.fixture()
def tokens(program):
    return lex(program)

@pytest.fixture()
def context():
    return GLOBAL_ENV

def test_lex():
    result = list(lex("(* x x)"))
    expected = ["(", Atom("*"), Atom("x"), Atom ("x"), ")"]
    assert result == expected

def test_analyze():
    elements = [Atom("*"), Atom("x"), Atom ("x")]
    result = parse(lex("(* x x)"))
    expected = Combination(elements)
    assert result == expected

def test_apply():
    f = Function((Atom("x"),), parse(lex("(: x (range (- x 1)))")))
    g = f(parse(lex("10")))
    e = parse(lex("(: 10 (range (- 10 1)))"))
    assert g == e

def test_apply2():
    f = Function((Atom("x"),), parse(lex("(* x x)")))
    result = f(Atom("10"))
    expected = parse(lex("(* 10 10)"))
    assert result == expected


def test_evaluate_constant_literal():
    assert interpret("12") == 12


def test_evaluate_if_true(context):
    assert interpret("(if 1 2 3)", context) == 2


def test_evaluate_if_false(context):
    assert interpret("(if 0 2 3)", context) == 3

def test_plus(context):
    assert interpret("(+ 2 3)", context) == 5


def test_evaluate_define(context):
    assert interpret("(begin (define x 2) x)", context) == 2


def test_define_procedure(context):
    program = "(begin (define (square x) (* x x)) (square 10))"
    assert interpret(program, context) == 100
