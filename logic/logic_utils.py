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
    puzzles: Any


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
        self.puzzles = additional_info.puzzles
        # Requirements solely in terms of items or item macros
        # This is useful for accurate hint importance calculations, and
        # makes SotS calculation much faster
        self.flattened_requirements = Logic.bottomup_propagate(
            self.requirements,
            Inventory(
                {
                    EXTENDED_ITEM[itemname]
                    for itemname in (
                        POTENTIALLY_USEFUL_ITEMS.keys()
                        | {self.short_to_full(macro) for macro in RAW_ITEM_MACROS}
                    )
                }
            ),
        )
        self.importance = self.calculate_importance()

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

        if not self.test_importance_validity():
            raise useroutput.GenerationFailed(
                "Hint Importance error: Could not reach Demise without 'not required' items."
            )

    @cache
    def _fill_for_test(self, banned_intset, inventory, use_flattened_requirements=True):
        custom_requirements = (
            self.flattened_requirements.copy()
            if use_flattened_requirements
            else self.requirements.copy()
        )
        for index, e in enumerate(reversed(bin(banned_intset))):
            if e == "1":
                custom_requirements[index] = DNFInventory(False)

        return Logic.fill_inventory(custom_requirements, inventory)

    # Flattened requirements are faster to evaluate, but they will not work for
    # restricting locations; only items.
    def fill_restricted(
        self,
        banned_indices: List[EXTENDED_ITEM] = [],
        starting_inventory: None | Inventory = None,
        use_flattened_requirements=True,
    ):
        if starting_inventory is None:
            starting_inventory = self.inventory

        banned_intset = 0
        for i in banned_indices:
            banned_intset |= 1 << i

        return self._fill_for_test(
            banned_intset, starting_inventory, use_flattened_requirements
        )

    def restricted_test(
        self,
        test_index,
        banned_indices: List[EXTENDED_ITEM] = [],
        starting_inventory: None | Inventory = None,
    ):
        restricted_full = self.fill_restricted(banned_indices, starting_inventory)

        return restricted_full[test_index]

    def is_redundant_copy(
        self,
        item: EXTENDED_ITEM_NAME,
        item_set: List[EXTENDED_ITEM_NAME],
        starting_inventory: None | Inventory = None,
    ) -> bool:
        if starting_inventory is None:
            starting_inventory = self.inventory | HINT_BYPASS_BIT

        return bool(
            self.filter_locked_by_items(
                [item],
                [
                    item_copy
                    for item_copy in item_set
                    if item_copy != item
                    and item_copy not in self.placement.starting_items
                ],
                starting_inventory,
            )
        )

    # Returns a list of which items in `items_to_test` are locked by the set of given items
    def filter_locked_by_items(
        self,
        items_to_test: List[EXTENDED_ITEM_NAME],
        items: List[EXTENDED_ITEM_NAME],
        starting_inventory: None | Inventory = None,
    ) -> List[EXTENDED_ITEM_NAME]:
        if not items:
            return []

        if starting_inventory is None:
            starting_inventory = self.inventory | HINT_BYPASS_BIT

        # To use flattened requirements, we need to test solely in terms of items, not locations.
        accessible_set = self.fill_restricted(
            [EXTENDED_ITEM[item] for item in items], starting_inventory
        )

        return [
            item for item in items_to_test if not accessible_set[EXTENDED_ITEM[item]]
        ]

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
        usefuls = self._get_useful_items(index)
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
            if self.placement.item_placement_limit[item] != DEFAULT_PLACEMENT_LIMIT:
                continue

            sots_loc = self.placement.items[item]

            if sots_loc == START_ITEM or sots_loc == UNPLACED_ITEM:
                continue

            hint_region = self.areas.checks[sots_loc]["hint_region"]
            yield (hint_region, sots_loc, item)

    @cache
    def _get_useful_items(self, idx: EXTENDED_ITEM, exclude_redundant_copies=False):
        # Use flattened requirements for more efficient aggregation
        requirements = self.flattened_requirements.copy()
        items_to_remove = set()
        first_pass_usefuls = []
        can_reuse_first_pass = True
        if exclude_redundant_copies:
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
                    if self.is_redundant_copy(item, item_set):
                        items_to_remove.add(item)
                        requirements[EXTENDED_ITEM[item]] = DNFInventory(False)

            # Perform a first-pass aggregation to determine useful items with the above copies removed
            first_pass_usefuls = [
                loc
                for i in self.aggregate_requirements(
                    requirements, self.full_inventory, idx
                )
                if (loc := EXTENDED_ITEM.get_item_name(i)) in INVENTORY_ITEMS
                and loc not in items_to_remove
            ]

            REVERSE_BATREAUX_LIST = list(
                reversed(self.locations_by_hint_region(BATREAUX))
            )
            WALLET_LOCKED_BEEDLE = [
                self.areas.short_to_full(beedle_check)
                for beedle_check in SORTED_BEEDLE_CHECKS[:4]
            ]
            CRYSTALS = list(GRATITUDE_CRYSTAL_PACKS.keys())
            WALLETS = list(PROGRESSIVE_WALLETS.keys()) + list(EXTRA_WALLETS.keys())

            # Go top-down through the list of Batreaux's rewards and find
            # the first one that hard-locks future crystal packs.
            banned_items = []
            batreaux_crystals = []
            for index, loc in enumerate(REVERSE_BATREAUX_LIST):
                reward_item = self.placement.locations[loc]
                # We don't care about crystal packs since they don't count as something useful on their own
                # (and they definitely won't be the *highest* Batreaux reward to lock another crystal pack)
                if reward_item in CRYSTALS:
                    batreaux_crystals.append(reward_item)
                    continue

                if reward_item in first_pass_usefuls:
                    # We've found a progress item, so add it to the list of forbidden items
                    # to test the crystal packs against
                    banned_items.append(reward_item)
                    # Consider Bat 30 / Bat 70 too if the 30 chest / 70 2nd reward are the first encountered
                    if (index == 1 or index == 5) and (
                        other_item := self.placement.locations[
                            REVERSE_BATREAUX_LIST[index + 1]
                        ]
                    ) in first_pass_usefuls:
                        banned_items.append(other_item)

                    if any(
                        hard_locked_crystals := self.filter_locked_by_items(
                            CRYSTALS,
                            banned_items,
                        )
                    ):
                        # At least one crystal pack is hard-locked by this Batreaux level, which is the
                        # highest Batreaux level with a useful item. This means none of the hard-locked
                        # crystal packs can possibly be useful, and none of the crystal packs
                        # later in Batreaux's rewards could be useful.
                        can_reuse_first_pass = False
                        for crystal in hard_locked_crystals + batreaux_crystals:
                            items_to_remove.add(crystal)
                            requirements[EXTENDED_ITEM[crystal]] = DNFInventory(False)

                    # We can stop looking now, since either we found redundant crystal packs or there's a
                    # useful item on Batreaux higher than any level that might hard-lock any crystal packs,
                    # meaning those crystal packs are technically still useful to get this useful item
                    break

            # The same principle applies for Beedle if wallets are locked by something
            # on medium/expensive purchases
            beedle_wallets = []
            for index, loc in enumerate(WALLET_LOCKED_BEEDLE):
                shop_item = self.placement.locations[loc]
                if shop_item in WALLETS:
                    beedle_wallets.append(shop_item)
                    continue

                if shop_item in first_pass_usefuls:
                    if any(
                        hard_locked_wallets := self.filter_locked_by_items(
                            WALLETS,
                            [shop_item],
                        )
                    ):
                        can_reuse_first_pass = False
                        for wallet in hard_locked_wallets + beedle_wallets:
                            items_to_remove.add(wallet)
                            requirements[EXTENDED_ITEM[wallet]] = DNFInventory(False)

                    break

        # Any redundant copies detected earlier will have been marked as impossible,
        # meaning they cannot be collected during aggregation.
        # This ensures that, for example, songs that lock only useless item copies
        # in silent realms may also be marked as not required.
        if can_reuse_first_pass and first_pass_usefuls:
            return first_pass_usefuls

        usefuls = self.aggregate_requirements(
            requirements,
            self.full_inventory,
            idx,
        )
        # We still need to filter copies that were removed earlier
        return [
            loc
            for i in usefuls.intset
            if (loc := EXTENDED_ITEM.get_item_name(i)) in INVENTORY_ITEMS
            and loc not in items_to_remove
        ]

    def get_useful_items(
        self, bit=EVERYTHING_UNBANNED_BIT, exclude_redundant_copies=False
    ):
        res = self._get_useful_items(bit, exclude_redundant_copies)
        if not res:
            return [
                loc
                for i in self.full_inventory.intset
                if (loc := EXTENDED_ITEM.get_item_name(i)) in PROGRESS_ITEMS
            ]
        return res

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
            if self.placement.item_placement_limit[item] == DEFAULT_PLACEMENT_LIMIT
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

    def calculate_importance(self):
        importance_map = {}
        # Start with the lowest importance, then work our way up
        for item in self.get_useful_items():
            importance_map[item] = HINT_IMPORTANCE.NotRequired
        for item in self.get_useful_items(
            EXTENDED_ITEM[self.short_to_full(DEMISE)], True
        ):
            importance_map[item] = HINT_IMPORTANCE.PossiblyRequired
        for item in self.get_sots_items():
            importance_map[item] = HINT_IMPORTANCE.Required
        return importance_map

    def get_importance_for_item(self, item):
        return self.importance.get(item, HINT_IMPORTANCE.Null)

    def test_importance_validity(self):
        unrequired_items = [
            item
            for item in self.full_inventory.intset
            if self.get_importance_for_item(EXTENDED_ITEM.get_item_name(item))
            == HINT_IMPORTANCE.NotRequired
        ]

        # The seed should still be beatable with all "not required" items removed.
        return self.restricted_test(
            EXTENDED_ITEM[self.areas.short_to_full(DEMISE)],
            unrequired_items,
            self.inventory | HINT_BYPASS_BIT,
        )
