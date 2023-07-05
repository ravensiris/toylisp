from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Self

from toylisp.parser import (AST, BooleanAST, CallAST, IntegerAST, StringAST,
                            VariableAST)


@dataclass
class Environment:
    parent: Optional[Environment] = None
    vars: dict[str, Any] = field(default_factory=dict)

    def extend(self) -> Environment:
        return Environment(self)

    def lookup(self, name: str) -> Optional[Environment]:
        scope: Optional[Environment] = self
        while scope is not None:
            if name in scope.vars:
                return scope
            scope = scope.parent
        return None

    def set_var(self, name: str, value: Any) -> Self:
        scope = self.lookup(name)
        (scope or self).vars[name] = value
        return self

    def get_var(self, name: str) -> Any:
        scope = self.lookup(name)
        vars = (scope or self).vars
        if name in vars:
            return vars[name]
        else:
            raise Exception(f"Unknown variable '{name}'")


@dataclass
class Interpreter:
    env: Environment

    def evaluate(self, expression: AST) -> Any:
        match expression:
            case IntegerAST(value) | StringAST(value) | BooleanAST(value):
                return value
            case CallAST(VariableAST(name), arguments):
                function = self.env.get_var(name)
                args = list(map(self.evaluate, arguments))
                return function(*args)
            case VariableAST(name):
                return self.env.get_var(name)
