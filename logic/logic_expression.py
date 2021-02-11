from typing import List, Tuple
from collections import OrderedDict
import re

ITEM_WITH_COUNT_REGEX = re.compile(r"^(.+) x(\d+)$")

class LogicExpression:
    def is_true(self, logic):
        raise NotImplementedError("abstract")
    
    def get_items_needed(self, logic) -> OrderedDict: # itemname -> count
        raise NotImplementedError("abstract")

    def to_str(self):
        raise NotImplementedError("abstract")

class BaseLogicExpression(LogicExpression):
    def __init__(self, req_name):
        self.req_name = req_name
    
    def is_true(self, logic):
        match = ITEM_WITH_COUNT_REGEX.match(self.req_name)
        if match:
            item_name = match.group(1)
            num_required = int(match.group(2))
            
            num_owned = logic.currently_owned_items.count(item_name)
            return num_owned >= num_required
        elif self.req_name.startswith("Can Access Other Location \""):
            return logic.check_other_location_requirement(self.req_name)
        elif self.req_name.startswith("Option \""):
            return logic.check_option_enabled_requirement(self.req_name)
        elif self.req_name in logic.all_item_names:
            return self.req_name in logic.currently_owned_items
        elif self.req_name in logic.macros:
            logical_expression = logic.macros[self.req_name]
            return logic.check_logical_expression_req(logical_expression)
        elif self.req_name == "Nothing":
            return True
        elif self.req_name == "Impossible":
            return False
        else:
            raise Exception("Unknown requirement name: " + self.req_name)
    
    def get_items_needed(self, logic) -> OrderedDict: # itemname, count
        if self.is_true(logic): # don't include items if this is already met
            return OrderedDict()
        match = ITEM_WITH_COUNT_REGEX.match(self.req_name)
        if match:
            item_name = match.group(1)
            num_required = int(match.group(2))
            
            return OrderedDict({item_name: num_required})
        elif self.req_name.startswith("Can Access Other Location \""):
            match = re.search(r"^Can Access Other Location \"([^\"]+)\"$", self.req_name)
            other_location_name = match.group(1)
            
            requirement_expression: LogicExpression = logic.item_locations[other_location_name]["Need"]
            return requirement_expression.get_items_needed(logic)
        elif self.req_name in logic.all_item_names:
            return OrderedDict({self.req_name: 1})
        elif self.req_name in logic.macros:
            return logic.macros[self.req_name].get_items_needed(logic)
        else:
            return None # unreachable
    
    def to_str(self):
        return self.req_name

class AndLogicExpression(LogicExpression):
    def __init__(self, requirements: List[LogicExpression]):
        self.requirements = requirements
    
    def is_true(self, logic):
        return all((req.is_true(logic) for req in self.requirements))
    
    def to_str(self):
        return '(' + (' & '.join((req.to_str() for req in self.requirements))) + ')'
    
    def get_items_needed(self, logic) -> OrderedDict: # itemname, count
        items_needed = OrderedDict()
        for subresult in (req.get_items_needed(logic) for req in self.requirements):
            if subresult is None: # if one is unreachable, all of this is
                return None
            for item_name, num_required in subresult.items():
                items_needed[item_name] = max(num_required, items_needed.setdefault(item_name, 0))
        return items_needed

class OrLogicExpression(LogicExpression):
    def __init__(self, requirements: List[LogicExpression]):
        self.requirements = requirements
    
    def is_true(self, logic):
        return any((req.is_true(logic) for req in self.requirements))
    
    def to_str(self):
        return '(' + (' | '.join((req.to_str() for req in self.requirements))) + ')'
    
    def get_items_needed(self, logic) -> OrderedDict: # itemname, count
        items_needed = OrderedDict()
        for subresult in (req.get_items_needed(logic) for req in self.requirements):
            if subresult == OrderedDict(): # if one is reachable without items, return not items
                return OrderedDict()
            if subresult == None:
                continue
            for item_name, num_required in subresult.items():
                items_needed[item_name] = max(num_required, items_needed.setdefault(item_name, 0))
        return items_needed

def find_closing_parenthesis(tokens: List[str], start: int) -> int:
    assert tokens[start] == '('
    nesting_lvl = 1
    pos = start + 1
    while nesting_lvl > 0 and pos < len(tokens):
        char = tokens[pos]
        if char == '(':
            nesting_lvl += 1
        elif char == ')':
            nesting_lvl -= 1
        pos += 1
    if nesting_lvl != 0:
        raise Exception('parenthesis never closed!')
    return pos - 1

def parse_logic_expression(expression: str) -> LogicExpression:
    tokens = [str.strip() for str in re.split("([&|()])", expression)]
    tokens = [token for token in tokens if token != ""]

    return parse_logic_token_expr(tokens)
        
def parse_logic_token_expr(tokens: List[str]) -> LogicExpression:
    pos = 0
    logic_type = None # can be 'or' or 'and'
    parsed = []
    while pos < len(tokens):
        cur_token = tokens[pos]
        if cur_token == '(':
            end = find_closing_parenthesis(tokens, pos)
            parsed.append(parse_logic_token_expr(tokens[pos + 1:end]))
            pos = end + 1
        elif cur_token == '&':
            if logic_type == 'or':
                raise Exception("mixed '&' and '|'!")
            else:
                logic_type = 'and'
            pos += 1
        elif cur_token == '|':
            if logic_type == 'and':
                raise Exception("mixed '&' and '|'!")
            else:
                logic_type = 'or'
            pos += 1
        else:
            parsed.append(BaseLogicExpression(cur_token))
            pos += 1
    if logic_type == None:
        assert len(parsed) == 1
        return parsed[0]
    elif logic_type == 'and':
        return AndLogicExpression(parsed)
    elif logic_type == 'or':
        return OrLogicExpression(parsed)
    else:
        raise Exception(logic_type)

def test():
    import yaml
    with open('SS Rando Logic - Item Location.yaml') as f:
        locations = yaml.safe_load(f)
    for loc in locations:
        req_str = locations[loc]['Need']
        print()
        print(req_str)
        print(parse_logic_expression(req_str).to_str())