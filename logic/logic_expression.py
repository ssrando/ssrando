from __future__ import annotations
from typing import Dict, List, Callable, Optional, Set, Tuple
from dataclasses import dataclass
from functools import cached_property, reduce
from abc import ABC
import re
from itertools import product, combinations

from .inventory import EXTENDED_ITEM, Inventory, EMPTY_INV, DAY_BIT, NIGHT_BIT
from .constants import EXTENDED_ITEM_NAME, number, ITEM_COUNTS, RAW_ITEM_NAMES


class LogicExpression(ABC):
    opaque: bool = False

    def localize(self, localizer: Callable[[str], Optional[str]]) -> Requirement:
        raise NotImplementedError

    @staticmethod
    def parse(text: str) -> LogicExpression:
        raise NotImplementedError


class Requirement(LogicExpression):
    def eval(self, inventory: Inventory) -> bool:
        raise NotImplementedError

    def day_only(self) -> Requirement:
        raise NotImplementedError

    def night_only(self) -> Requirement:
        raise NotImplementedError

    def __or__(self, other) -> Requirement:
        raise NotImplementedError

    def __and__(self, other) -> Requirement:
        raise NotImplementedError


class DNFInventory(Requirement):
    disjunction: Dict[Inventory, Inventory]

    def __init__(
        self,
        v: None
        | Set[Inventory]
        | Dict[Inventory, Inventory]
        | bool
        | Inventory
        | EXTENDED_ITEM
        | EXTENDED_ITEM_NAME
        | Tuple[str, int] = None,
    ):

        if v is None:
            self.disjunction = {}
        elif isinstance(v, set):
            self.disjunction = {k: k for k in v}
        elif isinstance(v, bool):
            if v:
                self.disjunction = {EMPTY_INV: EMPTY_INV}
            else:
                self.disjunction = {}
        elif isinstance(v, Inventory):
            self.disjunction = {v: v}
        elif isinstance(v, dict):
            self.disjunction = v
        else:
            inv = Inventory(v)
            self.disjunction = {inv: inv}

    def eval(self, inventory: Inventory):
        return any(req_items <= inventory for req_items in self.disjunction)

    def localize(self, *args):
        return self

    def __or__(self, other) -> DNFInventory:
        if isinstance(other, DNFInventory):
            filtered_self = self.disjunction.copy()
            filtered_other = {}
            for (conj, conj_pre) in other.disjunction.items():
                to_pop = []
                for conj2 in filtered_self:
                    if conj <= conj2 and conj != conj2:
                        conj_pre &= filtered_self[conj2]
                        to_pop.append(conj2)
                    if conj2 <= conj:
                        filtered_self[conj2] &= conj_pre
                        break
                else:
                    for c in to_pop:
                        del filtered_self[c]
                    filtered_other[conj] = conj_pre
            return DNFInventory((filtered_self | filtered_other))
        else:
            raise ValueError

    def __and__(self, other) -> DNFInventory:
        if isinstance(other, DNFInventory):
            return AndCombination.simplifyDNF([self, other])  # Can be optimised
        else:
            raise ValueError

    def __repr__(self) -> str:
        return f"DNFInventory({self.disjunction!r})"

    def remove(self, item):
        if isinstance(item, EXTENDED_ITEM):
            return DNFInventory({inv for inv in self.disjunction if not inv[item]})
        else:
            raise ValueError

    def is_impossible(self):
        return not self.disjunction

    def aggregate(self):
        ag = Inventory()
        for r in self.disjunction:
            ag |= r
        return ag

    def day_only(self):
        return DNFInventory(
            {inv.remove(DAY_BIT) for inv in self.disjunction if not inv[NIGHT_BIT]}
        )

    def night_only(self):
        return DNFInventory(
            {inv.remove(NIGHT_BIT) for inv in self.disjunction if not inv[DAY_BIT]}
        )


@dataclass
class Counter:
    targets: Dict[EXTENDED_ITEM, int]

    def localize(self, *args):
        return self

    def compute(self, inventory: Inventory):
        return sum(v * inventory[k] for k, v in self.targets.items())


@dataclass
class CounterThreshold(Requirement):
    target: EXTENDED_ITEM_NAME
    threshold: int

    @cached_property
    def counter(self) -> Counter:
        return EXTENDED_ITEM.counters[self.target]

    def eval(self, inventory: Inventory):
        return self.counter.compute(inventory) >= self.threshold

    def localize(self, *args):
        return self

    def day_only(self):
        return self

    def night_only(self):
        return self

    def __or__(self, other) -> CounterThreshold:
        if isinstance(other, CounterThreshold) and other.target == self.target:
            return CounterThreshold(self.target, min(self.threshold, other.threshold))
        else:
            raise ValueError

    def __and__(self, other) -> CounterThreshold:
        if isinstance(other, CounterThreshold) and other.target == self.target:
            return CounterThreshold(self.target, max(self.threshold, other.threshold))
        else:
            raise ValueError


class UnknownReq(Requirement):
    def eval(self, inventory: Inventory):
        return False

    def localize(self, *args):
        return self

    def day_only(self):
        return self

    def night_only(self):
        return self

    def __or__(self, other: Requirement) -> Requirement:
        return other

    def __and__(self, other) -> UnknownReq:
        raise ValueError


unknown_req = UnknownReq()


def InventoryAtom(item_name: str, quantity: int) -> Requirement:
    disjunction = set()
    for comb in combinations(range(ITEM_COUNTS[item_name]), quantity):
        i = Inventory()
        for index in comb:
            i |= EXTENDED_ITEM[number(item_name, index)]
        disjunction.add(i)
    return DNFInventory(disjunction)


