# %%
from math import gcd
from functools import reduce


def lcm(a, b):
    return a // gcd(a, b) * b


def parse_node(line: str) -> tuple[str, tuple[str, str]]:
    name, directions = line.split(" = ")
    left, right = directions.replace("(", "").replace(")", "").split(", ")
    return name, (left, right)


def parse(contents: str) -> tuple[dict[str, tuple[str, str]], str]:
    directions, _, *nodes = contents.splitlines()

    nodes = dict([parse_node(node) for node in nodes])
    return nodes, directions


def solve(
    nodes: dict[str, str],
    directions: str,
    *,
    start: str = "AAA",
    stop: str = "ZZZ",
):
    index = 0
    steps_taken = 0
    node = start
    DIRECTIONS = {"L": 0, "R": 1}
    while 1:
        steps_taken += 1
        node = nodes[node][DIRECTIONS[directions[index]]]
        index = (index + 1) % len(directions)

        if node.endswith(stop):
            break

    return steps_taken


with open("inputs/test.txt") as file:
    nodes, directions = parse(file.read())


print("Part 1")
print("Answer:", solve(nodes, directions))

print("Part 2")
start_nodes = [node for node in nodes if node.endswith("A")]
steps = [
    solve(nodes, directions, start=node, stop="Z") for node in start_nodes
]
print("Answer:", reduce(lcm, steps, 1))
