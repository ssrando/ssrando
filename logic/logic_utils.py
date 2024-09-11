from __future__ import annotations
from dataclasses import dataclass
from functools import cache
from typing import List  # Only for typing purposes
from hints.hint_types import HINT_IMPORTANCE

from .logic import Logic, Placement, LogicSettings
from .logic_input import Areas
from .logic_expression import DNFInventory
from .inventory import (
    Inventory,
    EXTENDED_ITEM,
    EMPTY_INV,
    EVERYTHING_BIT,
    EVERYTHING_UNBANNED_BIT,
    HINT_BYPASS_BIT,
    BANNED_BIT,
)
from .constants import *
from .placements import *
from .pools import *


@dataclass
class AdditionalInfo:
    required_dungeons: List[str]
    unrequired_dungeons: List[str]
    randomized_dungeon_entrance: dict[str, str]
    randomized_trial_entrance: dict[str, str]
    randomized_start_entrance: dict[str, str]
    randomized_start_statues: dict[str, str]
    known_locations: List[EIN]


class LogicUtils(Logic):
    def __init__(
        self,
        areas: Areas,
        placement: Placement,
        additional_info: AdditionalInfo,
        runtime_requirements,
        banned,
        /,
        reqs: List[DNFInventory] | None = None,
    ):
        starting_inventory = Inventory(
            {EXTENDED_ITEM[itemname] for itemname in placement.starting_items}
        )
        settings = LogicSettings(
            starting_inventory, EMPTY_INV, runtime_requirements, banned
        )
        super().__init__(areas, settings, placement, optim=False, requirements=reqs)
        self.full_inventory = Logic.get_everything_unbanned(self.requirements)
        self.required_dungeons = additional_info.required_dungeons
        self.unrequired_dungeons = additional_info.unrequired_dungeons
        self.randomized_dungeon_entrance = additional_info.randomized_dungeon_entrance
        self.randomized_trial_entrance = additional_info.randomized_trial_entrance
        self.randomized_start_entrance = additional_info.randomized_start_entrance
        self.randomized_start_statues = additional_info.randomized_start_statues
        self.known_locations = additional_info.known_locations

    def check(self, useroutput):
        full_inventory = Logic.fill_inventory(self.requirements, EMPTY_INV)
        DEMISE_BIT = EXTENDED_ITEM[self.short_to_full(DEMISE)]
        if not full_inventory[DEMISE_BIT]:
            raise useroutput.GenerationFailed(f"Could not reach Demise.")

        full_inventory = Logic.fill_inventory(self.requirements, Inventory(BANNED_BIT))

        if not full_inventory[EVERYTHING_BIT]:
            (everything_req,) = self.requirements[EVERYTHING_BIT].disjunction
            i = next(iter(everything_req.intset - full_inventory.intset))
            check = self.areas.full_to_short(EXTENDED_ITEM.get_item_name(i))
            raise useroutput.GenerationFailed(f"Could not reach check {check}.")

        if not all(item in self.placement.locations for item in self.areas.checks):
            check = next(iter(set(self.areas.checks) - set(self.placement.locations)))
            check_name = self.areas.full_to_short(check)
            raise useroutput.GenerationFailed(
                f"Check {check_name} has not been assigned an item."
            )

        if not all(item in self.placement.items for item in INVENTORY_ITEMS):
            item = next(iter(set(INVENTORY_ITEMS) - set(self.placement.items)))
            raise useroutput.GenerationFailed(
                f"Item {item} has not been handled by the randomizer."
            )

    @cache
    def _fill_for_test(self, banned_intset, inventory):
        custom_requirements = self.requirements.copy()
        for index, e in enumerate(reversed(bin(banned_intset))):
            if e == "1":
                custom_requirements[index] = DNFInventory(False)

        return Logic.fill_inventory(custom_requirements, inventory)

    def fill_restricted(
        self,
        banned_indices: List[EXTENDED_ITEM] = [],
        starting_inventory: None | Inventory = None,
    ):
        if starting_inventory is None:
            starting_inventory = self.inventory

        banned_intset = 0
        for i in banned_indices:
            banned_intset |= 1 << i

        return self._fill_for_test(banned_intset, starting_inventory)

    def restricted_test(
        self,
        test_index,
        banned_indices: List[EXTENDED_ITEM] = [],
        starting_inventory: None | Inventory = None,
    ):
        restricted_full = self.fill_restricted(banned_indices, starting_inventory)

        return restricted_full[test_index]

    def congregate_requirements(self, item):
        if not hasattr(self, "congregated_reqs"):
            self._isvisited_agg = set()
            self.aggregated_reqs: List[None | bool | Inventory] = [
                None for _ in self.requirements
            ]

        if item in self._isvisited_agg:
            return False

        if self.aggregated_reqs[item] is not None:
            return self.aggregated_reqs[item]

        self._isvisited_agg.add(item)
        aggregate = False
        for possibility, (_, conj_pre) in self.requirements[item].disjunction.items():
            aggregate_ = Inventory(conj_pre)
            for req_item in possibility:
                ag = self.congregate_requirements(req_item)
                if ag is False:
                    break
                aggregate_ |= ag
            else:
                if aggregate is False:
                    aggregate = aggregate_
                else:
                    aggregate &= aggregate_

        self._isvisited_agg.remove(item)
        if not self._isvisited_agg:
            self.aggregated_reqs[item] = aggregate

        return aggregate

    @cache
    def _get_sots_items(self, index: EXTENDED_ITEM):
        usefuls = self.get_useful_items(index)
        return [
            item
            for item in INVENTORY_ITEMS
            if item in usefuls
            and not self.restricted_test(
                index,
                [EXTENDED_ITEM[item]],
                starting_inventory=self.inventory | HINT_BYPASS_BIT,
            )
        ]

        # requireds: Inventory = self.congregate_requirements(index)  # type: ignore
        # return [
        # self.full_to_short(EXTENDED_ITEM[i])
        # for i in requireds.intset
        # if EXTENDED_ITEM[i] in self.checks
        # ]

    def get_sots_items(self, index: EXTENDED_ITEM | None = None):
        if index is None:
            index = EXTENDED_ITEM[self.short_to_full(DEMISE)]
        return self._get_sots_items(index)

    def get_sots_locations(self, index: EXTENDED_ITEM | None = None):
        if index is None:
            index = EXTENDED_ITEM[self.short_to_full(DEMISE)]
        for item in self.get_sots_items(index):
            if self.placement.item_placement_limit.get(item, ""):
                continue

            sots_loc = self.placement.items[item]

            if sots_loc == START_ITEM or sots_loc == UNPLACED_ITEM:
                continue

            hint_region = self.areas.checks[sots_loc]["hint_region"]
            yield (hint_region, sots_loc, item)

    @cache
    def _get_useful_items(self, index: EXTENDED_ITEM):
        usefuls = self.aggregate_requirements(
            self.requirements, self.full_inventory, index
        )
        return [
            loc
            for i in usefuls.intset
            if (loc := EXTENDED_ITEM.get_item_name(i)) in INVENTORY_ITEMS
        ]

    def get_useful_items(
        self, bit=EVERYTHING_UNBANNED_BIT, exclude_redundant_copies=False
    ):
        res = self._get_useful_items(bit)
        if not res:
            return [
                loc
                for i in self.full_inventory.intset
                if (loc := EXTENDED_ITEM.get_item_name(i)) in PROGRESS_ITEMS
            ]
        if not exclude_redundant_copies:
            return res
        items_to_remove = set()
        # First, check for redundancies in items that are only useful for one copy
        only_useful_once = [
            PROGRESSIVE_POUCHES.keys(),
            PROGRESSIVE_BOWS.keys(),
            PROGRESSIVE_SLINGSHOTS.keys(),
            PROGRESSIVE_BUG_NETS.keys(),
            EMPTY_BOTTLES.keys(),
        ]
        for item_set in only_useful_once:
            for item in item_set:
                # If an item is not accessible with all other copies of this item removed, it must
                # be redundant since it is definitely locked by a previous copy.
                if not self.restricted_test(
                    EXTENDED_ITEM[item],
                    [
                        EXTENDED_ITEM[self.placement.items[item_copy]]
                        for item_copy in item_set
                        if item != item_copy
                        and item_copy not in self.placement.starting_items
                    ],
                    self.inventory | HINT_BYPASS_BIT,
                ):
                    items_to_remove.add(item)
        REVERSE_BATREAUX_LIST = reversed(self.locations_by_hint_region(BATREAUX))
        max_batreaux_reward = None
        other_max_batreaux_reward = None
        for index, loc in enumerate(REVERSE_BATREAUX_LIST):
            if loc not in self.banned:
                max_batreaux_reward = loc
                match index:
                    case 1:  # Bat 70 second reward
                        # Include normal bat 70
                        other_max_batreaux_reward = REVERSE_BATREAUX_LIST[2]
                    case 2:  # Bat 70
                        # Include bat 70 second reward
                        other_max_batreaux_reward = REVERSE_BATREAUX_LIST[1]
                    case 6:  # Bat 30 chest
                        # Include normal bat 30
                        other_max_batreaux_reward = REVERSE_BATREAUX_LIST[7]
                    case 7:  # Bat 30
                        # Include bat 30 chest
                        other_max_batreaux_reward = REVERSE_BATREAUX_LIST[6]
                break
        if max_batreaux_reward is not None:
            for crystal_pack in GRATITUDE_CRYSTAL_PACKS.keys():
                # Crystal packs that logically come after the max Batreaux reward are redundant
                sots_locs = [
                    i[1] for i in self.get_sots_locations(EXTENDED_ITEM[crystal_pack])
                ]
                if max_batreaux_reward in sots_locs:
                    items_to_remove.add(crystal_pack)
                elif other_max_batreaux_reward is not None:
                    # We must check the equivalent-level batreaux reward if it is 70 or 30
                    if other_max_batreaux_reward in sots_locs:
                        items_to_remove.add(crystal_pack)
        WALLET_LOCKED_BEEDLE = SORTED_BEEDLE_CHECKS[:4]
        max_beedle = None
        for loc in WALLET_LOCKED_BEEDLE:
            if loc not in self.banned:
                max_beedle = loc
                break
        if max_beedle is not None:
            for wallet in list(PROGRESSIVE_WALLETS.keys()) + list(EXTRA_WALLETS.keys()):
                sots_locs = [
                    i[1] for i in self.get_sots_locations(EXTENDED_ITEM[wallet])
                ]
                # Wallets that logically come after the max Beedle shop item are redundant
                if max_beedle in sots_locs:
                    items_to_remove.add(wallet)
        return [item for item in res if item not in items_to_remove]

    @cache
    def locations_by_hint_region(self, region):
        return [n for n, c in self.areas.checks.items() if c["hint_region"] == region]

    @cache
    def _get_barren_regions(self, index: EXTENDED_ITEM):
        useful_checks = (
            loc
            for item in self.get_useful_items(index, True)
            for loc in (self.placement.items[item],)
            if item not in self.placement.starting_items
            if item not in self.placement.unplaced_items
            if not self.placement.item_placement_limit.get(item, "")
            if loc not in self.known_locations
        )

        non_banned = self.fill_restricted()

        useless_regions = set(ALL_HINT_REGIONS)
        for c in useful_checks:
            check = self.areas.checks[c]
            if (region := check.get("cube_region")) is None:
                region = check["hint_region"]
            useless_regions.discard(region)
        useless_regions = sorted(useless_regions)

        checks_per_region = {k: 0 for k in ALL_HINT_REGIONS}
        for c in self.areas.checks.values():
            if non_banned[c["req_index"]]:
                if (region := c.get("cube_region")) is None:
                    region = c["hint_region"]
                checks_per_region[region] += 1

        return (
            {k: v for k in useless_regions if (v := checks_per_region[k]) > 0},
            [k for k, v in checks_per_region.items() if v == 0],
        )

    def get_barren_regions(self, bit=None):
        if bit is None:
            bit = EXTENDED_ITEM[self.short_to_full(DEMISE)]
        return self._get_barren_regions(bit)

    def calculate_playthrough_progression_spheres(self):
        spheres = []
        inventory = self.inventory | HINT_BYPASS_BIT
        inventory2 = inventory
        requirements = self.backup_requirements
        usefuls = self.get_useful_items()
        while True:
            sphere = []
            keep_going = True
            while keep_going:
                keep_going = False
                for i in EXTENDED_ITEM.items():
                    if not inventory2[i] and requirements[i].eval(inventory):
                        keep_going = True
                        inventory2 |= i
                        if (item := EXTENDED_ITEM.get_item_name(i)) in usefuls:
                            loc = self.placement.items[item]
                            sphere.append(loc)
                        elif i == EXTENDED_ITEM[self.short_to_full(DEMISE)]:
                            sphere.append(DEMISE)
                        else:
                            inventory |= i
            inventory = inventory2
            if sphere:
                spheres.append(sphere)
            else:
                break
        return spheres

    def get_dowsing(self, dowsing_setting):
        # Get info for which dowsing slot (if any) a chest should respond to.
        # Dowsing slots:
        # 0: Main quest
        # 1: Rupee
        # 2: Key Piece / Scrapper Quest
        # 3: Crystal
        # 4: Heart
        # 5: Goddess Cube
        # 6: Look around (not usable afaik)
        # 7: Treasure
        # 8: None
        if dowsing_setting == "Vanilla":
            dowse = lambda v: 8
        elif dowsing_setting == "All Chests":
            dowse = lambda v: 0
        else:
            assert dowsing_setting == "Progress Items"

            def dowse(v) -> int:
                if v in self.get_useful_items():
                    return 0
                if v in RUPEES:
                    return 1
                if v in TREASURES:
                    return 7
                return 8

        return {k: dowse(v) for k, v in self.placement.locations.items()}

    def get_importance_for_item(self, item):
        # Skip trivially unrequired items
        if item not in self.get_useful_items():
            return HINT_IMPORTANCE.Null
        # Then check if the item is SotS
        if item in self.get_sots_items():
            return HINT_IMPORTANCE.Required
        # Then check if the item is considered useful for Demise; ultimately unrequired items will not count
        elif item in self.get_useful_items(
            EXTENDED_ITEM[self.short_to_full(DEMISE)], True
        ):
            return HINT_IMPORTANCE.PossiblyRequired
        # The item must now be not required
        else:
            return HINT_IMPORTANCE.NotRequired
