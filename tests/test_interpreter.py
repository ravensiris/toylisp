import sys
from io import StringIO
from itertools import chain, repeat
from typing import Any

import pytest

from toylisp.input_stream import InputStream
from toylisp.interpreter import Environment, Interpreter
from toylisp.parser import Parser
from toylisp.token_stream import TokenStream

sys.setrecursionlimit(999999999)

RECURSION_AMOUNT = 99999
RECURSION_HELL = "".join(
    chain(repeat("(+ 1 1 ", RECURSION_AMOUNT), repeat(")", RECURSION_AMOUNT))
)

CODES = [
    (
        """
(+ 1 1)
""",
        2,
    ),
    (
        """
(+ 1 10 100 1000 10000)
""",
        11111,
    ),
    (
        """
(+ 1 (+ 1 1))
""",
        3,
    ),
    (
        """
(- 10 1 1)
""",
        8,
    ),
    (
        """
(- 10 (+ 1 1 1) 1)
""",
        6,
    ),
    (RECURSION_HELL, 954),
]


def addition(*nums):
    total = 0
    for n in nums:
        total += n
    return total


def subtraction(total, *nums):
    for n in nums:
        total -= n
    return total


@pytest.mark.parametrize("code,expected", CODES)
def test_parser(code: str, expected: Any):
    code_io = StringIO(code)
    input_stream = InputStream(code_io)
    token_stream = TokenStream(input_stream)
    parser = Parser(token_stream)
    expr = parser.parse_atom()
    assert expr is not None
    env = Environment()
    env.vars["+"] = addition
    env.vars["-"] = subtraction
    interpreter = Interpreter(env)
    assert interpreter.evaluate(expr) == expected


def test_interpreter():
    pass
