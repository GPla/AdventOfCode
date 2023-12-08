# %%

from dataclasses import dataclass
from enum import Enum
from functools import total_ordering, lru_cache
from typing import Literal, get_args, Any, Callable
from collections import Counter
import operator

CARDS = ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2")
CARDS_JOKER = ("A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J")


class HandType(Enum):
    FiveKind = 0
    FourKind = 1
    FullHouse = 2
    ThreeKind = 3
    TwoPair = 4
    OnePair = 5
    High = 6

    @classmethod
    def get(cls, cards: str):
        if (n_cards := len(cards)) != 5:
            raise ValueError(f"Expected 5 cards, but got {n_cards}.")

        counts = Counter(cards)
        match [len(counts), max(counts.values())]:
            case [1, *_]:
                return HandType.FiveKind
            case [2, 4]:
                return HandType.FourKind
            case [2, 3]:
                return HandType.FullHouse
            case [3, 3]:
                return HandType.ThreeKind
            case [3, *_]:
                return HandType.TwoPair
            case [4, *_]:
                return HandType.OnePair
            case [5, *_]:
                return HandType.High
            case _:
                raise ValueError(f"Invalid Hand '{cards}'.")


class Hand:
    def __init__(self, *, cards: str, bid: int, with_joker: bool = False):
        self.cards = cards
        self.bid = bid

        self.type = HandType.get(
            cards if not with_joker else self._substitute_joker(cards)
        )
        CARD_ORDER = CARDS if not with_joker else CARDS_JOKER
        self.indexes = [CARD_ORDER.index(card) for card in cards]

    def _substitute_joker(self, cards: str) -> str:
        counts = Counter(cards.replace("J", ""))
        if not counts:
            return "AAAAA"
        best = counts.most_common(1)[0][0]
        return cards.replace("J", best)

    def _valid_operator(self, other):
        if not isinstance(other, Hand):
            raise NotImplementedError()

    def _compare(self, other: "Hand", op: Callable[[Any, Any], bool]):
        if self.type != other.type:
            return op(self.type.value, other.type.value)

        for left, right in zip(self.indexes, other.indexes):
            if left != right:
                return op(left, right)
        return False

    def __gt__(self, other: Any) -> bool:
        self._valid_operator(other)
        return self._compare(other, operator.gt)

    def __lt__(self, other: Any) -> bool:
        self._valid_operator(other)
        return self._compare(other, operator.lt)

    def __eq__(self, other: Any) -> bool:
        self._valid_operator(other)
        return self.type == other.type and self.cards == other.cards

    def __str__(self) -> str:
        return f"Hand(cards={self.cards}, bid={self.bid})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def parse(cls, line: str, with_joker: bool = False):
        cards, bid = line.split(" ")
        return Hand(cards=cards, bid=int(bid), with_joker=with_joker)


with open("inputs/test.txt") as file:
    lines = file.read().splitlines()


print("Part 1")
hands = [Hand.parse(line) for line in lines]
sorted_hands = sorted(hands, reverse=True)
winnings = [hand.bid * rank for rank, hand in enumerate(sorted_hands, 1)]
print("Answer:", sum(winnings))

print("Part 2")
hands = [Hand.parse(line, with_joker=True) for line in lines]
sorted_hands = sorted(hands, reverse=True)
winnings = [hand.bid * rank for rank, hand in enumerate(sorted_hands, 1)]
print("Answer:", sum(winnings))
