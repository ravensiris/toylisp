from io import StringIO

from toylisp.input_stream import InputStream
from toylisp.token_stream import (IdentifierToken, IntegerToken,
                                  ParenthesisToken, TokenStream)

TEST_CODE = StringIO(
    """
(+ 1 1)
"""
)


def test_token_stream():
    input_stream = InputStream(TEST_CODE)
    token_stream = TokenStream(input_stream)
    assert token_stream.read_next() == ParenthesisToken(open=True)
    assert token_stream.read_next() == IdentifierToken("+")
    assert token_stream.read_next() == IntegerToken(1)
    assert token_stream.read_next() == IntegerToken(1)
    assert token_stream.read_next() == ParenthesisToken(open=False)
