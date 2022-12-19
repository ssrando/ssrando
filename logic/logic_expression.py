from __future__ import annotations
from typing import Any, Dict, List, Callable, Optional, Set, Tuple
from dataclasses import dataclass, field, replace
from functools import cached_property, reduce
from abc import ABC
import re
from itertools import product, combinations

from .inventory import (
    BANNED_BIT,
    EXTENDED_ITEM,
    Inventory,
    EMPTY_INV,
    DAY_BIT,
    NIGHT_BIT,
)
from .constants import EXTENDED_ITEM_NAME, number, ITEM_COUNTS, RAW_ITEM_NAMES
from options import Options


def singleton(cls):
    instance = None

    new = cls.__new__

    def _singleton(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = new(*args, **kwargs)
        return instance

    cls.__new__ = _singleton

    return cls


class QueryExpression:
    else_banned: bool = False

    def eval(self, options: Options) -> bool:
        raise NotImplementedError

    def with_options(self, options):
        if self.eval(options):
            return EmptyReq()
        elif self.else_banned:
            return DNFInventory(BANNED_BIT)
        else:
            return ImpossibleReq()

    @staticmethod
    def parse(text: str) -> QueryExpression:
        raise NotImplementedError


def QueryElseBanned(query: QueryExpression) -> QueryExpression:
    query.else_banned = True
    return query


@dataclass
class MetaQuery(QueryExpression):
    query: QueryExpression

    def __post_init__(self):
        assert isinstance(self.query, (QueryOption, QueryContainerOption))
        self.option = self.query.option
        self.pattern = self.query.value

    def to_query(self, val):
        return replace(self.query, value=self.pattern.format(val))


@dataclass
class QueryBoolOption(QueryExpression):
    option: str
    negation: bool = False

    def eval(self, options: Options) -> bool:
        if self.negation:
            return not options[self.option]
        return options[self.option]


@dataclass
class QueryOption(QueryExpression):
    option: str
    value: Any
    negation: bool = False

    def eval(self, options: Options) -> bool:
        if self.negation:
            return options[self.option] != self.value
        return options[self.option] == self.value


@dataclass
class QueryContainerOption(QueryExpression):
    option: str
    value: Any
    negation: bool = False

    def eval(self, options: Options) -> bool:
        if self.negation:
            return self.value not in options[self.option]
        return self.value in options[self.option]


@dataclass
class QueryAndCombination(QueryExpression):
    arguments: List[QueryExpression]

    def eval(self, options: Options):
        all(arg.eval(options) for arg in self.arguments)


@dataclass
class QueryOrCombination(QueryExpression):
    arguments: List[QueryExpression]

    def eval(self, options: Options):
        any(arg.eval(options) for arg in self.arguments)


# Parsing

from lark import Lark, Transformer, v_args

query_grammar = r"""
    ?start: disjunction
        | "Meta" disjunction -> mk_meta

    ?disjunction: conjunction
        | disjunction "|" conjunction -> mk_or

    ?conjunction: atom
        | conjunction "&" atom -> mk_and

    ?atom:
        | "(" disjunction ")"
        | "true" -> mk_true
        | "false" -> mk_false
        | "Option" option
        | "Option" option "Else" "Banned" -> mk_else_banned

    ?option:
        | text "Enabled" -> mk_enabled
        | text "Disabled" -> mk_disabled
        | text "Is" text -> mk_is
        | text "Is Not" text -> mk_isnot
        | text "Contains" text -> mk_contains
        | text "Does Not Contain" text -> mk_doesnotcontain


    ?text: "\"" TEXT "\""

    TEXT: /[^"]+/

    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
"""


@v_args(inline=True)  # Affects the signatures of the methods
class MakeQueryExpression(Transformer):
    def mk_meta(self, query):
        return MetaQuery(query)

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
        return AndCombination([])

    def mk_false(self):
        return OrCombination([])

    def mk_enabled(self, option):
        return QueryBoolOption(option)

    def mk_disabled(self, option):
        return QueryBoolOption(option, negation=True)

    def mk_is(self, option, value):
        return QueryOption(option, value)

    def mk_isnot(self, option, value):
        return QueryOption(option, value, negation=True)

    def mk_contains(self, option, value):
        return QueryContainerOption(option, value)

    def mk_doesnotcontain(self, option, value):
        return QueryContainerOption(option, value, negation=True)

    def mk_else_banned(self, query):
        return QueryElseBanned(query)


query_parser = Lark(query_grammar, parser="lalr", transformer=MakeQueryExpression())
QueryExpression.parse = query_parser.parse  # type: ignore


def check_static_option_req(string, options):
    return QueryExpression.parse(string).eval(options)


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
    disjunction: Set[Inventory]

    def __init__(
        self,
        v: None
        | Set[Inventory]
        | bool
        | Inventory
        | EXTENDED_ITEM
        | EXTENDED_ITEM_NAME
        | Tuple[str, int] = None,
    ):

        if v is None:
            self.disjunction = set()
        elif isinstance(v, set):
            self.disjunction = v
        elif isinstance(v, bool):
            if v:
                self.disjunction = {EMPTY_INV}
            else:
                self.disjunction = set()
        elif isinstance(v, Inventory):
            self.disjunction = {v}
        else:
            inv = Inventory(v)
            self.disjunction = {inv}

    def eval(self, inventory: Inventory):
        return any(req_items <= inventory for req_items in self.disjunction)

    def localize(self, *args):
        return self

    def __or__(self, other) -> DNFInventory:
        if isinstance(other, DNFInventory):
            filtered_self = self.disjunction.copy()
            filtered_other = set()
            for conj in other.disjunction:
                to_pop = []
                for conj2 in filtered_self:
                    if conj <= conj2 and conj != conj2:
                        to_pop.append(conj2)
                    if conj2 <= conj:
                        break
                else:
                    for c in to_pop:
                        filtered_self.remove(c)
                    filtered_other.add(conj)
            return DNFInventory(filtered_self | filtered_other)
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
class CounterThreshold(Requirement):
    target: EXTENDED_ITEM_NAME
    threshold: int

    @cached_property
    def counter(self) -> Counter:
        return EXTENDED_ITEM.counters[self.target]

    def eval(self, inventory: Inventory):
        val = self.counter.compute(inventory)
        if val > self.counter.limit and not inventory[BANNED_BIT]:
            val = self.counter.limit
        return val >= self.threshold

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


@singleton
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

    def __repr__(self) -> str:
        return f"UnknownReq()"


@singleton
class EmptyReq(DNFInventory):
    disjunction: Set[Inventory] = {EMPTY_INV}

    def __init__(self):
        return

    def eval(self, inventory: Inventory):
        return True

    def localize(self, *args):
        return self

    def __or__(self, other) -> DNFInventory:
        if isinstance(other, DNFInventory):
            return self
        else:
            raise ValueError

    def __and__(self, other) -> DNFInventory:
        if isinstance(other, DNFInventory):
            return other
        else:
            raise ValueError

    def __repr__(self) -> str:
        return f"EmptyReq()"

    def remove(self, item):
        if isinstance(item, EXTENDED_ITEM):
            return self
        else:
            raise ValueError

    def is_impossible(self):
        return False

    def aggregate(self):
        return EMPTY_INV

    def day_only(self):
        return self

    def night_only(self):
        return self


@singleton
class ImpossibleReq(DNFInventory):
    disjunction: Set[Inventory] = set()

    def __init__(self):
        return

    def eval(self, inventory: Inventory):
        return False

    def localize(self, *args):
        return self

    def __or__(self, other) -> DNFInventory:
        if isinstance(other, DNFInventory):
            return other
        else:
            raise ValueError

    def __and__(self, other) -> DNFInventory:
        if isinstance(other, DNFInventory):
            return self
        else:
            raise ValueError

    def __repr__(self) -> str:
        return f"ImpossibleReq()"

    def remove(self, item):
        raise ValueError

    def is_impossible(self):
        return True

    def aggregate(self):
        raise ValueError

    def day_only(self):
        return self

    def night_only(self):
        return self


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


@dataclass
class AndCombination(LogicExpression):
    arguments: List[LogicExpression]

    @staticmethod
    def simplifyDNF(arguments: List[DNFInventory]) -> DNFInventory:
        disjunctions = map(lambda x: x.disjunction, arguments)

        new_req = DNFInventory()
        for conjunction_tuple in product(*disjunctions):
            conj = reduce(Inventory.__or__, conjunction_tuple, EMPTY_INV)
            new_req |= DNFInventory({conj})
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
        bigset = set()
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
        | "Runtime" -> mk_unknown
        | TEXT ">=" INT -> mk_counter_threshold
        | TEXT "*" INT -> mk_atom
        | TEXT -> mk_atom
        | "(" disjunction ")"

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
        return EmptyReq()

    def mk_false(self):
        return ImpossibleReq()

    def mk_unknown(self):
        return UnknownReq()

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

    def mk_counter_threshold(self, counter_name, threshold):
        c = CounterThreshold(counter_name, int(threshold))
        c.opaque = True
        return c


exp_parser = Lark(exp_grammar, parser="lalr", transformer=MakeExpression())
LogicExpression.parse = exp_parser.parse  # type: ignore


@dataclass
class Counter:
    targets: List[Tuple[Set[EXTENDED_ITEM], Callable[[int], int]]]
    limit: int | float

    def compute(self, inventory: Inventory):
        return sum(c(sum(inventory[k] for k in s)) for s, c in self.targets)

    def with_options(self, options: Options):
        pass

    @staticmethod
    def parse(text: str) -> Counter:
        raise NotImplementedError


@dataclass
class CounterLimitOption(Counter):
    limit: int | float = field(init=False)
    option: str
    interpret: Callable[[Any], int | float]

    def with_options(self, options: Options):
        self.limit = self.interpret(options[self.option])


counter_grammar = r"""
    ?start: counter ("," "Limit" int_expr)? -> mk_counter

    ?int_expr:
        | INT -> mk_int
        | "Option" text -> mk_int_option
        | "Option" text "{" (assoc_pair ("," assoc_pair)*) "}" -> mk_any_option

    ?assoc_pair: text "->" INT -> mk_pair

    ?counter: counter "+" counter -> mk_counter_add
        | INT ("x" | "*") TEXT -> mk_counter_atom1
        | TEXT "{" (INT ("," INT)*) "}" -> mk_counter_atom2

    ?text: "\"" TEXT "\""

    TEXT.-100: /\b[^$~|&()>=+,{}]+\b/

    %import common.INT
    %import common.WS
    %ignore WS
"""


@v_args(inline=True)  # Affects the signatures of the methods
class MakeCounter(Transformer):
    def mk_pair(self, a, b):
        return (str(a), int(b))

    def mk_counter_atom(self, item, c):
        if item not in RAW_ITEM_NAMES and item not in EXTENDED_ITEM:
            raise ValueError(f"Unknown item {item}")
        if item in EXTENDED_ITEM:
            return [({EXTENDED_ITEM[item]}, c)]
        s = {EXTENDED_ITEM[number(item, index)] for index in range(ITEM_COUNTS[item])}
        return [(s, c)]

    def mk_counter_atom1(self, count, item):
        count = int(count)
        c = lambda n: count * n
        return self.mk_counter_atom(item, c)

    def mk_counter_atom2(self, item, *counts):
        counts_dict = {i: int(count) for i, count in enumerate(counts)}
        c = lambda n: counts_dict[n]
        return self.mk_counter_atom(item, c)

    def mk_counter_add(self, left, right):
        return left + right

    def mk_int(self, i):
        return int(i)

    def mk_int_option(self, option):
        return str(option), lambda n: n

    def mk_any_option(self, option, *pairs):
        return str(option), lambda v: dict(pairs)[v]

    def mk_counter(self, counter, limit=None):
        if limit is None:
            return Counter(counter, float("inf"))

        elif isinstance(limit, int):
            return Counter(counter, limit)

        else:
            return CounterLimitOption(counter, *limit)


counter_parser = Lark(counter_grammar, parser="lalr", transformer=MakeCounter())
Counter.parse = counter_parser.parse  # type: ignore
