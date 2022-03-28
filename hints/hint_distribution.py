from collections import defaultdict
import json
from pprint import pprint
from random import Random
from typing import Tuple
from xmlrpc.client import Boolean

import yaml

from hints.hint_types import *
from logic.constants import POTENTIALLY_REQUIRED_DUNGEONS, ALL_DUNGEON_AREAS
from logic.logic import Logic
from paths import RANDO_ROOT_PATH


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

JUNK_TEXT = [
    "They say that crashing in BiT is easy.",
    "They say that bookshelves can talk",
    "They say that people who love the Bug Net also like Trains",
    "They say that there is a Gossip Stone by the Temple of Time",
    "They say there's a 35% chance for FS Boss Key to be Heetle Locked",
    "They say 64bit left Fire Sanctuary without learning Ballad of the Goddess",
    "They say that Ancient Cistern is haunted by the ghosts of softlocked Links",
    "They say the Potion Lady is still holding onto a Spiral Charge for CJ",
    "They say there is a chest underneath the party wheel in Lanayru",
    "They say that you need the hero's tunic to sleep on the main part of Skyloft",
    "They say that you need to Hot the Spile to defeat Imprisoned 2",
    "They say whenever Spiral Charge is on a trial, a seed roller goes mysteriously missing",
    "They say that Eldin Trial is vanilla whenever it is required",
    "They say that gymnast86 won the first randomizer tournament and retired immediately after",
    "They say that Mogmas don't understand Minesweeper",
    "They say that you can win a race by abandoning Lanayru to check Cawlin's Letter",
    "They say that tornados spawn frequently in the Sky",
    "They say Scrapper gets easily tilted",
    "They say there is a chest on the cliffs by the Goddess Statue",
    "They say that entering Ancient Cistern with no B items has a 1% chance of success",
    "They say that Glittering Spores are the best bird drugs",
    "They say that the Ancient Automaton fears danger darts",
    "They say the single tumbling plant is required every seed",
    "They say that your battery is low",
    "They say that you just have to get the right checks to win",
    "They say that rushing Peatrice is the play",
    "They say there is a 0.0000001164% chance your RNG won't change",
    "If only we could go Back in Time and name the glitch properly..."
    'They say that there is something called a "hash" that makes it easier for people to verify that they are playing the right seed',
    "They say that the bad seed rollers are still in the car, seeking for a safe refugee",
    "Have you heard the tragedy of Darth Kolok the Pause? I thought not, it's not a story the admins would tell you",
    "Sand Sea is the most hated region in the game, because Sand is coarse, rough and gets everywhere",
    "They say that rice has magical properties when visiting Yerbal",
    "They say that Jannon is still jammin to this day",
    "They say that there is only one place where the Slingshot beats the Bow",
    "They say that Koloktos waiting caused a civil war among players",
    "They say that there is a settings combination which needs 0 checks to be completed",
    "They say that avoiding Fledge's item from a fresh file is impossible",
    "... astronomically ...",
    "They say that you can open the chest behind bars in LMF after raising said bars",
    "They say that you look like you have a Questions",
    "They say that HD randomizer development is delayed by a day every time someone asks about it in the Discord",
    "The disc could not be read. Refer to the Wii Operations Manual for details.",
]


class InvalidHintDistribution(Exception):
    pass


