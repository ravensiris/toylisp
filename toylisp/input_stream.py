from dataclasses import dataclass
from typing import IO


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
