from typing import List, Tuple, NewType, DefaultDict, Dict
from collections import OrderedDict, defaultdict
import re

from .item_types import ALL_ITEM_NAMES
from options import Options


LocationName = NewType("LocationName", str)
ItemName = NewType("ItemName", str)


class Inventory:
    def __init__(self):
        self.owned_items: DefaultDict[str, int] = defaultdict(int)

    def copy(self):
        inv = Inventory()
        inv.owned_items = self.owned_items.copy()
        return inv

    def has_item(self, item):
        return self.owned_items.get(item, 0) >= 1

    def has_countable_item(self, item, count):
        return self.owned_items.get(item, 0) >= count

    def collect_item(self, item):
        # TODO: progress item groups
        self.owned_items[item] += 1

    def remove_item(self, item):
        # TODO: progress item groups
        if self.owned_items[item] >= 1:
            self.owned_items[item] -= 1

    def all_owned_unique_items(self):
        return set((item for item, count in self.owned_items.items() if count >= 1))

    def __str__(self):
        return str(self.owned_items)


def check_option_enabled_requirement(options, req_name):
    positive_boolean_match = re.search(r"^Option \"([^\"]+)\" Enabled$", req_name)
    negative_boolean_match = re.search(r"^Option \"([^\"]+)\" Disabled$", req_name)
    positive_dropdown_match = re.search(
        r"^Option \"([^\"]+)\" Is \"([^\"]+)\"$", req_name
    )
    negative_dropdown_match = re.search(
        r"^Option \"([^\"]+)\" Is Not \"([^\"]+)\"$", req_name
    )
    positive_list_match = re.search(
        r"^Option \"([^\"]+)\" Contains \"([^\"]+)\"$", req_name
    )
    negative_list_match = re.search(
        r"^Option \"([^\"]+)\" Does Not Contain \"([^\"]+)\"$", req_name
    )
    if positive_boolean_match:
        option_name = positive_boolean_match.group(1)
        return not not options.get(option_name)
    elif negative_boolean_match:
        option_name = negative_boolean_match.group(1)
        return not options.get(option_name)
    elif positive_dropdown_match:
        option_name = positive_dropdown_match.group(1)
        value = positive_dropdown_match.group(2)
        return options.get(option_name) == value
    elif negative_dropdown_match:
        option_name = negative_dropdown_match.group(1)
        value = negative_dropdown_match.group(2)
        return options.get(option_name) != value
    elif positive_list_match:
        option_name = positive_list_match.group(1)
        value = positive_list_match.group(2)
        return value in options.get(option_name, [])
    elif negative_list_match:
        option_name = negative_list_match.group(1)
        value = negative_list_match.group(2)
        return value not in options.get(option_name, [])
    else:
        raise Exception("Invalid option check requirement: %s" % req_name)


ITEM_WITH_COUNT_REGEX = re.compile(r"^(.+) x(\d+)$")


class LogicExpression:
    def is_true(self, options: Options, inventory: Inventory, macros):
        raise NotImplementedError("abstract")

    def get_items_needed(
        self, options: Options, inventory: Inventory, macros
    ) -> OrderedDict:  # itemname -> count
        raise NotImplementedError("abstract")

    def __str__(self):
        raise NotImplementedError("abstract")


class BaseLogicExpression(LogicExpression):
    def __init__(self, req_name):
        self.req_name = req_name

    def is_true(self, options: Options, inventory: Inventory, macros):
        match = ITEM_WITH_COUNT_REGEX.match(self.req_name)
        if match:
            item_name = match.group(1)
            num_required = int(match.group(2))

            return inventory.has_countable_item(item_name, num_required)
        elif self.req_name.startswith('Option "'):
            return check_option_enabled_requirement(options, self.req_name)
        elif self.req_name.endswith(" Trick"):
            trickname = self.req_name[: -len(" Trick")]
            if options["logic-mode"] == "BiTless":
                self.req_name = (
                    f'Option "enabled-tricks-bitless" Contains "{trickname}"'
                )
            else:
                self.req_name = (
                    f'Option "enabled-tricks-glitched" Contains "{trickname}"'
                )
            return check_option_enabled_requirement(options, self.req_name)
        elif self.req_name in ALL_ITEM_NAMES:
            return inventory.has_item(self.req_name)
        elif self.req_name in macros:
            return macros[self.req_name].is_true(options, inventory, macros)
        elif self.req_name == "Nothing":
            return True
        elif self.req_name == "Impossible":
            return False
        else:
            raise Exception("Unknown requirement name: " + self.req_name)

    def get_items_needed(
        self, options: Options, inventory: Inventory, macros
    ) -> OrderedDict:  # itemname, count
        if self.is_true(
            options, inventory, macros
        ):  # don't include items if this is already met
            return OrderedDict()
        match = ITEM_WITH_COUNT_REGEX.match(self.req_name)
        if match:
            item_name = match.group(1)
            num_required = int(match.group(2))

            items_needed = OrderedDict({item_name: num_required})
        elif self.req_name in ALL_ITEM_NAMES:
            items_needed = OrderedDict({self.req_name: 1})
        elif self.req_name in macros:
            items_needed = macros[self.req_name].get_items_needed(
                options, inventory, macros
            )
        else:
            items_needed = None  # unreachable

        return items_needed

    def __str__(self):
        return self.req_name