class HintDistribution:
    def __init__(self):
        self.banned_stones = []
        self.added_locations = []
        self.removed_locations = []
        self.added_items = []
        self.removed_items = []
        self.sots_dungeon_placed = 0
        self.dungeon_sots_limit = 0
        self.sots_dungeon_placed = 0
        self.dungeon_barren_limit = 0
        self.distribution = {}
        self.rng: Random = None
        self.logic = None
        self.hints = []
        self.weighted_types = []
        self.weights = []
        self.sots_locations = []
        self.barren_overworld_zones = []
        self.placed_ow_barren = 0
        self.barren_dungeons = []
        self.placed_dungeon_barren = 0
        self.prev_barren_type = None
        self.hinted_locations = []
        self.weighted_types = []
        self.weights = []
        self.hintable_items = []
        self.ready = False
        self.junk_hints = []

    def read_from_file(self, f):
        self._read_from_json(json.load(f))

    def read_from_str(self, s):
        self._read_from_json(json.loads(s))

    def _read_from_json(self, jsn):
        self.banned_stones = jsn["banned_stones"]
        self.added_locations = jsn["added_locations"]
        self.removed_locations = jsn["removed_locations"]
        self.added_items = jsn["added_items"]
        self.removed_items = jsn["removed_items"]
        self.dungeon_sots_limit = jsn["dungeon_sots_limit"]
        self.dungeon_barren_limit = jsn["dungeon_barren_limit"]
        self.distribution = jsn["distribution"]

    """
    Performs initial calculations and populates the distributions internal
    tracking mechanisms for hint generation
    """

    def start(self, logic: Logic, always_hints: list, sometimes_hints: list):
        self.rng = logic.rando.rng
        self.logic = logic


        hint_descriptors = {}
        for name, loc in self.logic.item_locations.items():
            if "text" in loc:
                hint_descriptors[name] = loc["text"]
        for name, loc in self.logic.item_locations.items():
            if "text" not in loc:
                hint_descriptors[name] = name + " has"

        for loc in self.added_locations:
            location = loc["location"]
            if loc["type"] == "always":
                always_hints.append(loc["location"])
                if location in sometimes_hints:
                    sometimes_hints.remove(location)
            elif loc["type"] == "sometimes":
                always_hints.append(loc["location"])
                if location in sometimes_hints:
                    always_hints.remove(location)

        for loc in self.removed_locations:
            always_hints.remove(loc)
            sometimes_hints.remove(loc)

        # all always hints are always hinted
        for hint in always_hints:
            self.hints.append(
                LocationGossipStoneHint(
                    hint,
                    self.logic.done_item_locations[hint],
                    True,
                    hint_descriptors[hint],
                )
            )
        self.rng.shuffle(self.hints)

        # calculate sometimes hints
        sometimes_coverage = self.distribution["sometimes"]["coverage"]
        if sometimes_coverage > 0:
            # we want to cover a specific portion of the available sometimes hints
            num_sometimes = len(sometimes_hints) * sometimes_coverage
        else:
            # cover a given number of sometimes hints
            num_sometimes = self.distribution["sometimes"]["fixed"]
        self.rng.shuffle(sometimes_hints)
        if len(sometimes_hints) < num_sometimes:
            num_sometimes = len(sometimes_hints)
        for i in range(num_sometimes):
            hint = sometimes_hints[i]
            self.hints.append(
                LocationGossipStoneHint(
                    hint,
                    self.logic.done_item_locations[hint],
                    True,
                    hint_descriptors[hint],
                )
            )

        # reverse the list of hints to we can pop off the back in O(1) in next_hint ()
        self.hints.reverse()

        # populate our internal list copies for later manipulation
        for sots_loc, item in self.logic.rando.sots_locations.items():
            if self.logic.rando.options["small-key-mode"] not in [
                "Anywhere",
                "Lanayru Caves Key Only",
            ]:
                # don't hint small keys unless keysanity is on
                if item.endswith("Small Key"):
                    continue
            elif self.logic.rando.options["small-key-mode"] == "Lanayru Caves Key Only":
                if item.endswith("Small Key") and item != "LanayruCaves Small Key":
                    continue

            if self.logic.rando.options["boss-key-mode"] not in ["Anywhere"]:
                # don't hint boss keys unless keysanity is on
                if item.endswith("Boss Key"):
                    continue
            zone, specific_loc = Logic.split_location_name_by_zone(sots_loc)
            self.sots_locations.append((zone, sots_loc, item))

        region_barren, nonprogress = self.logic.get_barren_regions()
        for zone in region_barren:
            if "Silent Realm" in zone:
                continue  # don't hint barren silent realms since they are an always hint
            if self.logic.rando.options["empty-unrequired-dungeons"]:
                # avoid placing barren hints for unrequired dungeons in race mode
                if self.logic.rando.options["skip-skykeep"] and zone == "Sky Keep":
                    # skykeep is always barren when race mode is on and Sky Keep is skipped
                    continue
                if (
                    zone in POTENTIALLY_REQUIRED_DUNGEONS
                    and zone not in self.logic.required_dungeons
                ):
                    # unrequired dungeons are always barren in race mode
                    continue
            if zone == "Sky Keep":
                # exclude Sky Keep from the eligible barren locations if it has no open checks
                if self.logic.rando.options["map-mode"] not in [
                    "Removed, Anywhere"
                ] or self.logic.rando.options["small-key-mode"] not in ["Anywhere"]:
                    continue
            if zone in ALL_DUNGEON_AREAS:
                self.barren_dungeons.append(zone)
            else:
                self.barren_overworld_zones.append(zone)

        self.hintable_items = HINTABLE_ITEMS.copy()
        self.logic.rando.rng.shuffle(self.hintable_items)

        for hint_type in self.distribution.keys():
            self.weighted_types.append(hint_type)
            self.weights.append(self.distribution[hint_type]["weight"])

        self.junk_hints = JUNK_TEXT.copy()
        self.rng.shuffle(self.junk_hints)

    """
    Uses the distribution to calculate the next hint
    """

    def next_hint(self) -> GossipStoneHint:
        if len(self.hints) > 0:
            return self.hints.pop()
        [next_type] = self.rng.choices(self.weighted_types, self.weights)
        if next_type == "sots":
            zone, loc, item = self.sots_locations.pop()
            if self.sots_dungeon_placed >= self.dungeon_sots_limit:
                while zone in ALL_DUNGEON_AREAS:
                    zone, loc, item = self.sots_locations.pop()
            elif zone in ALL_DUNGEON_AREAS:
                self.sots_dungeon_placed += 1
            return SpiritOfTheSwordGossipStoneHint(loc, item, True, zone)
        elif next_type == "barren":
            if self.prev_barren_type is None:
                # 50/50 between dungeon and overworld on the first hint
                self.prev_barren_type = self.rng.choices(
                    ["dungeon", "overworld"], [0.5, 0.5]
                )[0]
            elif self.prev_barren_type == "dungeon":
                self.prev_barren_type = self.rng.choices(
                    ["dungeon", "overworld"], [0.25, 0.75]
                )[0]
            elif self.prev_barren_type == "overworld":
                self.prev_barren_type = self.rng.choices(
                    ["dungeon", "overworld"], [0.75, 0.25]
                )[0]

            # Check against caps
            if self.prev_barren_type == "dungeon":
                if self.placed_dungeon_barren > self.dungeon_barren_limit:
                    self.prev_barren_type = "overworld"

            # Failsafes if there are not enough barren hints to fill out the generated hint
            if len(self.barren_dungeons) == 0 and self.prev_barren_type == "dungeon":
                self.prev_barren_type = "overworld"
                if len(self.barren_overworld_zones) == 0:
                    return EmptyGossipStoneHint(
                        None, None, False, self.junk_hints.pop()
                    )
            if (
                len(self.barren_overworld_zones) == 0
                and self.prev_barren_type == "overworld"
            ):
                self.prev_barren_type = "dungeon"
                if len(self.barren_dungeons) == 0:
                    return EmptyGossipStoneHint(
                        None, None, False, self.junk_hints.pop()
                    )

            # generate a hint and remove it from the lists
            if self.prev_barren_type == "dungeon":
                weights = [
                    len(self.logic.locations_by_zone_name[area])
                    for area in self.barren_dungeons
                ]
                area = self.rng.choices(self.barren_dungeons, weights)[0]
                self.barren_dungeons.remove(area)
                return BarrenGossipStoneHint(None, None, False, area)
            else:
                weights = [
                    len(self.logic.locations_by_zone_name[area])
                    for area in self.barren_overworld_zones
                ]
                area = self.rng.choices(self.barren_overworld_zones, weights)[0]
                self.barren_overworld_zones.remove(area)
                return BarrenGossipStoneHint(None, None, False, area)
        elif next_type == "item":
            hinted_item = self.hintable_items.pop()
            for location, item in self.logic.done_item_locations.items():
                if item == hinted_item and location not in self.hinted_locations:
                    self.hinted_locations.append(location)
                    return ItemGossipStoneHint(location, item, True)
        # junk hint is the last possible type and also a fallback
        return EmptyGossipStoneHint(None, None, False, self.junk_hints.pop())

    def get_junk_text(self):
        return self.junk_hints.pop()
