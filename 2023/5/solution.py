# %%
from dataclasses import dataclass
from typing import Optional
from itertools import batched
from tqdm import tqdm

@dataclass
class Entry:
    destination: int
    source: int
    range: int

    def map(self, value: int) -> Optional[int]:
        offset = value - self.source
        if offset < 0 or offset >= self.range:
            return None

        return self.destination + offset


@dataclass
class Map:
    name: str
    entries: list[Entry]

    def convert(self, value: int) -> int:
        for entry in self.entries:
            if (output := entry.map(value)) is not None:
                return output
        return value

    @classmethod
    def parse(cls, block: str):
        name, *entries = block.splitlines()
        name = name.replace(' map:', '')
        return Map(
            name=name,
            entries=[Entry(*map(int, entry.split(' '))) for entry in entries],
        )


def resolve(seed: int, maps: list[Map], verbose: bool = False):
    if verbose:
        print('seed', seed)

    value = seed
    for map in maps:
        value = map.convert(value)
        if verbose:
            print(map.name.split('-')[-1], value)

    return value


with open('inputs/test.txt') as file:
    lines = file.read()

seeds, *blocks = lines.split('\n\n')
seeds = list(map(int, seeds.split(' ')[1:]))
maps = [Map.parse(block) for block in blocks]

locations = [resolve(seed, maps, verbose=False) for seed in seeds]


# Part 1
print('Part 1')
print('Answer:', min(locations))

# Part 2
print('Part 2')
locations = [
    resolve(seed, maps, verbose=False)
    for (start, stop) in tqdm(batched(seeds, n=2), 'Seeds')
    for seed in tqdm(range(start, start + stop), 'Seed', position=2)
]
print('Answer:', min(locations))
