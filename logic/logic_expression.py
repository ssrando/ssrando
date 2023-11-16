from __future__ import annotations
from typing import Dict, List, Callable, Optional, Set, Tuple
from dataclasses import dataclass
from functools import reduce
from abc import ABC
import re
from itertools import product, combinations

from .inventory import EXTENDED_ITEM, Inventory, EMPTY_INV, DAY_BIT, NIGHT_BIT
from .constants import EXTENDED_ITEM_NAME, number, ITEM_COUNTS, RAW_ITEM_NAMES

GLOBAL_DUMP_MODE = False


class LogicExpression(ABC):
    opaque: bool = False

    def localize(self, localizer: Callable[[str], Optional[str]]) -> LogicExpression:
        raise NotImplementedError

    def eval(self, inventory: Inventory) -> bool:
        raise NotImplementedError

    @staticmethod
    def parse(text: str) -> LogicExpression:
        raise NotImplementedError

    def __or__(self, other) -> DNFInventory:
        return OrCombination([self, other])

    def __and__(self, other) -> DNFInventory:
        return AndCombination([self, other])

    def day_only(self):
        return self & BasicTextAtom("Day")

    def night_only(self):
        return self & BasicTextAtom("Night")


class DNFInventory(LogicExpression):
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
            for conj, conj_pre in other.disjunction.items():
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
            return super().__or__(other)

    def __and__(self, other) -> DNFInventory:
        if isinstance(other, DNFInventory):
            return AndCombination.simplifyDNF([self, other])  # Can be optimised
        else:
            raise super().__and__(other)

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


def InventoryAtom(item_name: str, quantity: int) -> DNFInventory:
    if GLOBAL_DUMP_MODE:
        if quantity == 1:
            return BasicTextAtom(f"{item_name}")
        return BasicTextAtom(f"{item_name} x {quantity}")
    disjunction = set()
    for comb in combinations(range(ITEM_COUNTS[item_name]), quantity):
        i = Inventory()
        for index in comb:
            i |= EXTENDED_ITEM[number(item_name, index)]
        disjunction.add(i)
    return DNFInventory(disjunction)


def EventAtom(event_address: EXTENDED_ITEM_NAME) -> DNFInventory:
    if GLOBAL_DUMP_MODE:
        return BasicTextAtom(str(event_address))
    return DNFInventory(event_address)


@dataclass
class BasicTextAtom(LogicExpression):
    text: str

    def eval(self, *args):
        raise TypeError("Text must be localized to be evaluated.")

    def localize(self, localizer: Callable[[str], EXTENDED_ITEM_NAME | None]):
        if GLOBAL_DUMP_MODE:
            try:
                if (v := localizer(self.text)) is not None:
                    self.text = v
            except ValueError:
                print(self.text)
            return self
        if (v := localizer(self.text)) is None:
            raise ValueError(f"Unknown event {self.text}.")
        else:
            ret = EventAtom(v)
            ret.opaque = self.opaque
            return ret

    def __repr__(self):
        if GLOBAL_DUMP_MODE:
            return self.text
        return f'BasicTextAtom("{self.text}")'


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

    def eval(self, *args):
        raise TypeError(
            f"Some argument of this {type(self).__name__} cannot be evaluated, or something has gone wrong."
        )


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

    def eval(self, *args):
        raise TypeError(
            f"Some argument of this {type(self).__name__} cannot be evaluated, or something has gone wrong."
        )


# Parsing

from lark import Lark, Transformer, v_args

exp_grammar = """
    ?start: disjunction
        | "$" disjunction -> mk_opaque

    ?disjunction: conjunction
        | disjunction "|" conjunction -> mk_or

    ?conjunction: atom
        | conjunction "&" atom -> mk_and

    ?atom: TEXT -> mk_atom
         | "(" disjunction ")"

    TEXT: /[^$|&())]+/

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

    def mk_atom(self, text):
        text = text.strip()
        if text == "Nothing":
            return EventAtom(True)
        if text == "Impossible":
            return EventAtom(False)

        if match := item_with_count_re.search(text):
            item_name = match.group(1)
            if item_name not in RAW_ITEM_NAMES:
                raise ValueError(f"Unknown item {item_name}.")
            return InventoryAtom(item_name, int(match.group(2)))

        elif text in RAW_ITEM_NAMES or text in EXTENDED_ITEM:
            return InventoryAtom(text, 1)

        else:
            return BasicTextAtom(text)


exp_parser = Lark(exp_grammar, parser="lalr", transformer=MakeExpression())
LogicExpression.parse = exp_parser.parse  # type: ignore