def EventAtom(event_address: EXTENDED_ITEM_NAME) -> Requirement:
    return DNFInventory(event_address)


@dataclass
class BasicTextAtom(LogicExpression):
    text: str

    def localize(self, localizer: Callable[[str], EXTENDED_ITEM_NAME | None]):
        if (v := localizer(self.text)) is None:
            raise ValueError(f"Unknown event {self.text}")
        else:
            ret = EventAtom(v)
            ret.opaque = self.opaque
            return ret


def and_reducer(v, v1):
    a, b = v
    a1, b1 = v1
    return a | a1, b | b1


@dataclass
class AndCombination(LogicExpression):
    arguments: List[LogicExpression]

    @staticmethod
    def simplifyDNF(arguments: List[DNFInventory]) -> DNFInventory:
        disjunctions = map(lambda x: x.disjunction.items(), arguments)

        new_req = DNFInventory()
        for conjunction_tuple in product(*disjunctions):
            conj, conj_pre = reduce(
                and_reducer, conjunction_tuple, (EMPTY_INV, EMPTY_INV)
            )
            new_req |= DNFInventory(({conj: conj_pre}))
        return new_req

    @staticmethod
    def simplify(arguments: List[LogicExpression]) -> LogicExpression:
        if all(map(lambda x: isinstance(x, DNFInventory), arguments)):
            return AndCombination.simplifyDNF(arguments)  # type: ignore
        else:
            return AndCombination(arguments)

    def localize(self, localizer):
        ret = self.simplify([arg.localize(localizer) for arg in self.arguments])
        ret.opaque = self.opaque
        return ret


@dataclass
class OrCombination(LogicExpression):
    arguments: List[LogicExpression]

    @staticmethod
    def simplifyDNF(arguments: List[DNFInventory]) -> DNFInventory:
        disjunctions = map(lambda x: x.disjunction, arguments)
        bigset = {}
        for s in disjunctions:
            bigset |= s
        return DNFInventory(Inventory.simplify_invset(bigset))

    @staticmethod
    def simplify(arguments: List[LogicExpression]) -> LogicExpression:
        if all(map(lambda x: isinstance(x, DNFInventory), arguments)):
            return OrCombination.simplifyDNF(arguments)  # type: ignore
        else:
            return OrCombination(arguments)

    def localize(self, localizer):
        ret = self.simplify([arg.localize(localizer) for arg in self.arguments])
        ret.opaque = self.opaque
        return ret


# Parsing

from lark import Lark, Transformer, v_args

exp_grammar = r"""
    ?start: disjunction
        | "~" disjunction -> mk_opaque

    ?disjunction: conjunction
        | disjunction "|" conjunction -> mk_or

    ?conjunction: atom
        | conjunction "&" atom -> mk_and

    ?atom:
        | "Nothing" -> mk_true
        | "Impossible" -> mk_false
        | "$" counter -> mk_counter
        | TEXT ">=" INT -> mk_counter_threshold
        | TEXT "*" INT -> mk_atom
        | TEXT -> mk_atom
        | "(" disjunction ")"

    ?counter: counter "+" counter -> mk_counter_add
        | INT ("x" | "*") TEXT -> mk_counter_atom

    TEXT.-100: /\b[^$~|&()>=+]+\b/

    %import common.INT
    %import common.WS
    %ignore WS
"""

item_with_count_re = re.compile(r"^(.+) [x][ ]*(\d+)$")


@v_args(inline=True)  # Affects the signatures of the methods
class MakeExpression(Transformer):
    def mk_opaque(self, exp):
        exp.opaque = True
        return exp

    def mk_or(self, left, right):
        if isinstance(left, OrCombination):
            return OrCombination(left.arguments + [right])
        else:
            return OrCombination([left, right])

    def mk_and(self, left, right):
        if isinstance(left, AndCombination):
            return AndCombination(left.arguments + [right])
        else:
            return AndCombination([left, right])

    def mk_true(self):
        return DNFInventory(True)

    def mk_false(self):
        return DNFInventory(False)

    def mk_atom(self, text, count=None):
        text = text.strip()

        if match := item_with_count_re.search(text):
            text = match.group(1)
            count = match.group(2)

        if count is not None:
            count = int(count)
            if text not in RAW_ITEM_NAMES:
                raise ValueError(f"Unknown item {text}")
            return InventoryAtom(text, count)

        elif text in RAW_ITEM_NAMES or text in EXTENDED_ITEM:
            return InventoryAtom(text, 1)

        else:
            return BasicTextAtom(text)

    def mk_counter_atom(self, count, item):
        count = int(count)
        if item not in RAW_ITEM_NAMES and item not in EXTENDED_ITEM:
            raise ValueError(f"Unknown item {item}")
        if item in EXTENDED_ITEM:
            return {EXTENDED_ITEM[item]: count}
        return {
            EXTENDED_ITEM[number(item, index)]: count
            for index in range(ITEM_COUNTS[item])
        }

    def mk_counter_add(self, left, right):
        return left | right

    def mk_counter(self, counter):
        return Counter(counter)

    def mk_counter_threshold(self, counter_name, threshold):
        c = CounterThreshold(counter_name, int(threshold))
        c.opaque = True
        return c


exp_parser = Lark(exp_grammar, parser="lalr", transformer=MakeExpression())
LogicExpression.parse = exp_parser.parse  # type: ignore
