from hints.hint_distribution import HintDistribution
from hints.hint_types import *
from .logic import Logic
from paths import RANDO_ROOT_PATH
import yaml
from collections import OrderedDict, defaultdict
from dataclasses import dataclass
from typing import List

from .constants import (
    POTENTIALLY_REQUIRED_DUNGEONS,
    ALL_DUNGEON_AREAS,
    SILENT_REALMS,
    SILENT_REALM_CHECKS,
)
from util import textbox_utils

HINTABLE_ITEMS = (
    ["Clawshots"]
    + ["Progressive Beetle"] * 2
    + ["Progressive Sword"] * 4
    + ["Emerald Tablet"] * 1
    + ["Ruby Tablet"] * 1
    + ["Amber Tablet"] * 1
    + ["Goddess Harp"] * 1
    + ["Water Scale"] * 1
    + ["Fireshield Earrings"] * 1
)

ALWAYS_REQUIRED_LOCATIONS = [
    "Thunderhead - Song from Levias",
    "Sky - Kina's Crystals",
    "Central Skyloft - Peater/Peatrice's Crystals",
    "Batreaux - 80 Crystals",
    "Lanayru Mining Facility - Boss Key Chest",
    "Fire Sanctuary - Chest after Bombable Wall",
]

SOMETIMES_LOCATIONS = [
    "Lanayru Sand Sea - Rickety Coaster - Heart Stopping Track in 1'05",
    "Knight Academy - Pumpkin Archery - 600 Points",
    "Sky - Lumpy Pumpkin Harp Minigame",
    "Sky - Fun Fun Island Minigame - 500 Rupees",
    "Thunderhead - Bug Heaven - 10 Bugs in 3 Minutes",
    "Batreaux - 70 Crystals Second Reward",
    "Batreaux - 70 Crystals",
    "Batreaux - 50 Crystals",
    "Knight Academy - Owlan's Crystals",
    "Skyloft Village - Sparrot's Crystals",
    "Lanayru Desert - Chest on top of Lanayru Mining Facility",
    "Central Skyloft - Waterfall Goddess Chest",  # stronghold cube
    "Sky - Beedle's Island Goddess Chest",  # goddess cube in ToT area
    "Skyview - Chest behind Three Eyes",
    "Sandship - Boss Key Chest",
    "Sandship - Tentalus Heart Container",
    "Sandship - Bow",
    "Thunderhead - Isle of Songs - Din's Power",
    "Sealed Grounds - Zelda's Blessing",
    "Lanayru Sand Sea - Skipper's Retreat - Chest in Shack",
    "Volcano Summit - Item behind Digging",
    "Faron Woods - Slingshot",
    "Sky - Beedle's Crystals",
    "Sealed Grounds - Gorko's Goddess Wall Reward",
]


