from io import StringIO
from itertools import chain, repeat
from typing import Union

import pytest

from toylisp.input_stream import InputStream
from toylisp.parser import AST, CallAST, IntegerAST, Parser, VariableAST
from toylisp.token_stream import TokenStream

SIMPLE_ADDITION = (
    """
(+ 1 1)
""",
    CallAST(
        function=VariableAST(name="+"),
        arguments=[IntegerAST(value=1), IntegerAST(value=1)],
    ),
)


ADDITION_WITH_INNER = (
    """
(+ 1 1 (+ 1 1))
""",
    CallAST(
        function=VariableAST(name="+"),
        arguments=[IntegerAST(value=1), IntegerAST(value=1), SIMPLE_ADDITION[1]],
    ),
)

# hits default recursion limit of 1000 at this depth
RECURSION_AMOUNT = 477
RECURSION_HELL = (
    "".join(chain(repeat("(+ 1 1 ", RECURSION_AMOUNT), repeat(")", RECURSION_AMOUNT))),
    True,
)

CODES = [SIMPLE_ADDITION, ADDITION_WITH_INNER, RECURSION_HELL]


@pytest.mark.parametrize("code,expected", CODES)
def test_parser(code: str, expected: Union[bool, AST]):
    code_io = StringIO(code)
    input_stream = InputStream(code_io)
    token_stream = TokenStream(input_stream)
    parser = Parser(token_stream)
    if expected is True:
        assert parser.parse_atom()
    else:
        assert parser.parse_atom() == expected
