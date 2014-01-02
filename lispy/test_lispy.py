import operator

import pytest

from analysis import parse, lex
from expression import Atom, Combination
from interpreter import interpret, GLOBAL_ENV
from context import Context
from semantics import Function, reduce


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
    square = Function((Atom("x"),), parse(lex("(* x x)")))
    result = square(Atom("10"))
    expected = parse(lex("(* 10 10)"))
    assert result == expected


def test_reduce(context):
    square = Function((Atom("x"),), parse(lex("(* x x)")))
    context[Atom("square")] = square
    result = reduce(Combination([Atom("square"), Atom("10")]), context)
    expected = reduce(Combination([Atom("*"), Atom("10"), Atom("10")]), context)
    assert result == expected


def test_evaluate_constant_literal():
    assert interpret("12") == 12


def test_evaluate_if_true(context):
    assert interpret("(if 1 2 3)", context) == 2


def test_evaluate_if_true2(context):
    assert interpret("(if (== 0 0) 2 3)", context) == 2


def test_evaluate_if_false(context):
    assert interpret("(if 0 2 3)", context) == 3

def test_evaluate_if_false2(context):
    assert interpret("(if (== 0 1) 2 3)", context) == 3

def test_plus(context):
    assert interpret("(+ 2 3)", context) == 5


def test_evaluate_define(context):
    assert interpret("(begin (define x 2) x)", context) == 2


def test_define_procedure(context):
    program = "(begin (define (square x) (* x x)) (square 10))"
    assert interpret(program, context) == 100


def test_fact(context):
    program = """
    (begin
        (define (fact n) (if (== n 0) 1 (* n (fact (- n 1)))))
        (fact 10)
    )
    """
    assert interpret(program) == 3628800
