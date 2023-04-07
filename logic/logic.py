from __future__ import annotations
from functools import cache
from typing import Any, Dict, Iterable, List, Set, Tuple
from collections import defaultdict
from dataclasses import dataclass, field

from hints.hint_types import GossipStoneHintWrapper, Hint

from .constants import *
from .logic_input import Area, Areas, DayOnly, NightOnly, Both
from .logic_expression import DNFInventory, AndCombination
from .inventory import (
    HINT_BYPASS_BIT,
    EVERYTHING_BIT,
    EVERYTHING_UNBANNED_BIT,
    Inventory,
    EXTENDED_ITEM,
    EMPTY_INV,
    BANNED_BIT,
)


@dataclass
class PoolEntrance:
    entrance: EXTENDED_ITEM_NAME
    constraints: List[EXTENDED_ITEM_NAME] = field(default_factory=list)


@dataclass
class PoolExit:
    exit: EXTENDED_ITEM_NAME
    constraints: List[EXTENDED_ITEM_NAME] = field(default_factory=list)


@dataclass
class Placement:
    item_placement_limit: Dict[EXTENDED_ITEM_NAME, EXTENDED_ITEM_NAME] = field(
        default_factory=lambda: defaultdict(lambda: EIN(str()))
    )

    map_transitions: Dict[EIN, EIN] = field(default_factory=dict)
    reverse_map_transitions: Dict[EIN, EIN] = field(default_factory=dict)

    locations: Dict[EIN, EIN] = field(default_factory=dict)
    items: Dict[EXTENDED_ITEM_NAME, EXTENDED_ITEM_NAME] = field(default_factory=dict)
    stones: Dict[EIN, List[EIN]] = field(default_factory=lambda: defaultdict(list))
    stone_hints: Dict[EIN, EIN] = field(default_factory=dict)
    hints: Dict[EIN, Hint | GossipStoneHintWrapper] = field(default_factory=dict)
    starting_items: Set[EIN] = field(default_factory=set)
    unplaced_items: Set[EIN] = field(default_factory=set)

    def copy(self):
        return Placement(
            self.item_placement_limit.copy(),
            self.map_transitions.copy(),
            self.reverse_map_transitions.copy(),
            self.locations.copy(),
            self.items.copy(),
            self.stones.copy(),
            self.stone_hints.copy(),
            self.hints.copy(),
            self.starting_items.copy(),
            self.unplaced_items.copy(),
        )

    def __or__(self, other: Placement) -> Placement:
        if not isinstance(other, Placement):
            raise ValueError
        # item_placement_limit
        for k, v in other.item_placement_limit.items():
            if k in self.item_placement_limit and v != self.item_placement_limit[k]:
                raise ValueError(
                    f"Found key '{k}' in self.item_placement_limit. Expected value '{v}' but found value '{self.item_placement_limit[k]}'."
                )
        # map_transitions
        for k, v in other.map_transitions.items():
            if k in self.map_transitions and v != self.map_transitions[k]:
                raise ValueError(
                    f"Found key '{k}' in self.map_transitions. Expected value '{v}' but found value '{self.map_transitions[k]}'."
                )
        # reverse_map_trasitions
        for k, v in other.reverse_map_transitions.items():
            if (
                k in self.reverse_map_transitions
                and v != self.reverse_map_transitions[k]
            ):
                raise ValueError(
                    f"Found key '{k}' in self.reverse_map_transitions. Expected value '{v}' but found value '{self.reverse_map_transitions[k]}'."
                )
        # locations
        for location, item in other.locations.items():
            if location in self.locations and item != self.locations[location]:
                raise ValueError(
                    f"Found location '{location}' in self.locations. Expected item '{item}' but found item '{self.locations[location]}'."
                )
        # items
        for item, location in other.items.items():
            if item in self.items and location != self.items[item]:
                raise ValueError(
                    f"Found item '{item}' in self.items. Expected location '{location}' but found location '{self.items[item]}'."
                )
        # stones
        for k, v in other.stones.items():
            if k in self.stones and v != self.stones[k]:
                raise ValueError(
                    f"Found key '{k}' in self.stones. Expected value '{v}' but found value '{self.stones[k]}'."
                )
        # stone_hints
        for k, v in other.stone_hints.items():
            if k in self.stone_hints and v != self.stone_hints[k]:
                raise ValueError(
                    f"Found key '{k}' in self.stone_hints. Expected value '{v}' but found value '{self.stone_hints[k]}'."
                )
        # hints
        for k, v in other.hints.items():
            if k in self.hints and v != self.hints[k]:
                raise ValueError(
                    f"Found key '{k}' in self.hints. Expected value '{v}' but found value '{self.hints[k]}'."
                )
        return Placement(
            self.item_placement_limit | other.item_placement_limit,
            self.map_transitions | other.map_transitions,
            self.reverse_map_transitions | other.reverse_map_transitions,
            self.locations | other.locations,
            self.items | other.items,
            self.stones | other.stones,
            self.stone_hints | other.stone_hints,
            self.hints | other.hints,
            self.starting_items | other.starting_items,
            self.unplaced_items | other.unplaced_items,
        )

    def add_starting_items(self, items: Set[EIN]):
        for item in items:
            if item in self.items and self.items[item] != START_ITEM:
                raise ValueError(
                    f"Start item '{item}' has already been placed. Start items should take priority over all but required dungeons. Something weird has happened."
                )

        self.items |= {k: START_ITEM for k in items}
        self.starting_items |= items

    def add_unplaced_items(self, items: Set[EIN]):
        for item in items:
            if item in self.items and self.items[item] != UNPLACED_ITEM:
                raise ValueError(f"Unplaced item '{item}' has already been placed.")

        self.items |= {k: UNPLACED_ITEM for k in items}
        self.unplaced_items |= items


