from __future__ import annotations
from typing import Set, List, Tuple

from yaml_files import options
from .constants import *


def extended_item_generator():
    yield from ["Day", "Night"]  # Dummy events, will be removed from the requirements
    yield from ["Banned", EVERYTHING, "Everything unbanned", "Hint bypass"]
    # Technical dummy events
    yield from sorted(INVENTORY_ITEMS)

    yield from LOGIC_OPTIONS

    for option in options:
        if option["name"].startswith("Enabled Tricks"):
            for trick in option["choices"]:
                yield f"{trick} Trick"

    for i in range(MAX_STONE_HINTS + MAX_FI_HINTS):
        yield number(HINT, i)


class MetaContainer(type):
    def __getitem__(self, arg):
        return self.getitem(arg)  # type: ignore

    def __len__(self):
        return self.len()  # type: ignore

    def __iter__(self):
        return self.iter()  # type: ignore


class EXTENDED_ITEM(int, metaclass=MetaContainer):
    items_list: List[EXTENDED_ITEM_NAME] = list(extended_item_generator())  # type: ignore
    complete = False

    @classmethod
    def items(cls):
        for i in range(len(cls)):
            yield cls(i)

    @classmethod
    def len(cls):
        return len(cls.items_list)

    @classmethod
    def iter(cls):
        return iter(cls.items_list)

    @classmethod
    def getitem(cls, name: EXTENDED_ITEM_NAME) -> EXTENDED_ITEM:
        return cls(cls.items_list.index(name))

    @classmethod
    def get_item_name(cls, i: EXTENDED_ITEM) -> EXTENDED_ITEM_NAME:
        return cls.items_list[i]

    def __str__(self) -> str:
        return super().__repr__() + f" ({self.items_list[self]})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({super().__repr__()})"


class Inventory:
    bitset: int
    intset: Set[EXTENDED_ITEM]

    def __init__(
        self,
        v: (
            None
            | Tuple[int, Set[EXTENDED_ITEM]]
            | Tuple[str, int]
            | EXTENDED_ITEM_NAME
            | Set[EXTENDED_ITEM]
            | EXTENDED_ITEM
            | Inventory
        ) = None,
    ):
        if v is None:
            self.bitset = 0
            self.intset = set()
        elif isinstance(v, Inventory):
            self.bitset = v.bitset
            self.intset = v.intset
        elif isinstance(v, set):
            bitset = 0
            for item in v:
                bitset += 1 << item
            self.intset = v
            self.bitset = bitset
        elif isinstance(v, EXTENDED_ITEM):
            self.bitset = 1 << v
            self.intset = {v}
        elif isinstance(v, str):
            bit = EXTENDED_ITEM[v]
            self.bitset = 1 << bit
            self.intset = {bit}
        elif isinstance(v, tuple):  # Item, count
            item, count = v
            if isinstance(item, int):  # bitset, intset
                assert isinstance(count, set)
                self.bitset = item
                self.intset = count
            else:
                assert isinstance(count, int)
                assert count <= ITEM_COUNTS[item]
                if ITEM_COUNTS[item] == 1:
                    bit = EXTENDED_ITEM[item]
                    self.bitset = 1 << bit
                    self.intset = {bit}
                else:
                    self.bitset = 0
                    self.intset = set()
                    for i in range(count):
                        bit = EXTENDED_ITEM[number(item, i)]
                        self.bitset |= 1 << bit
                        self.intset.add(bit)
        else:
            raise ValueError

    def __getitem__(self, index):
        if isinstance(index, EXTENDED_ITEM):
            return bool(self.bitset & (1 << index))
        else:
            raise ValueError

    def __or__(self, other):
        if isinstance(other, EXTENDED_ITEM):
            return Inventory((self.bitset | (1 << other), self.intset | {other}))
        elif isinstance(other, Inventory):
            return Inventory((self.bitset | other.bitset, self.intset | other.intset))
        else:
            raise ValueError

    def __and__(self, other):
        if isinstance(other, Inventory):
            return Inventory((self.bitset & other.bitset, self.intset & other.intset))
        else:
            raise ValueError

    def __sub__(self, other):
        if isinstance(other, EXTENDED_ITEM):
            return Inventory((self.bitset & ~(1 << other), self.intset - {other}))
        elif isinstance(other, Inventory):
            return Inventory((self.bitset & ~other.bitset, self.intset - other.intset))
        else:
            raise ValueError

    def __le__(self, other):
        """Define inclusion"""
        return self.intset.issubset(other.intset)

    def __eq__(self, other):
        return self.intset == other.intset

    def __hash__(self):
        return hash(self.bitset)

    def __iter__(self):
        return iter(self.intset)

    def __repr__(self) -> str:
        return f"Inventory({self.intset!r})"

    def add(self, item: EXTENDED_ITEM | str):
        if isinstance(item, EXTENDED_ITEM) or isinstance(item, Inventory):
            return self | item
        elif isinstance(item, str):
            if ITEM_COUNTS[item] == 1 and not self[(item_bit := EXTENDED_ITEM[item])]:
                return self | item_bit
            else:
                for i in range(ITEM_COUNTS[item]):
                    if not self[(item_bit := EXTENDED_ITEM[number(item, i)])]:
                        return self | item_bit
        raise ValueError

    def remove(self, item: EXTENDED_ITEM | str):
        if isinstance(item, EXTENDED_ITEM):
            return Inventory(
                (self.bitset & ~(1 << item), self.intset.difference({item}))
            )
        elif isinstance(item, str):
            for i in reversed(range(ITEM_COUNTS[item])):
                if self[(item_bit := EXTENDED_ITEM[number(item, i)])]:
                    return Inventory(
                        (
                            self.bitset & ~(1 << item_bit),
                            self.intset.difference({item_bit}),
                        )
                    )
            else:
                raise ValueError(f"{item} not in inventory.")
        raise ValueError(item)

    def intersects(self, other: Inventory) -> bool:
        return bool(self & other)

    @staticmethod
    def simplify_invset(argset):
        def gen():
            for bitset in argset:
                for bitset2 in argset:
                    if bitset2 <= bitset and bitset2 != bitset:
                        break
                else:
                    yield bitset

        return set(gen())

    def all_owned_unique_items(self):
        return set(
            (
                (v := item.name)[: v.index("#") - 1]
                for item in EXTENDED_ITEM
                if self[item]
            )
        )


BANNED = EIN("Banned")

EMPTY_INV = Inventory()
DAY_BIT: EXTENDED_ITEM = EXTENDED_ITEM["Day"]
NIGHT_BIT: EXTENDED_ITEM = EXTENDED_ITEM["Night"]
BANNED_BIT: EXTENDED_ITEM = EXTENDED_ITEM[BANNED]
EVERYTHING_BIT: EXTENDED_ITEM = EXTENDED_ITEM["Everything"]
EVERYTHING_UNBANNED_BIT: EXTENDED_ITEM = EXTENDED_ITEM["Everything unbanned"]
HINT_BYPASS_BIT: EXTENDED_ITEM = EXTENDED_ITEM["Hint bypass"]
