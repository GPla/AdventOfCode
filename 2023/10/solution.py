# %%
with open("inputs/test.txt") as file:
    contents = file.read()


class Maze:
    def __init__(self, lines: str):
        self.tiles: list[list[str]] = [
            [self._create_tile(tile, (i, j)) for i, tile in enumerate(line)]
            for j, line in enumerate(lines.splitlines())
        ]

        if not hasattr(self, "start"):
            raise ValueError("Missing start.")

    def _create_tile(self, value: str, position: tuple[int, int]):
        if value == "S":
            self.start: tuple[int, int] = position
        return value

    def __getitem__(self, position: tuple[int, int]) -> str:
        return self.tiles[position[1]][position[0]]

    def _directions(
        self,
        tile: str,
    ) -> tuple[tuple[int, int], tuple[int, int]]:
        match tile:
            case "|":
                return (0, 1), (0, -1)
            case "-":
                return (-1, 0), (1, 0)
            case "L":
                return (0, -1), (1, 0)
            case "J":
                return (0, -1), (-1, 0)
            case "7":
                return (0, 1), (-1, 0)
            case "F":
                return (0, 1), (1, 0)
            case _:
                return (0, 0), (0, 0)

    def explore(self, tile: str):
        if not self._valid_tile(tile, self.start):
            raise ValueError(
                "Invalid starting tile. "
                "Must be connected to exactly two other tiles."
            )

        direction = self._directions(tile)[0]
        position = self._move(self.start, direction)

        steps = 1
        inv_direction = self._invert_direction(direction)
        while position != self.start:
            dir_1, dir_2 = self._directions(self[position])
            direction = dir_1 if dir_1 != inv_direction else dir_2
            inv_direction = self._invert_direction(direction)

            if not self._valid_move(position, direction):
                raise ValueError("Not a loop.")

            position = self._move(position, direction)
            steps += 1

        return steps

    def _invert_direction(self, direction: tuple[int, int]) -> tuple[int, int]:
        return (-1 * direction[0], -1 * direction[1])

    def _move(
        self,
        position: tuple[int, int],
        direction: tuple[int, int],
    ) -> tuple[int, int]:
        return (position[0] + direction[0], position[1] + direction[1])

    def _valid_tile(self, tile: str, position: tuple[int, int]) -> bool:
        for direction in self._directions(tile):
            other_tile = self[self._move(position, direction)]
            inv_direction = self._invert_direction(direction)
            if inv_direction not in self._directions(other_tile):
                return False
        return True

    def _valid_move(
        self,
        position: tuple[int, int],
        direction: tuple[int, int],
    ) -> bool:
        tile = self[self._move(position, direction)]
        if tile == "S":
            return True

        if direction == (0, 0):
            return False

        return self._invert_direction(direction) in self._directions(tile)


maze = Maze(contents)
for start_tile in ["|", "-", "L", "J", "7", "F"]:
    try:
        steps = maze.explore(start_tile)
        print(f'Took {steps} steps with tile "{start_tile}".')
        print("Answer:", int(steps / 2))
    except ValueError:
        print(f"Invalid tile {start_tile}.")
