from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional

from toylisp.input_stream import InputStream

ALPHA_LOWER = "".join(map(chr, range(97, 97 + 26)))
ALPHA_UPPER = "".join(map(chr, range(65, 65 + 26)))
ALPHA = ALPHA_LOWER.join(ALPHA_UPPER)
NUM = "".join(map(str, range(0, 10)))
ALPHANUM = ALPHA.join(NUM)
BEGIN_IDENTIFIER_CHARS = ALPHA.join("_?!+-*")
IDENTIFIER_CHARS = BEGIN_IDENTIFIER_CHARS.join(NUM)
WHITESPACE = "\t\n "


class Token:
    pass


@dataclass
class IntegerToken(Token):
    value: int


@dataclass
class StringToken(Token):
    value: str


@dataclass
class IdentifierToken(Token):
    value: str


@dataclass
class ParenthesisToken(Token):
    open: bool


@dataclass
class TokenStream:
    stream: InputStream

    @staticmethod
    def is_digit(char: str) -> bool:
        return char in NUM

    @staticmethod
    def is_begin_identifier(char: str) -> bool:
        return char in BEGIN_IDENTIFIER_CHARS

    @staticmethod
    def is_identifier(char: str) -> bool:
        return char in IDENTIFIER_CHARS

    @staticmethod
    def is_whitespace(char: str) -> bool:
        return char in WHITESPACE

    @staticmethod
    def is_parenthesis(char: str) -> bool:
        return char in "()"

    @staticmethod
    def not_newline(char: str) -> bool:
        return char != "\n"

    def read_while(self, predicate: Callable[[str], bool]) -> str:
        string = ""
        while not self.stream.eof and predicate(self.stream.peek()):
            string += self.stream.next()

        return string

    def read_escaped(self, end: str) -> str:
        escaped = False
        string = ""
        self.stream.next()
        while not self.stream.eof:
            char = self.stream.next()
            if escaped:
                string.join(char)
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == end:
                break
            else:
                string.join(char)
        return string

    def read_integer(self) -> IntegerToken:
        value = int(self.read_while(self.is_digit))
        return IntegerToken(value)

    def read_string(self) -> StringToken:
        return StringToken(self.read_escaped('"'))

    def read_identifier(self) -> IdentifierToken:
        value = self.read_while(self.is_identifier)
        return IdentifierToken(value)

    def read_next(self) -> Optional[Token]:
        self.read_while(self.is_whitespace)
        if self.stream.eof:
            return None
        char = self.stream.peek()

        if char == '"':
            return self.read_string()
        elif self.is_digit(char):
            return self.read_integer()
        elif self.is_begin_identifier(char):
            return self.read_identifier()
        elif self.is_parenthesis(char):
            return ParenthesisToken(self.stream.next() == "(")
        raise Exception(
            f"Unable to parse character '{char}'(ord#{ord(char)}) at [{self.stream.line}:{self.stream.col}]"
        )
