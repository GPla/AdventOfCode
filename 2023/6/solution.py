# %%
from dataclasses import dataclass
from typing import Iterator
import re
from functools import reduce
import operator
import math


@dataclass
class Race:
    time: int
    distance: int
    acceleration: int = 1

    def get_winning(self):
        min, max = self.solve_distance()
        return max - min + 1

    def get_strategies(self, threshold: int = 0) -> list[tuple[int, int]]:
        return [
            (t, distance)
            for t in range(self.time)
            if (distance := self.f_distance(t)) > threshold
        ]

    def f_distance(self, t: int) -> int:
        return (self.time - t) * t

    def solve_distance(self):
        a = self.time / 2
        b = math.sqrt((self.time / 2) ** 2 - self.distance)
        eps = 1e-8
        return math.ceil(a - b + eps), math.floor(a + b - eps)

    @classmethod
    def parse(cls, contents: str) -> Iterator["Race"]:
        times, distances = contents.splitlines()
        times, distances = [re.findall(r"\d+", s) for s in [times, distances]]

        for time, distance in zip(times, distances):
            yield Race(int(time), int(distance))


with open("inputs/test.txt") as file:
    contents = file.read()

# Part 1
races = list(Race.parse(contents))
winning = [race.get_winning() for race in races]
print("Part 1")
print("Answer:", reduce(operator.mul, winning))

# Part 2
race = list(Race.parse(contents.replace(" ", "")))[0]
winning = [race.get_winning() for race in races]

print("Part 2")
print("Answer:", race.get_winning())
