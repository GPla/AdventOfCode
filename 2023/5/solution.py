# %%
from dataclasses import dataclass
from typing import Optional
from tqdm import tqdm
from joblib import Parallel, delayed
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

    def reverse_map(self, value: int) -> Optional[int]:
        offset = value - self.destination
        if offset < 0 or offset >= self.range:
            return None

        return self.source + offset


@dataclass
class Map:
    name: str
    entries: list[Entry]

    def convert(self, value: int) -> int:
        for entry in self.entries:
            if (output := entry.map(value)) is not None:
                return output
        return value

    def reverse_convert(self, value: int) -> int:
        for entry in self.entries:
            if (output := entry.reverse_map(value)) is not None:
                return output
        return value

    @classmethod
    def parse(cls, block: str):
        name, *entries = block.splitlines()
        name = name.replace(" map:", "")
        return Map(name=name, entries=cls.generate_entries(*entries))

    @classmethod
    def generate_entries(cls, *lines: str):
        entries = [Entry(*map(int, line.split(" "))) for line in lines]
        min_entry = min(entries, key=lambda e: e.destination)
        if min_entry.destination != 0:
            entries.append(Entry(0, 0, min_entry.destination))
        return entries


@dataclass
class RangeSeed:
    value: int
    range: int

    def contains(self, value: int) -> bool:
        return self.value <= value < self.value + self.range


class Solver:
    @staticmethod
    def resolve(seed: int, maps: list[Map], verbose: bool = False):
        if verbose:
            print("seed", seed)

        value = seed
        for map in maps:
            value = map.convert(value)
            if verbose:
                print(map.name.split("-")[-1], value)

        return value

    @staticmethod
    def reverse_resolve(location: int, maps: list[Map], verbose: bool = False):
        if verbose:
            print("location", location)

        value = location
        for map in maps[::-1]:
            value = map.reverse_convert(value)
            if verbose:
                print(map.name.split("-")[0], value)

        return value

    @staticmethod
    def reverse_search(
        seeds: list[RangeSeed],
        maps: list[Map],
        verbose: bool = True,
    ) -> Optional[int]:
        sorted_entries = sorted(maps[-1].entries, key=lambda e: e.destination)
        for entry in tqdm(sorted_entries, "Entries"):
            if verbose:
                print(f"Searching {entry.range} from {entry.destination}.")

            possible_locations = range(
                entry.destination,
                entry.destination + entry.range,
            )

            possible_seeds = Parallel()(
                delayed(Solver._reverse_search_location)(location, maps)
                for location in tqdm(possible_locations, position=1)
            )

            location, seed = next(
                (
                    (location, seed)
                    for (location, seed) in possible_seeds
                    if seed is not None
                ),
                (None, None),
            )

            if seed is not None:
                return seed, location

    @staticmethod
    def _reverse_search_location(location: int, maps: list[Map]):
        possible_seed = Solver.reverse_resolve(location, maps)
        for seed in seeds:
            if seed.contains(possible_seed):
                print(f"Matched seed '{seed}' to location '{location}'.")
                return location, seed
        return (location, None)


with open("inputs/test.txt") as file:
    lines = file.read()

seeds, *blocks = lines.split("\n\n")
seeds = list(map(int, seeds.split(" ")[1:]))
maps = [Map.parse(block) for block in blocks]

locations = [Solver.resolve(seed, maps, verbose=False) for seed in seeds]


# %%
# Part 1
print("Part 1")
print("Answer:", min(locations))

# Part 2
print("Part 2")
seeds = [RangeSeed(s, r) for s, r in list(zip(seeds[0::2], seeds[1::2]))]
Solver.reverse_search(seeds, maps)
# Still takes like 15mins to find the correct seed :/
