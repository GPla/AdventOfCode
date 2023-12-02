# %%

from dataclasses import dataclass
import operator
from functools import reduce


@dataclass
class Draw:
    red: int = 0
    blue: int = 0
    green: int = 0

    @classmethod
    def parse(cls, line: str):
        return Draw(
            **{
                color: int(count)
                for count, color in map(str.split, line.split(","))
            }
        )

    def is_valid(self, red: int, blue: int, green: int) -> bool:
        return self.red <= red and self.green <= green and self.blue <= blue


@dataclass
class Game:
    id: int
    draws: Draw

    @classmethod
    def parse(cls, line: str):
        id, games = line.split(":")
        id = int(id.split(" ")[1])
        draws = [Draw.parse(draw) for draw in games.split(";")]
        return Game(id=id, draws=draws)

    def is_valid(self, red: int, blue: int, green: int) -> bool:
        return all([draw.is_valid(red, blue, green) for draw in self.draws])

    def fewest(self):
        return {
            field: max([getattr(draw, field) for draw in self.draws])
            for field in Draw.__dataclass_fields__
        }

    def fewest_power(self):
        return reduce(operator.mul, self.fewest().values(), 1)


with open("inputs/test.txt", "r") as file:
    games = [Game.parse(line) for line in file.readlines()]

with open("inputs/val.txt", "r") as file:
    val_games = [Game.parse(line) for line in file.readlines()]

# Part 1
ids = [game.id for game in games if game.is_valid(red=12, green=13, blue=14)]
print("Part 1")
print("Answer:", sum(ids))
print()

# Part 2
powers = [game.fewest_power() for game in games]
print("Part 2")
print("Answer:", sum(powers))
