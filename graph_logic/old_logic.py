import re

from options import Options


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
    def is_true(self, options: Options):
        raise NotImplementedError("abstract")

    def __str__(self):
        raise NotImplementedError("abstract")


class BaseLogicExpression(LogicExpression):
    def __init__(self, req_name):
        self.req_name = req_name

    def is_true(self, options: Options):
        if self.req_name.startswith('Option "'):
            return check_option_enabled_requirement(options, self.req_name)
        elif self.req_name == "Nothing":
            return True
        elif self.req_name == "Impossible":
            return False
        else:
            raise Exception("Unknown requirement name: " + self.req_name)

    def __str__(self):
        return self.req_name


class AndLogicExpression(LogicExpression):
    def __init__(self, requirements):
        self.requirements = requirements
        self.recursion_flag = False

    def is_true(self, options: Options):
        if self.recursion_flag:
            res = False
        else:
            self.recursion_flag = True
            res = all((req.is_true(options) for req in self.requirements))
            self.recursion_flag = False
        return res

    def __str__(self):
        return "(" + (" & ".join((str(req) for req in self.requirements))) + ")"


class OrLogicExpression(LogicExpression):
    def __init__(self, requirements):
        self.requirements = requirements
        self.recursion_flag = False

    def is_true(self, options: Options):
        if self.recursion_flag:
            res = False
        else:
            self.recursion_flag = True
            res = any((req.is_true(options) for req in self.requirements))
            self.recursion_flag = False
        return res

    def __str__(self):
        return "(" + (" | ".join((str(req) for req in self.requirements))) + ")"


def find_closing_parenthesis(tokens, start: int) -> int:
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


def parse_logic_token_expr(tokens) -> LogicExpression:
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


def parse_logic_expression(expression: str):
    tokens = [str.strip() for str in re.split("([&|()])", expression)]
    tokens = [token for token in tokens if token != ""]

    return parse_logic_token_expr(tokens)


def check_static_option_req(string, options):
    return parse_logic_expression(string).is_true(options)
