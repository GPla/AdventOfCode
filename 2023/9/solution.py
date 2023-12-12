# %%
from dataclasses import dataclass
from itertools import pairwise
from functools import reduce


@dataclass
class Series:
    numbers: list[int]

    def extrapolate(self) -> int:
        diffs = self._find_diffs(self.numbers)
        diff = sum([diff[-1] for diff in diffs[1:-1]])
        return self.numbers[-1] + diff

    def _find_diffs(self, numbers: list[int]) -> list[list[int]]:
        numbers = [numbers]
        while not all([n == 0 for n in numbers[-1]]):
            numbers.append(self._extrapolate(numbers[-1]))
        return numbers

    def _extrapolate(self, numbers: list[int]) -> list[int]:
        return [b - a for (a, b) in pairwise(numbers)]

    def extrapolate_rev(self) -> int:
        diffs = self._find_diffs(self.numbers)
        s = [diff[0] for diff in diffs[1:]][::-1]
        diff = reduce(lambda a, b: b - a, s)
        return self.numbers[0] - diff

    @classmethod
    def parse(cls, line: str) -> "Series":
        return Series([int(n) for n in line.split(" ")])


with open("inputs/test.txt") as file:
    lines = file.read().splitlines()

series = [Series.parse(line) for line in lines]

extrapolated = [s.extrapolate() for s in series]
print("Part 1")
print("Answer:", sum(extrapolated))


extrapolated_rev = [s.extrapolate_rev() for s in series]
print("Part 2")
print("Answer:", sum(extrapolated_rev))
