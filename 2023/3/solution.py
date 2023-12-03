# %%
from typing import Optional, Iterator, Any
from enum import StrEnum
from dataclasses import dataclass
from functools import cached_property
import re
from functools import reduce
import operator


class Direction(StrEnum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"
    NE = "NE"
    SE = "SE"
    SW = "SW"
    NW = "NW"

    @cached_property
    def _coordinates(self) -> dict[str, tuple[int, int]]:
        return {
            "N": (0, 1),
            "E": (1, 0),
            "S": (0, -1),
            "W": (-1, 0),
            "NE": (1, 1),
            "SE": (1, -1),
            "SW": (-1, -1),
            "NW": (-1, 1),
        }

    def coords(self) -> tuple[int, int]:
        return self._coordinates[self.value]


@dataclass(frozen=True)
class Cell:
    value: str

    i: int
    j: int
    matrix: "Matrix"

    def astuple(self) -> tuple[int, int]:
        return (self.i, self.j)

    def is_digit(self) -> bool:
        return self.value.isnumeric()

    def is_symbol(self) -> bool:
        return not self.value.isnumeric() and self.value != "."

    def move(self, direction: str | Direction) -> Optional["Cell"]:
        direction = (
            direction
            if isinstance(direction, Direction)
            else Direction(direction.upper())
        )

        new_i = self.i + direction.coords()[0]
        new_j = self.j + direction.coords()[1]

        if not self.matrix.is_valid(new_i, new_j):
            return None

        return self.matrix[new_i, new_j]

    def has_symbol_neighbor(self) -> bool:
        for direction in Direction:
            if (cell := self.move(direction)) is None:
                continue

            if cell.is_symbol():
                return True

        return False

    def get_symbol_neighbor(self) -> Optional["Cell"]:
        for direction in Direction:
            if (cell := self.move(direction)) is None:
                continue

            if cell.is_symbol():
                return cell

        return None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return False

        for attr in ["value", "i", "j"]:
            if getattr(self, attr) != getattr(other, attr):
                return False

        return True


@dataclass(eq=True, frozen=True)
class Matrix:
    rows: list[str]

    def is_valid(self, i: int, j: int) -> bool:
        valid_row = i >= 0 and i < len(self.rows)
        if not valid_row:
            return False

        valid_col = j >= 0 and j < len(self.rows[i])
        return valid_col

    def __getitem__(self, coords: tuple[int, int]) -> "Cell":
        i, j = coords

        if not self.is_valid(i, j):
            raise KeyError(f"Invalid coordinates ({i}, {j}).")

        return Cell(self.rows[i][j], i, j, self)


@dataclass
class Part:
    digits: list[Cell]

    def __contains__(self, cell: Cell):
        return cell in self.digits

    def is_valid(self) -> True:
        for digit in self.digits:
            if digit.has_symbol_neighbor():
                return True

        return False

    def get_symbol_neighbor(self) -> Optional["Symbol"]:
        for digit in self.digits:
            if (cell := digit.get_symbol_neighbor()) is not None:
                return Symbol(cell, [self])

        return None

    def __str__(self) -> str:
        return "".join(map(lambda c: c.value, self.digits))

    @classmethod
    def parse(cls, matrix: Matrix) -> Iterator["Part"]:
        for i, row in enumerate(matrix.rows):
            for match in re.finditer(r"\d+", row):
                yield Part([matrix[i, j] for j in range(*match.span())])


@dataclass(eq=True, frozen=True)
class Symbol:
    cell: Cell
    parts: list[Part]

    @property
    def ratio(self) -> int:
        return reduce(operator.mul, [int(str(p)) for p in self.parts])

    def is_gear(self) -> bool:
        return (self.cell.value == "*") and len(self.parts) == 2

    def __str__(self) -> str:
        return f"{self.cell.value}".join(map(lambda p: str(p), self.parts))

    def __add__(self, other: Any) -> "Symbol":
        if not isinstance(other, Symbol):
            raise ValueError(f'Cannot add with other of type "{type(other)}".')

        return Symbol(self.cell, [*self.parts, *other.parts])


with open("inputs/test.txt", "r") as file:
    m = Matrix(file.read().splitlines())

# Part 1

parts = list(Part.parse(m))
ids = [int(str(part)) for part in parts if part.is_valid()]
print("Part 1")
print("Valid Parts:", len(ids))
print("Solution:", sum(ids))
print()

symbols: dict[tuple[int, int], Symbol] = {}
for part in parts:
    if (symbol := part.get_symbol_neighbor()) is None:
        continue

    coords = symbol.cell.astuple()
    if coords in symbols:
        symbols[coords] = symbols[coords] + symbol
    else:
        symbols[coords] = symbol

ratios = [v.ratio for v in symbols.values() if v.is_gear()]
print("Part 2")
print("Gears:", len(ratios))
print("Solution:", sum(ratios))
