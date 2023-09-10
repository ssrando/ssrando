from __future__ import annotations
from typing import Any, List
from dataclasses import dataclass
from options import Options


class BoolExpression:
    def eval(self, options: Options) -> bool:
        raise NotImplementedError

    @staticmethod
    def parse(text: str) -> BoolExpression:
        raise NotImplementedError


@dataclass
class QueryBoolOption(BoolExpression):
    option: str
    negation: bool = False

    def eval(self, options: Options) -> bool:
        if self.negation:
            return not options[self.option]
        return options[self.option]


@dataclass
class QueryOption(BoolExpression):
    option: str
    value: Any
    negation: bool = False

    def eval(self, options: Options) -> bool:
        if self.negation:
            return options[self.option] != self.value
        return options[self.option] == self.value


@dataclass
class QueryLessThanOption(BoolExpression):
    option: str
    threshold: int
    negation: bool = False

    def eval(self, options: Options) -> bool:
        if self.negation:
            return options[self.option] >= self.threshold
        return options[self.option] < self.threshold


@dataclass
class QueryGreaterThanOption(BoolExpression):
    option: str
    threshold: int
    negation: bool = False

    def eval(self, options: Options) -> bool:
        if self.negation:
            return options[self.option] <= self.threshold
        return options[self.option] > self.threshold


@dataclass
class QueryContainerOption(BoolExpression):
    option: str
    value: Any
    negation: bool = False

    def eval(self, options: Options) -> bool:
        if self.negation:
            return self.value not in options[self.option]
        return self.value in options[self.option]


@dataclass
class AndCombination(BoolExpression):
    arguments: List[BoolExpression]

    def eval(self, options: Options) -> bool:
        return all(arg.eval(options) for arg in self.arguments)


@dataclass
class OrCombination(BoolExpression):
    arguments: List[BoolExpression]

    def eval(self, options: Options) -> bool:
        return any(arg.eval(options) for arg in self.arguments)


# Parsing

from lark import Lark, Transformer, v_args

exp_grammar = r"""
    ?start: disjunction

    ?disjunction: conjunction
        | disjunction "|" conjunction -> mk_or

    ?conjunction: atom
        | conjunction "&" atom -> mk_and

    ?atom:
         | "(" disjunction ")"
         | "true" -> mk_true
         | "false" -> mk_false
         | "Nothing" -> mk_true
         | "Option" text "Enabled" -> mk_enabled
         | "Option" text "Disabled" -> mk_disabled
         | "Option" text "Is" text -> mk_is
         | "Option" text "Is Not" text -> mk_isnot
         | "Option" text "Is Less Than" text -> mk_islt
         | "Option" text "Is Greater Than" text -> mk_isgt
         | "Option" text "Contains" text -> mk_contains
         | "Option" text "Does Not Contain" text -> mk_doesnotcontain


    ?text: "\"" TEXT "\""

    TEXT: /[^"]+/

    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
"""


@v_args(inline=True)  # Affects the signatures of the methods
class MakeExpression(Transformer):
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

    def mk_islt(self, option, threshold):
        return QueryLessThanOption(str(option), int(threshold))

    def mk_isgt(self, option, threshold):
        return QueryGreaterThanOption(str(option), int(threshold))

    def mk_contains(self, option, value):
        return QueryContainerOption(option, value)

    def mk_doesnotcontain(self, option, value):
        return QueryContainerOption(option, value, negation=True)


exp_parser = Lark(exp_grammar, parser="lalr", transformer=MakeExpression())
BoolExpression.parse = exp_parser.parse  # type: ignore


def check_static_option_req(string, options):
    return BoolExpression.parse(string).eval(options)