@dataclass
class LogicSettings:
    full_inventory: Inventory
    starting_inventory: Inventory
    runtime_requirements: Dict[EIN, DNFInventory]
    banned: List[EIN]


class Logic:
    @staticmethod
    def fill_inventory(requirements: List[DNFInventory], inventory: Inventory):
        keep_going = True
        while keep_going:
            keep_going = False
            for i in EXTENDED_ITEM.items():
                if not inventory[i] and requirements[i].eval(inventory):
                    inventory |= i
                    keep_going = True
        return inventory

    @staticmethod
    def is_full_inventory(requirements: List[DNFInventory], inventory: Inventory):
        for i in EXTENDED_ITEM.items():
            if not inventory[i] and requirements[i].eval(inventory):
                return False
        return True

    @staticmethod
    def aggregate_requirements(
        requirements: List[DNFInventory],
        full_inventory: Inventory | None,
        start_bit: EXTENDED_ITEM | None = None,
    ):
        aggregate = EMPTY_INV
        if full_inventory is None:
            test = lambda _: True
        else:
            test = lambda bit: full_inventory[bit]
        if start_bit is None:
            for bit in EXTENDED_ITEM.items():
                if test(bit):
                    for conj in requirements[bit].disjunction:
                        aggregate |= conj
        else:
            todos = {start_bit}
            while todos:
                bit = todos.pop()
                if test(bit):
                    for conj in requirements[bit].disjunction:
                        todos |= conj.intset - aggregate.intset
                        aggregate |= conj

        return aggregate

    @staticmethod
    def get_everything_unbanned(requirements: List[DNFInventory]):
        inventory = Inventory(
            {EXTENDED_ITEM[itemname] for itemname in INVENTORY_ITEMS}
            | {HINT_BYPASS_BIT}
        )
        full_inventory = Logic.fill_inventory(requirements, inventory)
        (everything_req,) = requirements[EVERYTHING_BIT].disjunction
        everything_unbanned_req = DNFInventory(
            Inventory({item for item in everything_req if full_inventory[item]})
        )
        requirements[EVERYTHING_UNBANNED_BIT] = everything_unbanned_req
        return Logic.fill_inventory(requirements, full_inventory)

    @staticmethod
    def free_simplify(requirements, free: Inventory):
        req = DNFInventory(True)
        for i in Logic.fill_inventory(requirements, free) - free:
            requirements[i] = req

    @staticmethod
    def shallow_simplify(requirements, opaques):
        simplifiables = Inventory(
            {
                item
                for item in EXTENDED_ITEM.items()
                if not opaques[item]
                if len(requirements[item].disjunction) <= 1
            }
        )

        for item, req in enumerate(requirements):
            if item == EVERYTHING_BIT or len(req.disjunction) >= 30:
                continue
            new_req = DNFInventory()
            for conj in req.disjunction:
                if conj & simplifiables:
                    new_conj = Inventory()
                    skip = False
                    for req_item in conj.intset:
                        if not simplifiables[req_item]:
                            new_conj |= Inventory(req_item)
                        else:
                            req_item_req = requirements[req_item].disjunction
                            if not req_item_req:
                                skip = True
                                break
                            (req_item_conj,) = req_item_req
                            new_conj |= req_item_conj
                    if not skip and not new_conj[EXTENDED_ITEM(item)]:
                        new_req |= DNFInventory(new_conj)
                else:
                    new_req |= conj
            requirements[item] = new_req

    @staticmethod
    def deep_simplify(requirements, opaques):
        simplified = [len(req.disjunction) > 5 for req in requirements]
        visited = set()
        todo_list = list((range(len(requirements))))

        def simplify(item) -> Tuple[DNFInventory, Set[EXTENDED_ITEM]]:
            hit_a_visited = set()
            if opaques[item]:
                return DNFInventory(item), set()

            if item in visited:
                return DNFInventory(item), {item}

            if simplified[item]:
                return requirements[item], set()

            visited.add(item)
            new_req = DNFInventory()
            for possibility in requirements[item].disjunction:
                simplified_conj = []
                for req_item in possibility.intset:
                    item_req, h_a_v = simplify(req_item)
                    hit_a_visited = hit_a_visited | h_a_v
                    simplified_conj.append(item_req.remove(item))
                new_req |= AndCombination.simplifyDNF(simplified_conj)

            visited.remove(item)
            hit_a_visited.discard(item)
            if not hit_a_visited:
                requirements[item] = new_req
                simplified[item] = True
            elif len(todo_list) < 50:
                todo_list.append(item)
            return new_req, hit_a_visited

        while todo_list:
            item = EXTENDED_ITEM(todo_list.pop())
            simplify(item)

    def __init__(
        self,
        areas: Areas,
        logic_settings: LogicSettings,
        placement: Placement,
        /,
        optim=True,
        requirements: List[DNFInventory] | None = None,
    ):
        self.areas = areas
        self.short_to_full = areas.short_to_full
        self.full_to_short = areas.full_to_short

        self.requirements = areas.requirements.copy()
        self.opaque = areas.opaque.copy()

        if requirements is not None:
            self.requirements = requirements.copy()

        self.entrance_allowed_time_of_day = areas.entrance_allowed_time_of_day
        self.exit_to_area = areas.exit_to_area
        self.placement = placement
        self.fixed_locations = list(placement.locations)

        self.banned = logic_settings.banned
        banned_bit_inv = DNFInventory(BANNED_BIT)

        self.ban_if = lambda it, r: r & banned_bit_inv if it in self.banned else r

        self.inventory = logic_settings.full_inventory
        self.frees = logic_settings.starting_inventory

        self.backup_requirements = self.requirements.copy()

        for loc, req in logic_settings.runtime_requirements.items():
            it = EXTENDED_ITEM[loc]
            # assert self.opaque[it]
            self.requirements[it] |= self.ban_if(loc, req)
            if it != EVERYTHING_BIT:
                self.opaque[it] = False

        self.shallow_simplify(self.requirements, self.opaque)

        for exit, entrance in self.placement.map_transitions.items():
            self.link_connection(exit, entrance)

        self.full_inventory = self.inventory
        for k, v in self.placement.locations.items():
            self.place_item(k, v, fill=False)

        pure_usefuls = self.aggregate_requirements(areas.requirements, None)
        for it in self.banned:
            if it not in EXTENDED_ITEM:
                continue
            bit = EXTENDED_ITEM[it]
            if self.areas.requirements[bit].is_impossible() or bit not in pure_usefuls:
                self.requirements[bit] &= banned_bit_inv
            else:
                raise ValueError(
                    f"Cannot ban potentially inlined away requirement {it}"
                )

        if optim:
            self.free_simplify(self.requirements, self.frees)
            self.shallow_simplify(self.requirements, self.opaque)
            self.fill_inventory_i(monotonic=True)
        self.backup_requirements = self.requirements.copy()
        self.aggregate = self.aggregate_requirements(self.requirements, None)

    def add_item(self, item: EXTENDED_ITEM):
        self.inventory |= item
        self.full_inventory |= item
        self.fill_inventory_i(monotonic=True)

    def add_items(self, items: Iterable[EXTENDED_ITEM]):
        for item in items:
            self.inventory |= item
            self.full_inventory |= item
        self.fill_inventory_i(monotonic=True)

    def remove_item(self, item: EXTENDED_ITEM):
        self.inventory = self.inventory.remove(item)
        if Inventory(item) <= self.aggregate:
            self.fill_inventory_i()

    def remove_items(self, items: Iterable[EXTENDED_ITEM]):
        for item in items:
            self.inventory = self.inventory.remove(item)
        if any(item in self.aggregate.intset for item in items):
            self.fill_inventory_i()

    def fill_inventory_i(self, monotonic=False):
        # self.shallow_simplify()
        self.free_simplify(self.requirements, self.frees)
        inventory = self.full_inventory if monotonic else self.inventory
        self.full_inventory = self.fill_inventory(self.requirements, inventory)

    @staticmethod
    def explore(checks, area: Area) -> Iterable[EIN]:
        def explore(area):
            for loc in area.locations:
                loc_full = with_sep_full(area.name, loc)
                if loc_full in checks:
                    yield loc_full
            for sub_area in area.sub_areas.values():
                yield from explore(sub_area)

        return explore(area)

    @cache
    def check_list(self, placement_limit: EIN) -> List[EIN]:
        return list(
            dict.fromkeys(self.explore(self.areas.checks, self.areas[placement_limit]))
        )

    def accessible_checks(self, placement_limit: EIN = EIN("")) -> List[EIN]:
        if placement_limit in self.areas.checks:
            placement_limit2, loc = placement_limit.rsplit("\\", 1)
            locations = self.areas[placement_limit2].locations
            assert loc in locations
            if placement_limit in self.fixed_locations:
                return []
            return [EIN(placement_limit)]
        else:
            return [
                loc
                for loc in self.check_list(placement_limit)
                if self.full_inventory[EXTENDED_ITEM[loc]]
                and loc not in self.fixed_locations
            ]

    def accessible_stones(self) -> Iterable[EIN]:
        for stone in self.areas.gossip_stones:
            if self.full_inventory[self.areas.gossip_stones[stone]["req_index"]]:
                yield stone

    def accessible_exits(self, exit_pool: Iterable[PoolExit]) -> Iterable[PoolExit]:
        for exit in exit_pool:
            if exit in self.areas.map_exits:
                if self.full_inventory[EXTENDED_ITEM[exit]]:
                    yield exit

    def link_connection(self, exit: EIN, entrance: EIN, pool=None, requirements=None):
        allowed_times = self.entrance_allowed_time_of_day[entrance]
        exit_bit = EXTENDED_ITEM[exit]
        exit_area = self.exit_to_area[exit]
        exit_as_req = DNFInventory(exit_bit)

        if exit_area.abstract:
            day_req = exit_as_req
            night_req = exit_as_req
        elif exit_area.allowed_time_of_day == Both:
            day_req = exit_as_req & DNFInventory(
                EXTENDED_ITEM[make_day(exit_area.name)]
            )
            night_req = exit_as_req & DNFInventory(
                EXTENDED_ITEM[make_night(exit_area.name)]
            )
        elif exit_area.allowed_time_of_day == DayOnly:
            day_req = exit_as_req
            night_req = DNFInventory()
        else:
            day_req = DNFInventory()
            night_req = exit_as_req

        if allowed_times == Both:
            bit_req = [
                (EXTENDED_ITEM[make_day(entrance)], day_req),
                (EXTENDED_ITEM[make_night(entrance)], night_req),
            ]
        elif allowed_times == DayOnly:
            bit_req = [(EXTENDED_ITEM[entrance], day_req)]
        else:
            bit_req = [(EXTENDED_ITEM[entrance], night_req)]

        if requirements is None:
            self.placement.map_transitions[exit] = entrance
            self.placement.reverse_map_transitions[entrance] = exit
            for bit, req in bit_req:
                self.opaque[bit] = False
                req = self.ban_if(entrance, req)
                self.requirements[bit] |= req
                self.backup_requirements[bit] |= req
        else:
            for bit, req in bit_req:
                req = self.ban_if(entrance, req)
                requirements[bit] |= req

    def place_item(self, location: EIN, item: EIN, hint_mode=False, fill=True):
        if (
            not hint_mode
            and location in self.placement.locations
            and self.placement.locations[location] != item
        ):
            raise ValueError(f"Location {location} is already taken.")

        items = self.placement.stone_hints if hint_mode else self.placement.items
        if (
            item in items
            and items[item] != location
            and item not in DUPLICABLE_ITEMS
            and item not in DUPLICABLE_COUNTERPROGRESS_ITEMS
        ):
            if hint_mode:
                name = ""
            else:
                name = "Item "
            raise ValueError(f"{name}{item} is already placed.")

        if item in self.placement.item_placement_limit and not location.startswith(
            self.placement.item_placement_limit[item]
        ):
            raise ValueError(
                "This item cannot be placed in this area, "
                f"it must be placed in {self.placement.item_placement_limit[item]}."
            )

        if hint_mode:
            req = DNFInventory({Inventory(location), Inventory(HINT_BYPASS_BIT)})
            # loc | Hint Bypass
        else:
            req = DNFInventory(EXTENDED_ITEM[location])

        if item in EXTENDED_ITEM:
            item_bit = EXTENDED_ITEM[item]
            req = self.ban_if(item, req)
            self.requirements[item_bit] = req
            self.backup_requirements[item_bit] = req
            self.opaque[item_bit] = False
            if fill:
                self.fill_inventory_i(monotonic=True)
            items[item] = location

        if hint_mode:
            self.placement.stones[location].append(item)
        else:
            self.placement.locations[location] = item
        return True

    def replace_item(self, location: EIN, item: EIN, old_hint: EIN | None = None):
        if hint_mode := old_hint is not None:
            if location not in self.placement.stones:
                raise ValueError(f"Hint stone {location} is empty.")
            if old_hint not in self.placement.stones[location]:
                raise ValueError(f"Hint stone {location} does not contain {old_hint}.")
            if item in self.placement.stone_hints:
                raise ValueError(f"{item} is already placed.")
            self.placement.stones[location].remove(old_hint)
            del self.placement.stone_hints[old_hint]
            old_item = old_hint
        else:
            if location not in self.placement.locations:
                raise ValueError(f"Location {location} is not taken.")
            if item in self.placement.items:
                raise ValueError(f"Item {item} is already placed.")
            old_item = self.placement.locations[location]
            del self.placement.locations[location]
            del self.placement.items[old_item]

        if old_item in EXTENDED_ITEM:
            # We should always be in this case
            old_item_bit = EXTENDED_ITEM[old_item]
            self.opaque[old_item_bit] = True
            self.backup_requirements[old_item_bit] = DNFInventory()
            self.requirements = self.backup_requirements.copy()
            self.fill_inventory_i()

        self.place_item(location, item, hint_mode=hint_mode)
        return old_item
