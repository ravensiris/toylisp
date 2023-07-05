from dataclasses import dataclass
from typing import Optional, Union

from toylisp.token_stream import (IdentifierToken, IntegerToken,
                                  ParenthesisToken, StringToken, TokenStream)

AST = Union["IntegerAST", "StringAST", "BooleanAST", "VariableAST", "CallAST", "End"]


class End:
    pass


@dataclass
class IntegerAST:
    value: int


@dataclass
class StringAST:
    value: str


@dataclass
class BooleanAST:
    value: bool


@dataclass
class VariableAST:
    name: str


@dataclass
class CallAST:
    function: VariableAST
    arguments: list[AST]


@dataclass
class Parser:
    tokens: TokenStream

    def parse_call(self) -> AST:
        function = self.parse_atom()
        if not isinstance(function, VariableAST):
            raise Exception(
                f"Encountered unexpected call {function} at [{self.tokens.stream.line}:{self.tokens.stream.col}]"
            )
        arguments: list[AST] = []
        while not isinstance((atom := self.parse_atom()), End):
            if atom is None:
                raise Exception(
                    f"Encountered unexpected end in {function} at [{self.tokens.stream.line}:{self.tokens.stream.col}]"
                )
            arguments.append(atom)
        return CallAST(function, arguments)

    def parse_atom(self) -> Optional[AST]:
        token = self.tokens.read_next()
        match token:
            case ParenthesisToken(open=True):
                return self.parse_call()
            case ParenthesisToken(open=False):
                return End()
            case IdentifierToken(value=name):
                return VariableAST(name)
            case IntegerToken(value=value):
                return IntegerAST(value=value)
            case StringToken(value=value):
                return StringAST(value=value)
            case None:
                return None
        raise Exception(f"Unknown token encountered {token}")
