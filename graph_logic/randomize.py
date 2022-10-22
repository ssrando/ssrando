from __future__ import annotations
from dataclasses import dataclass
from functools import cache
import random
from typing import List  # Only for typing purposes

from options import Options, OPTIONS
from .random_fill import RandomFill
from .front_fill import FrontFill
from .assumed_fill import AssumedFill
from .fill_algo_common import RandomizationSettings, UserOutput
from .logic import Logic, Placement, LogicSettings
from .logic_input import Areas
from .logic_expression import DNFInventory, InventoryAtom
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


def shuffle_indices(self, list, indices=None):
    if indices is None:
        return self.shuffle(list)
    else:
        n = len(indices)
        for i in range(n - 1):
            j = self.randint(i, n - 1)
            ii, jj = indices[i], indices[j]
            list[ii], list[jj] = list[jj], list[ii]
        return


@dataclass
class AdditionalInfo:
    required_dungeons: List[str]
    unrequired_dungeons: List[str]
    randomized_dungeon_entrance: dict[str, str]
    randomized_trial_entrance: dict[str, str]
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
        self.known_locations = additional_info.known_locations

    def check(self, useroutput):
        full_inventory = Logic.fill_inventory(self.requirements, EMPTY_INV)
        DEMISE_BIT = EXTENDED_ITEM[self.short_to_full(DEMISE)]
        if not full_inventory[DEMISE_BIT]:
            raise useroutput.GenerationFailed(f"Could not reach Demise")

        full_inventory = Logic.fill_inventory(self.requirements, Inventory(BANNED_BIT))

        if not full_inventory[EVERYTHING_BIT]:
            (everything_req,) = self.requirements[EVERYTHING_BIT].disjunction
            i = next(iter(everything_req.intset - full_inventory.intset))
            check = self.areas.full_to_short(EXTENDED_ITEM.get_item_name(i))
            raise useroutput.GenerationFailed(f"Could not reach check {check}")

        if not all(item in self.placement.locations for item in self.areas.checks):
            check = next(iter(set(self.areas.checks) - set(self.placement.locations)))
            check_name = self.areas.full_to_short(check)
            raise useroutput.GenerationFailed(
                f"Check {check_name} has not been assigned an item"
            )

        if not all(item in self.placement.items for item in INVENTORY_ITEMS):
            item = next(iter(set(INVENTORY_ITEMS) - set(self.placement.items)))
            raise useroutput.GenerationFailed(
                f"Item {item} has not been handled by the randomizer"
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
        for (possibility, (_, conj_pre)) in self.requirements[item].disjunction.items():
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

            if sots_loc == START_ITEM:
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

    def get_useful_items(self, bit=EVERYTHING_UNBANNED_BIT):
        return self._get_useful_items(bit)

    @cache
    def locations_by_hint_region(self, region):
        return [n for n, c in self.areas.checks.items() if c["hint_region"] == region]

    @cache
    def _get_barren_regions(self, index: EXTENDED_ITEM):
        useful_checks = (
            loc
            for item in self.get_useful_items(index)
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

        inacc_regions = set(ALL_HINT_REGIONS)
        for c in self.areas.checks.values():
            if non_banned[c["req_index"]]:
                if (region := c.get("cube_region")) is None:
                    region = c["hint_region"]
                inacc_regions.discard(region)

        return sorted(useless_regions - inacc_regions), sorted(inacc_regions)

    def get_barren_regions(self, bit=EVERYTHING_UNBANNED_BIT):
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


class Rando:
    def __init__(self, areas: Areas, options: Options, rng: random.Random):

        self.options = options
        self.rng = rng

        self.areas = areas
        self.short_to_full = areas.short_to_full
        self.norm = self.short_to_full

        placement = self.options.get("placement")
        self.placement: Placement = placement if placement is not None else Placement()
        self.parse_options()
        self.initial_placement = self.placement.copy()

        fill_algorithm = self.options["fill-algorithm"]
        if fill_algorithm == "Assumed Fill":
            start_inventory = Inventory(
                {
                    EXTENDED_ITEM[itemname]
                    for itemname in INVENTORY_ITEMS
                    if self.placement.items.get(itemname, START_ITEM) == START_ITEM
                    # Either not placed yet or a start item
                }
                | {HINT_BYPASS_BIT}
            )

            frees = Inventory(
                {EXTENDED_ITEM[itemname] for itemname in self.placement.starting_items}
                | {HINT_BYPASS_BIT}
            )
            FillAlgorithm = AssumedFill
        elif fill_algorithm == "Front Fill":
            start_inventory = Inventory({HINT_BYPASS_BIT})
            frees = start_inventory
            FillAlgorithm = FrontFill
        elif fill_algorithm == "Random Fill":
            start_inventory = Inventory()
            frees = start_inventory
            # Any would work for those two
            FillAlgorithm = RandomFill
        else:
            raise ValueError(
                f"Wrong value for option 'fill-algorithm: f'{fill_algorithm}'"
            )

        runtime_requirements = (
            self.logic_options_requirements
            | self.endgame_requirements
            | self.ban_options
            | {i: DNFInventory(True) for i in self.placement.starting_items}
            | self.no_logic_requirements
        )

        logic_settings = LogicSettings(
            start_inventory,
            frees,
            runtime_requirements,
            self.banned,
        )
        additional_info = AdditionalInfo(
            self.required_dungeons,
            self.unrequired_dungeons,
            self.randomized_dungeon_entrance,
            self.randomized_trial_entrance,
            list(self.placement.locations),
        )

        logic = Logic(areas, logic_settings, self.placement)

        self.rando_algo = FillAlgorithm(logic, self.rng, self.randosettings)

        self.randomised = False

        def fun():
            if not self.randomised:
                raise ValueError("Cannot extract hint logic before randomisation")
            return LogicUtils(
                areas,
                logic.placement,
                additional_info,
                runtime_requirements,
                self.banned,
            )

        self.extract_hint_logic = fun

    def get_total_progress_steps(self):
        return self.rando_algo.get_total_progress_steps()

    def randomize(self, useroutput: UserOutput):
        self.rando_algo.randomize(useroutput)
        self.randomised = True

    def parse_options(self):
        # Initialize location related attributes.
        self.randomize_required_dungeons()  # self.required_dungeons, self.unrequired_dungeons
        self.randomize_starting_items()  # self.placement.starting_items
        self.ban_the_banned()  # self.banned, self.ban_options

        self.get_endgame_requirements()  # self.endgame_requirements

        self.set_placement_options()  # self.logic_options_requirements

        self.initialize_items()  # self.randosettings

        self.randomize_dungeons_trials()

    def randomize_required_dungeons(self):
        """
        Selects the required dungeons randomly based on options
        """
        indices = list(range(len(REGULAR_DUNGEONS)))
        self.rng.shuffle(indices)
        nb_dungeons = self.options["required-dungeon-count"]
        req_indices = indices[:nb_dungeons]
        unreq_indices = indices[nb_dungeons:]
        req_indices.sort()
        unreq_indices.sort()
        self.required_dungeons = [REGULAR_DUNGEONS[i] for i in req_indices]
        self.unrequired_dungeons = [REGULAR_DUNGEONS[i] for i in unreq_indices]

    def randomize_starting_items(self):
        """
        Chooses all items the player has at the start,
        for tablet randomizer adds random tablets
        """
        starting_items = {
            number(PROGRESSIVE_SWORD, i)
            for i in range(SWORD_COUNT[self.options["starting-sword"]])
        }

        for tablet in self.rng.sample(TABLETS, k=self.options["starting-tablet-count"]):
            starting_items.add(tablet)

        # if self.options.get('start-with-sailcloth', True):
        #   starting_items.add('Sailcloth')
        if self.options["start-with-pouch"]:
            starting_items.add(number(PROGRESSIVE_POUCH, 0))

        self.placement = self.placement.add_starting_items(starting_items)

    def ban_the_banned(self):

        banned_req = DNFInventory(BANNED_BIT)
        nothing_req = DNFInventory(True)
        maybe_req = lambda b: banned_req if b else nothing_req
        self.ban_options = {
            BEEDLE_STALL_ACCESS: maybe_req(self.options["shop-mode"] == "Always Junk"),
            MEDIUM_PURCHASES: maybe_req("medium" in self.options["banned-types"]),
            EXPENSIVE_PURCHASES: maybe_req("expensive" in self.options["banned-types"]),
        } | {
            MAY_GET_n_CRYSTALS(c): (maybe_req(c > self.options["max-batreaux-reward"]))
            for c in CRYSTAL_THRESHOLDS
        }

        banned_types = set(self.options["banned-types"]) - {"medium", "expensive"}
        self.ban_options |= {s: maybe_req(s in banned_types) for s in BANNABLE_TYPES}

        self.banned: List[EIN] = []

        if self.options["empty-unrequired-dungeons"]:
            self.banned.extend(
                self.norm(entrance_of_exit(DUNGEON_MAIN_EXITS[dungeon]))
                for dungeon in self.unrequired_dungeons
            )

            if (
                not self.options["triforce-required"]
                or self.options["triforce-shuffle"] == "Anywhere"
            ):
                self.banned.append(self.norm(entrance_of_exit(DUNGEON_MAIN_EXITS[SK])))

    def get_endgame_requirements(self):
        # needs to be able to open GoT and open it, requires required dungeons
        got_raising_requirement = (
            DNFInventory(self.short_to_full(SONG_IMPA_CHECK))
            if self.options["got-start"]
            else DNFInventory(True)
        )
        got_opening_requirement = InventoryAtom(
            PROGRESSIVE_SWORD, SWORD_COUNT[self.options["got-sword-requirement"]]
        )
        horde_door_requirement = (
            DNFInventory(self.short_to_full(COMPLETE_TRIFORCE))
            if self.options["triforce-required"]
            else DNFInventory(True)
        )

        dungeons_req = Inventory()
        for dungeon in self.required_dungeons:
            dungeons_req |= Inventory(self.short_to_full(DUNGEON_FINAL_CHECK[dungeon]))

        if self.options["got-dungeon-requirement"] == "Required":
            got_opening_requirement &= DNFInventory(dungeons_req)
        elif self.options["got-dungeon-requirement"] == "Unrequired":
            horde_door_requirement &= DNFInventory(dungeons_req)

        everything_list = {
            check["req_index"] for check in self.areas.checks.values()
        } | {EXTENDED_ITEM[self.short_to_full(DEMISE)]}
        everything_req = DNFInventory(Inventory(everything_list))

        self.endgame_requirements = {
            GOT_RAISING_REQUIREMENT: got_raising_requirement,
            GOT_OPENING_REQUIREMENT: got_opening_requirement,
            HORDE_DOOR_REQUIREMENT: horde_door_requirement,
            EVERYTHING: everything_req,
        }

    def initialize_items(self):
        # Initialize item related attributes.
        must_be_placed_items = (
            PROGRESS_ITEMS | NONPROGRESS_ITEMS | ALL_SMALL_KEYS | ALL_BOSS_KEYS
        )
        if self.options["map-mode"] != "Removed":
            must_be_placed_items |= ALL_MAPS

        may_be_placed_list: List[EIN] = [
            item for item in CONSUMABLE_ITEMS if item not in self.placement.items
        ]
        duplicable_items = DUPLICABLE_ITEMS

        rupoor_mode = self.options["rupoor-mode"]
        if rupoor_mode != "Off":
            duplicable_items = DUPLICABLE_COUNTERPROGRESS_ITEMS  # Rupoors
            length = len(may_be_placed_list)
            self.rng.shuffle(may_be_placed_list)
            if rupoor_mode == "Added":
                unplaced = []
                # Coarsely emulate adding 15 rupoors then removing 15 elements
                for _ in range(15):
                    if (i := self.rng.randint(0, length - 1 + 15)) < length:
                        unplaced.append(may_be_placed_list[i])
            elif rupoor_mode == "Rupoor Mayhem":
                unplaced = may_be_placed_list[: length // 2]
            elif rupoor_mode == "Rupoor Insanity":
                unplaced = may_be_placed_list
            else:
                raise ValueError(f"Option rupoor-mode has unknown value {rupoor_mode}")
            self.placement = self.placement.add_unplaced_items(set(unplaced))
        may_be_placed_items = dict.fromkeys(may_be_placed_list)

        for item in self.placement.items:
            must_be_placed_items.pop(item, None)
            may_be_placed_items.pop(item, None)

        self.randosettings = RandomizationSettings(
            must_be_placed_items, may_be_placed_items, duplicable_items
        )

    def set_placement_options(self):
        shop_mode = self.options["shop-mode"]
        place_gondo_progressives = self.options["gondo-upgrades"]

        options = {
            OPEN_THUNDERHEAD_OPTION: self.options["open-thunderhead"] == "Open",
            OPEN_ET_OPTION: self.options["open-et"],
            OPEN_LMF_OPTION: self.options["open-lmf"] == "Open",
            LMF_NODES_ON_OPTION: self.options["open-lmf"] == "Main Node",
            RANDOMIZED_BEEDLE_OPTION: shop_mode != "Vanilla",
            GONDO_UPGRADES_ON_OPTION: not place_gondo_progressives,
            NO_BIT_CRASHES: self.options["fix-bit-crashes"],
            HERO_MODE: self.options["hero-mode"],
        }

        enabled_tricks = set(self.options["enabled-tricks-bitless"])

        self.logic_options_requirements = {
            k: DNFInventory(b) for k, b in options.items()
        } | {
            EIN(trick(trick_name)): DNFInventory(trick_name in enabled_tricks)
            for trick_name in OPTIONS["enabled-tricks-bitless"]["choices"]
        }

        self.no_logic_requirements = {}
        if self.options["logic-mode"] == "No Logic":
            self.no_logic_requirements = {
                item: DNFInventory(True) for item in EXTENDED_ITEM.items_list
            }

        self.placement |= SINGLE_CRYSTAL_PLACEMENT(self.norm, self.areas.checks)

        vanilla_map_transitions = {}
        vanilla_reverse_map_transitions = {}
        for exit, v in self.areas.map_exits.items():
            if (
                v["type"] == "entrance"
                or v.get("disabled", False)
                or "vanilla" not in v
            ):
                continue
            entrance = self.norm(v["vanilla"])
            vanilla_map_transitions[exit] = entrance
            vanilla_reverse_map_transitions[entrance] = exit

        self.placement |= Placement(
            map_transitions=vanilla_map_transitions,
            reverse_map_transitions=vanilla_reverse_map_transitions,
        )

        sword_reward_mode = self.options["sword-dungeon-reward"]
        if sword_reward_mode != "None":
            swords_to_place = [
                sword
                for sword in PROGRESSIVE_SWORDS
                if sword not in self.placement.items
            ]

            if sword_reward_mode == "Heart Container":
                checks_to_use = DUNGEON_HEART_CONTAINERS
            elif sword_reward_mode == "Final Check":
                checks_to_use = DUNGEON_FINAL_CHECK
            else:
                raise ValueError(
                    f"Option sword-dungeon-reward has unknown value {sword_reward_mode}"
                )

            dungeons = self.required_dungeons.copy()
            self.rng.shuffle(dungeons)
            for dungeon, sword in zip(dungeons, swords_to_place):
                final_check = self.short_to_full(checks_to_use[dungeon])
                self.placement |= Placement(
                    items={sword: final_check},
                    locations={final_check: sword},
                )

        # self.placement |= HARDCODED_PLACEMENT(self.norm)

        if self.options["open-et"]:
            self.placement = self.placement.add_unplaced_items(set(KEY_PIECES))

        if not place_gondo_progressives:
            self.placement = self.placement.add_unplaced_items(GONDO_ITEMS)

        if shop_mode == "Vanilla":
            self.placement |= VANILLA_BEEDLE_PLACEMENT(self.norm, self.areas.checks)
        elif shop_mode == "Randomized":
            pass
        elif shop_mode == "Always Junk":
            pass

        small_key_mode = self.options["small-key-mode"]
        boss_key_mode = self.options["boss-key-mode"]
        map_mode = self.options["map-mode"]
        triforce_mode = self.options["triforce-shuffle"]
        # remove small keys from the dungeon pool if small key sanity is enabled
        if small_key_mode == "Vanilla":
            self.placement |= VANILLA_SMALL_KEYS_PLACEMENT(self.norm, self.areas.checks)
        elif small_key_mode == "Own Dungeon - Restricted":
            self.placement |= DUNGEON_SMALL_KEYS_RESTRICTION(self.norm)
            self.placement |= CAVES_KEY_RESTRICTION(self.norm)
        elif small_key_mode == "Lanayru Caves Key Only":
            self.placement |= DUNGEON_SMALL_KEYS_RESTRICTION(self.norm)
        elif small_key_mode == "Anywhere":
            pass

        # remove boss keys from the dungeon pool if boss key sanity is enabled
        if boss_key_mode == "Vanilla":
            self.placement |= VANILLA_BOSS_KEYS_PLACEMENT(self.norm, self.areas.checks)
        elif boss_key_mode == "Own Dungeon":
            self.placement |= DUNGEON_BOSS_KEYS_RESTRICTION(self.norm)
        elif boss_key_mode == "Anywhere":
            pass

        # remove maps from the dungeon pool if maps are shuffled
        if map_mode == "Removed":
            pass  # Dealt with during item initialization
        elif map_mode == "Vanilla":
            self.placement |= VANILLA_MAPS_PLACEMENT(self.norm, self.areas.checks)
        elif map_mode == "Own Dungeon - Restricted":
            self.placement |= DUNGEON_MAPS_RESTRICTED_RESTRICTION(self.norm)
        elif map_mode == "Own Dungeon - Unrestricted":
            self.placement |= DUNGEON_MAPS_RESTRICTION(self.norm)
        elif map_mode == "Anywhere":
            pass

        rupeesanity = self.options["rupeesanity"]
        if rupeesanity == "Vanilla":
            self.placement |= VANILLA_RUPEES(self.norm, self.areas.checks)
        elif rupeesanity == "No Quick Beetle":
            self.placement |= VANILLA_QUICK_BEETLE_RUPEES(self.norm, self.areas.checks)
        elif rupeesanity == "All":
            pass

        if triforce_mode == "Vanilla":
            self.placement |= VANILLA_TRIFORCES_PLACEMENT(self.norm, self.areas.checks)
        elif triforce_mode == "Sky Keep":
            self.placement |= TRIFORCES_RESTRICTION(self.norm)
        elif triforce_mode == "Anywhere":
            pass

    #
    #
    # Retro-compatibility

    def reassign_entrances(
        self, exs1: list[EIN] | list[list[EIN]], exs2: list[EIN] | list[list[EIN]]
    ):
        for ex1, ex2 in zip(exs1, exs2):
            if isinstance(ex1, str):
                ex1 = [ex1]
            if isinstance(ex2, str):
                ex2 = [ex2]
            assert ex1[0] in self.placement.map_transitions
            assert ex2[0] in self.placement.map_transitions
            en1 = EIN(entrance_of_exit(ex1[0]))
            en2 = EIN(entrance_of_exit(ex2[0]))
            for exx1 in ex1:
                self.placement.map_transitions[exx1] = en2
            for exx2 in ex2:
                self.placement.map_transitions[exx2] = en1
            self.placement.reverse_map_transitions[en1] = ex2[0]
            self.placement.reverse_map_transitions[en2] = ex1[0]

    def randomize_dungeons_trials(self):
        # Do this in a deliberately hacky way, this is not supposed to be how ER works
        der = self.options["randomize-entrances"]
        dungeons = ALL_DUNGEONS.copy()
        entrances = [DUNGEON_OVERWORLD_ENTRANCES[dungeon] for dungeon in ALL_DUNGEONS]
        if der == "All Dungeons":
            indices = list(range(len(REGULAR_DUNGEONS)))
            shuffle_indices(self.rng, dungeons, indices=indices)

        elif der == "All Dungeons + Sky Keep":
            self.rng.shuffle(dungeons)

        elif der == "Required Dungeons Separately":
            req_indices = [ALL_DUNGEONS.index(d) for d in self.required_dungeons]
            unreq_indices = [ALL_DUNGEONS.index(d) for d in self.unrequired_dungeons]
            if (
                not self.options["triforce-required"]
                or self.options["triforce-shuffle"] == "Anywhere"
            ):
                unreq_indices.append(ALL_DUNGEONS.index(SK))
            else:
                req_indices.append(ALL_DUNGEONS.index(SK))
            shuffle_indices(self.rng, dungeons, indices=req_indices)
            shuffle_indices(self.rng, dungeons, indices=unreq_indices)
        else:
            assert der == "None"

        self.randomized_dungeon_entrance = {}
        for entrance, dungeon in zip(entrances, dungeons):
            self.randomized_dungeon_entrance[entrance] = dungeon

        pre_LMF_index = dungeons.index(LMF)

        dungeon_entrances = [
            [self.norm(e) for e in DUNGEON_ENTRANCE_EXITS[k]] for k in entrances
        ]
        dungeons = [[self.norm(DUNGEON_MAIN_EXITS[k])] for k in dungeons]

        if ALL_DUNGEONS[pre_LMF_index] != LMF:
            dungeons[pre_LMF_index].append(self.norm(LMF_SECOND_EXIT))

        self.reassign_entrances(dungeon_entrances, dungeons)

        ter = self.options["randomize-trials"]
        pool = ALL_SILENT_REALMS.copy()
        gates = [SILENT_REALM_GATES[realm] for realm in ALL_SILENT_REALMS]
        if ter:
            self.rng.shuffle(pool)

        self.randomized_trial_entrance = {}
        for gate, realm in zip(gates, pool):
            self.randomized_trial_entrance[gate] = realm

        trial_entrances = [self.norm(TRIAL_GATE_EXITS[k]) for k in gates]
        trials = [self.norm(SILENT_REALM_EXITS[k]) for k in pool]
        self.reassign_entrances(trial_entrances, trials)
