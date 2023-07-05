from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import IO, Union


@dataclass
class InputStream:
    input: IO[str]
    line: int = 0
    col: int = 0

    @property
    def pos(self) -> int:
        return self.input.tell()

    @property
    def eof(self) -> bool:
        return self.peek() == ""

    def next(self) -> str:
        char = self.input.read(1)
        self.col += 1
        if char == "\n":
            self.line += 1
            self.col = 0
        return char

    def peek(self) -> str:
        pos = self.pos
        char = self.input.read(1)
        self.input.seek(pos)
        return char


ALPHA_LOWER = "".join(map(chr, range(97, 97 + 26)))
ALPHA_UPPER = "".join(map(chr, range(65, 65 + 26)))
ALPHA = ALPHA_LOWER.join(ALPHA_UPPER)
NUM = "".join(map(str, range(0, 10)))
ALPHANUM = ALPHA.join(NUM)
IDENTIFIER_CHARS = ALPHANUM.join("_?!")
WHITESPACE = "\t\n "
OPERATOR_CHARS = "+-*/%=&|<>"
PUNCTUATION_CHARS = ",(){}[]"


class TokenType(Enum):
    Integer = auto()
    String = auto()
    Identifier = auto()
    Operator = auto()
    Punctuation = auto()


@dataclass
class Token:
    type: TokenType
    value: Union[int, str]


@dataclass
class TokenStream:
    stream: InputStream

    @staticmethod
    def is_digit(char: str) -> bool:
        return char in NUM

    @staticmethod
    def is_id_start(char: str) -> bool:
        return char in ALPHA

    @staticmethod
    def is_id(char: str) -> bool:
        return char in IDENTIFIER_CHARS

    @staticmethod
    def is_whitespace(char: str) -> bool:
        return char in WHITESPACE

    @staticmethod
    def not_newline(char: str) -> bool:
        return char != "\n"

    @staticmethod
    def is_op_char(char: str) -> bool:
        return char in OPERATOR_CHARS

    @staticmethod
    def is_punc(char: str) -> bool:
        return char in PUNCTUATION_CHARS

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

    def read_int(self) -> Token:
        value = int(self.read_while(self.is_digit))
        return Token(type=TokenType.Integer, value=value)

    def read_string(self) -> Token:
        return Token(type=TokenType.String, value=self.read_escaped('"'))

    def read_ident(self) -> Token:
        value = self.read_while(self.is_id)
        return Token(type=TokenType.Identifier, value=value)

    def skip_comment(self) -> str:
        self.read_while(self.not_newline)
        return self.stream.next()

    def read_next(self):
        self.read_while(self.is_whitespace)
        if self.stream.eof:
            return None
        char = self.stream.peek()
        if char == ";":
            self.skip_comment()
            return self.read_next()
        elif char == '"':
            return self.read_string()
        elif self.is_digit(char):
            return self.read_int()
        elif self.is_id_start(char):
            return self.read_ident()
        elif self.is_punc(char):
            return Token(type=TokenType.Punctuation, value=self.stream.next())
        elif self.is_op_char(char):
            return Token(type=TokenType.Operator, value=self.stream.next())
        raise Exception(
            f"Unable to parse character '{char}'(ord#{ord(char)}) at {self.stream.line}:{self.stream.col}"
        )


class AST:
    pass


@dataclass
class IntegerAST(AST):
    value: int


@dataclass
class StringAST(AST):
    value: str


@dataclass
class BoolAST(AST):
    value: bool


@dataclass
class VariableAST(AST):
    name: str


@dataclass
class LambdaAST(AST):
    vars: list[AST]
    body: AST


@dataclass
class CallAST(AST):
    function: AST
    args: AST


@dataclass
class IfAST(AST):
    condition: AST
    then: AST
    else_: AST


@dataclass
class BinaryAST(AST):
    operator: str
    left: AST
    right: AST


@dataclass
class AssignAST(AST):
    left: AST
    right: AST


class ClosureAST(AST):
    inner: list[AST]
