# %%
from typing import Optional
from enum import Enum

with open("inputs/test.txt") as file:
    raw_field = file.read().splitlines()


class Direction(Enum):
    N = (0, -1)
    W = (-1, 0)
    S = (0, 1)
    E = (1, 0)


class Field:
    def __init__(self, field: list[str]) -> None:
        self.field = [[item for item in row] for row in field]

    def __getitem__(self, position: tuple[int, int]) -> str:
        return self.field[position[1]][position[0]]

    def __setitem__(self, position: tuple[int, int], value: str):
        self.field[position[1]][position[0]] = value

    def tilt(self, direction: Direction):
        if direction in [Direction.N, Direction.W]:
            for j, row in enumerate(self.field):
                for i, item in enumerate(row):
                    if item == "O":
                        self.move_rock((i, j), direction)
        else:
            rows, cols = len(self.field) - 1, len(self.field[0]) - 1
            for j, row in enumerate(self.field[::-1]):
                for i, item in enumerate(row[::-1]):
                    if item == "O":
                        self.move_rock((cols - i, rows - j), direction)

    def move_rock(self, position: tuple[int, int], direction: Direction):
        next = self._next(position, direction)

        while next is not None and self[next] == ".":
            self[position] = "."
            self[next] = "O"
            position = next
            next = self._next(position, direction)

    def _next(
        self, position: tuple[int, int], direction: Direction
    ) -> Optional[tuple[int, int]]:
        match direction:
            case Direction.N:
                if position[1] == 0:
                    return None
            case Direction.S:
                if position[1] == len(self.field) - 1:
                    return None
            case Direction.E:
                if position[0] == len(self.field[0]) - 1:
                    return None
            case Direction.W:
                if position[0] == 0:
                    return None

        return (
            position[0] + direction.value[0],
            position[1] + direction.value[1],
        )

    def calculate_load(self):
        load = 0
        for j, row in enumerate(self.field[::-1], 1):
            for item in row:
                if item == "O":
                    load += j

        return load

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self.field])

    def __repr__(self) -> str:
        return self.__str__()


field = Field(raw_field)

print("Part 1")
field.tilt(Direction.N)
print("Answer:", field.calculate_load())

field = Field(raw_field)
i = 0
max_iter = 100000
while i <= max_iter:
    for direction in Direction:
        field.tilt(direction)
    if (i % 1000) == 0:
        print(i, field.calculate_load())
    i += 1