class Hints:
    def __init__(self, logic: Logic):
        self.stonehint_definitions = logic.rando.stonehint_definitions
        self.logic = logic
        for hintname, hintdef in self.stonehint_definitions.items():
            if self.logic.rando.options["logic-mode"] == "No Logic":
                hintdef["Need"] = Logic.parse_logic_expression(hintname, "Nothing")
            else:
                hintdef["Need"] = self.logic.macros[hintname]
        self.hints = OrderedDict()
        with open(
            RANDO_ROOT_PATH
            / f"hints/distributions/{self.logic.rando.options['hint-distribution']}.json"
        ) as f:
            self.dist = HintDistribution()
            self.dist.read_from_file(f)

    def do_hints(self):
        needed_always_hints = self.logic.filter_locations_for_progression(
            [
                loc
                for loc in self.logic.item_locations.keys()
                if "hint" in self.logic.item_locations[loc]
                and self.logic.item_locations[loc]["hint"] == "always"
            ]
        )
        # in shopsanity, we need to hint some beetle shop items
        # add them manually, cause they need to be kinda weirdly implemented because of bug net
        if (
            self.logic.rando.options["shop-mode"] == "Randomized"
            and "expensive" not in self.logic.rando.options["banned-types"]
        ):
            needed_always_hints.append("Beedle - 1200 Rupee Item")
            needed_always_hints.append("Beedle - 1600 Rupee Item")
        if self.logic.rando.options["song-hints"] == "None":
            needed_always_hints.append("Skyloft Silent Realm - Stone of Trials")
            needed_always_hints.append("Faron Silent Realm - Water Scale")
            needed_always_hints.append("Lanayru Silent Realm - Clawshots")
            needed_always_hints.append("Eldin Silent Realm - Fireshield Earrings")
        needed_sometimes_hints = self.logic.filter_locations_for_progression(
            [
                loc
                for loc in self.logic.item_locations.keys()
                if "hint" in self.logic.item_locations[loc]
                and self.logic.item_locations[loc]["hint"] == "sometimes"
            ]
        )
        self.dist.start(self.logic, needed_always_hints, needed_sometimes_hints)
        hints = []
        i = 0
        while i < 32:
            hint = self.dist.next_hint()
            if hint is not None:
                hints.append(hint)
                i += 1
        self._place_hints_for_locations(hints)

    def _place_hints_for_locations(self, hints: List[GossipStoneHint]):
        # make sure hint locations aren't locked by the item they hint
        hint_banned_stones = defaultdict(set)
        for hint in hints:
            if not hint.needs_logic:
                # hints with no logic don't have any banned stones
                # this also short circuits type errors for hints that don't have locations
                continue
            if hint.location in SILENT_REALM_CHECKS.keys():
                loc_trial_gate = SILENT_REALM_CHECKS[hint.location]
                trial_gate_dest = self.logic.trial_connections[loc_trial_gate]
                trial_gate_dest_loc = [
                    trial
                    for trial in SILENT_REALM_CHECKS.keys()
                    if trial_gate_dest in trial
                ].pop()
                hinted_trial = trial_gate_dest_loc
                hinted_item = self.logic.done_item_locations[trial_gate_dest_loc]
                if hinted_item in self.logic.all_progress_items:
                    for (
                        gossipstone_name,
                        gossipstone_def,
                    ) in self.stonehint_definitions.items():
                        if not self.logic.can_reach_restricted(
                            [hinted_trial], gossipstone_def["Need"]
                        ):
                            hint_banned_stones[gossipstone_name].add(hint)
            else:
                hinted_item = self.logic.done_item_locations[hint.location]
                if hinted_item in self.logic.all_progress_items:
                    for (
                        gossipstone_name,
                        gossipstone_def,
                    ) in self.stonehint_definitions.items():
                        if not self.logic.can_reach_restricted(
                            [hint.location], gossipstone_def["Need"]
                        ):
                            hint_banned_stones[gossipstone_name].add(hint)

        stones_to_banned_locs_sorted = sorted(
            hint_banned_stones.items(), key=lambda x: len(x[1]), reverse=True
        )

        if len(hints) < len(self.stonehint_definitions) * 2:
            hints.extend([None] * (len(self.stonehint_definitions) * 2 - len(hints)))
        unplace_hints = hints.copy()

        hint_to_location = {}
        # place locations that are restricted in locations
        for gossipstone_name, banned_locations in stones_to_banned_locs_sorted:
            valid_locations = [
                loc for loc in unplace_hints if not loc in banned_locations
            ]
            if len(valid_locations) == 0:
                print(
                    f"no valid location for {gossipstone_name} in seed {self.logic.rando.seed}"
                )
                loc_to_hint = unplace_hints[0]
                second_loc_to_hint = unplace_hints[1]
                # raise Exception('no valid location to place hint!')
            else:
                loc_to_hint = self.logic.rando.rng.choice(valid_locations)
                # ensure we dont try to place the same hint twice
                removed_list = valid_locations.copy()
                removed_list.remove(loc_to_hint)
                second_loc_to_hint = self.logic.rando.rng.choice(removed_list)
            hint_to_location[gossipstone_name] = [loc_to_hint, second_loc_to_hint]
            unplace_hints.remove(loc_to_hint)
            unplace_hints.remove(second_loc_to_hint)
        # place locations that aren't restricted and also fill rest of locations
        for gossipstone_name in [
            name for name in self.stonehint_definitions if not name in hint_to_location
        ]:
            if len(unplace_hints) == 0:
                # placeholder
                hint_to_location[gossipstone_name] = [None]
                continue
            loc_to_hint = self.logic.rando.rng.choice(unplace_hints)
            unplace_hints.remove(loc_to_hint)
            second_loc_to_hint = self.logic.rando.rng.choice(unplace_hints)
            unplace_hints.remove(second_loc_to_hint)
            hint_to_location[gossipstone_name] = [loc_to_hint, second_loc_to_hint]
        anywhere_hints = [hint for hint in hints if not hint.needs_logic]
        self.logic.rando.rng.shuffle(anywhere_hints)

        for gossipstone_name in self.stonehint_definitions:
            if gossipstone_name in self.dist.banned_stones:
                self.hints[gossipstone_name] = EmptyGossipStoneHint(
                    None, None, False, self.dist.get_junk_text()
                )
            else:
                locs_to_hint = hint_to_location[gossipstone_name]
                loc_to_hint = locs_to_hint[0]
                second_loc_to_hint = locs_to_hint[1]
                if second_loc_to_hint is None and loc_to_hint is not None:
                    if len(anywhere_hints) > 0:
                        self.hints[gossipstone_name] = GossipStoneHintWrapper(
                            loc_to_hint,
                            BarrenGossipStoneHint(zone=anywhere_hints.pop()),
                        )
                    else:
                        self.hints[gossipstone_name] = loc_to_hint
                elif second_loc_to_hint is not None and loc_to_hint is None:
                    if len(anywhere_hints) > 0:
                        self.hints[gossipstone_name] = GossipStoneHintWrapper(
                            BarrenGossipStoneHint(zone=anywhere_hints.pop()),
                            second_loc_to_hint,
                        )
                    else:
                        self.hints[gossipstone_name] = second_loc_to_hint
                elif loc_to_hint is None:
                    # place barren hints at locations with no hints
                    if len(anywhere_hints) < 0:
                        hint = anywhere_hints.pop()
                    else:
                        hint = None
                    if hint is not None:
                        self.hints[gossipstone_name] = hint
                    else:
                        self.hints[gossipstone_name] = EmptyGossipStoneHint(
                            None, None, False, self.dist.get_junk_text()
                        )
                else:
                    self.hints[gossipstone_name] = GossipStoneHintWrapper(
                        loc_to_hint, second_loc_to_hint
                    )
