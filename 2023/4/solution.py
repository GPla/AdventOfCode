# %%
from dataclasses import dataclass


@dataclass
class Card:
    id: int
    winners: set[int]
    numbers: set[int]

    @property
    def points(self) -> int:
        return int(2 ** (len(self.winning()) - 1))

    def winning(self) -> set[int]:
        return self.winners.intersection(self.numbers)

    def n_winning(self) -> int:
        return len(self.winning())

    @classmethod
    def parse(cls, input: str) -> "Card":
        id, rest = input.split(":")
        id = int(id.split(" ")[-1])

        winners, numbers = [
            {int(e) for e in s.split(" ") if e.strip()}
            for s in rest.split("|")
        ]

        return Card(id=id, winners=winners, numbers=numbers)


with open("inputs/test.txt", "r") as file:
    cards = [Card.parse(line) for line in file.read().splitlines()]


points = sum(map(lambda card: card.points, cards))

print("Part 1")
print("Answer:", points)


print("Part 2")
copies = {card.id: 1 for card in cards}
for card in cards:
    n_winning = card.n_winning()
    for id in range(card.id + 1, card.id + n_winning + 1):
        copies[id] += copies[card.id]
print("Answer:", sum(copies.values()))
