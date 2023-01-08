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
from .logic_utils import AdditionalInfo, LogicUtils
from .logic_input import Areas
from .logic_expression import DNFInventory, InventoryAtom
from .inventory import (
    Inventory,
    EXTENDED_ITEM,
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

        starting_items |= {
            number(HEART_CONTAINER, i)
            for i in range(self.options["starting-heart-containers"])
        }

        starting_items |= {
            number(HEART_PIECE, i) for i in range(self.options["starting-heart-pieces"])
        }

        if not self.options["open-et"]:
            starting_items |= {
                number(KEY_PIECE, i)
                for i in range(self.options["starting-items"].count(KEY_PIECE))
            }

        for item in self.options["starting-items"]:
            if item == KEY_PIECE:
                continue
            elif item not in EXTENDED_ITEM.items_list:
                if number(item, 0) not in starting_items:
                    for count in range(self.options["starting-items"].count(item)):
                        starting_items.add(number(item, count))
                else:  # Skips over duplicate entries for Progressive Items.
                    continue
            else:
                starting_items.add(item)

        if self.options["random-starting-item"]:

            possible_random_starting_items = [
                item
                for item in RANDOM_STARTING_ITEMS
                if item not in self.options["starting-items"]
            ]
            if len(possible_random_starting_items) == 0:
                raise ValueError(
                    "All valid progress items have already been added as starting items."
                )
            else:
                random_item = self.rng.choice(possible_random_starting_items)
                if random_item not in EXTENDED_ITEM.items_list:
                    random_item = number(random_item, 0)
                starting_items.add(random_item)

        if self.options["map-mode"] == "Removed":
            self.placement.add_unplaced_items(set(ALL_MAPS) - starting_items)

        self.placement.add_starting_items(starting_items)

    def ban_the_banned(self):

        banned_req = DNFInventory(BANNED_BIT)
        nothing_req = DNFInventory(True)
        maybe_req = lambda b: banned_req if b else nothing_req
        self.ban_options = {
            BEEDLE_STALL_ACCESS: maybe_req(self.options["shop-mode"] == "Always Junk"),
            MEDIUM_PURCHASES: maybe_req(
                self.options["shop-mode"] == "Randomized - Cheap"
            ),
            EXPENSIVE_PURCHASES: maybe_req(
                self.options["shop-mode"] == "Randomized - Cheap"
                or self.options["shop-mode"] == "Randomized - Medium"
            ),
        } | {
            MAY_GET_n_CRYSTALS(c): (maybe_req(c > self.options["max-batreaux-reward"]))
            for c in CRYSTAL_THRESHOLDS
        }

        self.banned: List[EIN] = []
        self.banned.extend(map(self.norm, self.options["excluded-locations"]))

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
        rupoor_mode = self.options["rupoor-mode"]
        if rupoor_mode != "Off":
            may_be_placed_list: List[EIN] = [
                item for item in CONSUMABLE_ITEMS if item not in self.placement.items
            ]
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
            self.placement.add_unplaced_items(set(unplaced))

        must_be_placed_items = (
            PROGRESS_ITEMS
            | NONPROGRESS_ITEMS
            | ALL_SMALL_KEYS
            | ALL_BOSS_KEYS
            | ALL_MAPS
        )
        may_be_placed_items = CONSUMABLE_ITEMS.copy()
        duplicable_items = (
            DUPLICABLE_ITEMS
            if rupoor_mode != "Off"
            else DUPLICABLE_COUNTERPROGRESS_ITEMS  # Rupoors
        )

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
            self.placement.add_unplaced_items(set(KEY_PIECES))

        if not place_gondo_progressives:
            self.placement.add_unplaced_items(GONDO_ITEMS)

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
            pass
            # handled later
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
            self.placement |= VANILLA_TRIFORCES_PLACEMENT(self.norm)
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