class AndLogicExpression(LogicExpression):
    def __init__(self, requirements: List[LogicExpression]):
        self.requirements = requirements
        self.recursion_flag = False

    def is_true(self, options: Options, inventory: Inventory, macros):
        if self.recursion_flag:
            res = False
        else:
            self.recursion_flag = True
            res = all(
                (req.is_true(options, inventory, macros) for req in self.requirements)
            )
            self.recursion_flag = False
        return res

    def __str__(self):
        return "(" + (" & ".join((str(req) for req in self.requirements))) + ")"

    def get_items_needed(
        self, options: Options, inventory: Inventory, macros
    ) -> OrderedDict:  # itemname, count
        items_needed = OrderedDict()
        if self.recursion_flag:
            items_needed = None
        else:
            self.recursion_flag = True
            for subresult in (
                req.get_items_needed(options, inventory, macros)
                for req in self.requirements
            ):
                if subresult is None:  # if one is unreachable, all of this is
                    items_needed = None
                    break
                for item_name, num_required in subresult.items():
                    items_needed[item_name] = max(
                        num_required, items_needed.setdefault(item_name, 0)
                    )
            self.recursion_flag = False

        return items_needed


class OrLogicExpression(LogicExpression):
    def __init__(self, requirements: List[LogicExpression]):
        self.requirements = requirements
        self.recursion_flag = False

    def is_true(self, options: Options, inventory: Inventory, macros):
        if self.recursion_flag:
            res = False
        else:
            self.recursion_flag = True
            res = any(
                (req.is_true(options, inventory, macros) for req in self.requirements)
            )
            self.recursion_flag = False
        return res

    def __str__(self):
        return "(" + (" | ".join((str(req) for req in self.requirements))) + ")"

    def get_items_needed(
        self, options: Options, inventory: Inventory, macros
    ) -> OrderedDict:  # itemname, count
        items_needed = OrderedDict()
        if self.recursion_flag:
            items_needed = None
        else:
            self.recursion_flag = True
            for subresult in (
                req.get_items_needed(options, inventory, macros)
                for req in self.requirements
            ):
                if (
                    subresult == OrderedDict()
                ):  # if one is reachable without items, return not items
                    self.recursion_flag = False
                    return OrderedDict()
                if subresult == None:
                    continue
                for (
                    item_name,
                    num_required,
                ) in subresult.items():  # This seems very wrong
                    items_needed[item_name] = max(
                        num_required, items_needed.setdefault(item_name, 0)
                    )
            self.recursion_flag = False

        return (
            items_needed if items_needed else None
        )  # If the dict is still empty, then no-one subresult filled it, so it is impossible


def find_closing_parenthesis(tokens: List[str], start: int) -> int:
    assert tokens[start] == "("
    nesting_lvl = 1
    pos = start + 1
    while nesting_lvl > 0 and pos < len(tokens):
        char = tokens[pos]
        if char == "(":
            nesting_lvl += 1
        elif char == ")":
            nesting_lvl -= 1
        pos += 1
    if nesting_lvl != 0:
        raise Exception("parenthesis never closed!")
    return pos - 1


def parse_logic_expression(expression: str) -> LogicExpression:
    tokens = [str.strip() for str in re.split("([&|()])", expression)]
    tokens = [token for token in tokens if token != ""]

    return parse_logic_token_expr(tokens)


def parse_logic_token_expr(tokens: List[str]) -> LogicExpression:
    pos = 0
    logic_type = None  # can be 'or' or 'and'
    parsed = []
    while pos < len(tokens):
        cur_token = tokens[pos]
        if cur_token == "(":
            end = find_closing_parenthesis(tokens, pos)
            parsed.append(parse_logic_token_expr(tokens[pos + 1 : end]))
            pos = end + 1
        elif cur_token == "&":
            if logic_type == "or":
                raise Exception("mixed '&' and '|'!")
            else:
                logic_type = "and"
            pos += 1
        elif cur_token == "|":
            if logic_type == "and":
                raise Exception("mixed '&' and '|'!")
            else:
                logic_type = "or"
            pos += 1
        else:
            parsed.append(BaseLogicExpression(cur_token))
            pos += 1
    if logic_type == None:
        assert len(parsed) == 1
        return parsed[0]
    elif logic_type == "and":
        return AndLogicExpression(parsed)
    elif logic_type == "or":
        return OrLogicExpression(parsed)
    else:
        raise Exception(logic_type)


def test():
    import yaml

    with open("SS Rando Logic - Item Location.yaml") as f:
        locations = yaml.safe_load(f)
    for loc in locations:
        req_str = locations[loc]["Need"]
        print()
        print(req_str)
        print(str(parse_logic_expression(req_str)))
