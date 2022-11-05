from collections import defaultdict
import json
from random import Random

from hints.hint_types import *
from logic.constants import *
from logic.logic import Logic
from paths import RANDO_ROOT_PATH


HINTABLE_ITEMS = (
    ["Clawshots"]
    + ["Progressive Beetle"] * 2
    + ["Progressive Sword"] * 6
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
    "They say there's a 35% chance for Fire Sanctuary Boss Key to be Heetle Locked",
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
    "If only we could go Back in Time and name the glitch properly...",
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
    "They say that a massive storm brews over the Lanayru Sand Sea due to Tentalus' immense size",
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
        self.goal_locations = []
        self.goals = []
        self.goal_index = 0
        self.barren_overworld_zones = []
        self.placed_ow_barren = 0
        self.barren_dungeons = []
        self.placed_dungeon_barren = 0
        self.prev_barren_type = None
        self.hinted_locations = []
        self.hintable_items = []
        self.junk_hints = []
        self.sometimes_hints = []
        self.barren_hinted_areas = set()
        self.counts_by_type = defaultdict(int)

        self.hintfuncs = {
            "sometimes": self._create_sometimes_hint,
            "sots": self._create_sots_hint,
            "goal": self._create_goal_hint,
            "barren": self._create_barren_hint,
            "item": self._create_item_hint,
            "random": self._create_random_hint,
            "junk": self._create_junk_hint,
            "bk": self._create_bk_hint,
        }

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

        for loc in self.added_locations:
            location = loc["location"]
            if loc["type"] == "always":
                if location in always_hints:
                    continue
                always_hints.append(location)
                if location in sometimes_hints:
                    sometimes_hints.remove(location)
            elif loc["type"] == "sometimes":
                if location in sometimes_hints:
                    continue
                sometimes_hints.append(location)
                if location in always_hints:
                    always_hints.remove(location)

        for loc in self.removed_locations:
            if loc in always_hints:
                always_hints.remove(loc)
            if loc in sometimes_hints:
                sometimes_hints.remove(loc)

        trial_rando = self.logic.rando.options["randomize-trials"]
        # all always hints are always hinted
        for hint in always_hints:
            self.hinted_locations.append(hint)
            if (
                trial_rando
                and hint in SILENT_REALM_CHECKS_REV
                and self.logic.rando.options["treasuresanity-in-silent-realms"] == False
            ):
                trial = SILENT_REALM_CHECKS_REV[hint]
                trial_gate = {v: k for k, v in self.logic.trial_connections.items()}[
                    trial
                ]
                trial_item = self.logic.done_item_locations[hint]
                self.hints.extend(
                    [TrialGateGossipStoneHint(hint, trial_item, trial_gate)]
                    * self.distribution["always"]["copies"]
                )
            else:
                self.hints.extend(
                    [
                        LocationGossipStoneHint(
                            "always",
                            hint,
                            self.logic.done_item_locations[hint],
                            self.logic.item_locations[hint].get("text"),
                        )
                    ]
                    * self.distribution["always"]["copies"]
                )
        self.rng.shuffle(self.hints)
        self.rng.shuffle(sometimes_hints)
        self.sometimes_hints = sometimes_hints

        # ensure prerandomized locations cannot be hinted
        self.hinted_locations.extend(
            (
                loc
                for loc in self.logic.prerandomization_item_locations.keys()
                if not self.logic.is_restricted_placement_item(
                    self.logic.done_item_locations[loc]
                )
            )
        )

        # creates a list of boss key locations for required dungeons
        self.required_boss_key_locations = [
            loc
            for loc, item in self.logic.done_item_locations.items()
            if ("Boss Key" in item)
            and Logic.split_location_name_by_zone(loc)[0]
            in self.logic.required_dungeons
        ]
        self.rng.shuffle(self.required_boss_key_locations)

        # populate our internal list copies for later manipulation
        self.sots_locations = self.loc_dict_filter(self.logic.rando.sots_locations)
        self.rng.shuffle(self.sots_locations)
        self.goals = list(self.logic.rando.goal_locations.keys())
        # shuffle the goal names that will be chosen in sequence when goal hints are placed to try to ensure one is placed for each goal
        self.rng.shuffle(self.goals)
        # create corresponding list of shuffled goal items
        self.goal_locations = [
            (self.loc_dict_filter(self.logic.rando.goal_locations[goal_name]))
            for goal_name in self.goals
        ]
        for locations in self.goal_locations:
            self.rng.shuffle(locations)

        region_barren, nonprogress = self.logic.get_barren_regions()
        for zone in region_barren:
            if (
                ("Silent Realm" in zone)
                and self.logic.rando.options["treasuresanity-in-silent-realms"] == False
                or (zone == "Flooded Faron Woods")
            ):
                continue  # don't hint barren silent realms since they are an always hint
            if self.logic.rando.options["empty-unrequired-dungeons"]:
                # avoid placing barren hints for unrequired dungeons in race mode
                if (
                    not self.logic.rando.options["triforce-required"]
                    or self.logic.rando.options["triforce-shuffle"] == "Anywhere"
                ) and (zone == SK):
                    # skykeep is always barren when race mode is on and Sky Keep is skipped
                    continue
                if (
                    zone in POTENTIALLY_REQUIRED_DUNGEONS
                    and zone not in self.logic.required_dungeons
                ):
                    # unrequired dungeons are always barren in race mode
                    continue
            if zone == SK:
                # exclude Sky Keep from the eligible barren locations if it has no open checks
                if (
                    self.logic.rando.options["map-mode"]
                    not in [
                        "Removed",
                        "Anywhere",
                    ]
                    and self.logic.rando.options["small-key-mode"] not in ["Anywhere"]
                    and self.logic.rando.options["triforce-shuffle"] not in ["Anywhere"]
                    and self.logic.rando.options["rupeesanity"]
                    not in ["No Quick Beetle", "All"]
                ):
                    continue
            if zone in ALL_DUNGEON_AREAS:
                self.barren_dungeons.append(zone)
            else:
                self.barren_overworld_zones.append(zone)

        self.hintable_items = HINTABLE_ITEMS.copy()
        for item in self.added_items:
            self.hintable_items.extend([item["name"]] * item["amount"])
        if "Sea Chart" in self.logic.all_progress_items:
            self.hintable_items.append("Sea Chart")
        for item in self.removed_items:
            if item in self.hintable_items:
                self.hintable_items.remove(item)
        for item in self.logic.starting_items:
            if item in self.hintable_items:
                self.hintable_items.remove(item)
        self.logic.rando.rng.shuffle(self.hintable_items)

        needed_fixed = []

        # for each fixed goal hint, place one for each required dungeon
        if "goal" in self.distribution.keys():
            self.distribution["goal"]["fixed"] *= len(self.logic.required_dungeons)

        for type in self.distribution.keys():
            if self.distribution[type]["fixed"] > 0:
                needed_fixed.append(type)
        needed_fixed.sort(key=lambda type: self.distribution[type]["order"])

        self.junk_hints = JUNK_TEXT.copy()
        self.rng.shuffle(self.junk_hints)

        for type in needed_fixed:
            curr_type = self.distribution[type]
            func = self.hintfuncs[type]
            for _ in range(curr_type["fixed"]):
                if hint := func():
                    self.counts_by_type[type] += 1
                    self.hints.extend([hint] * curr_type["copies"])

        # reverse the list of hints to we can pop off the back in O(1)
        # this also preserves the order they were added as they are removed so that order parameter is repsected
        self.hints.reverse()

        for hint_type in self.distribution.keys():
            self.weighted_types.append(hint_type)
            self.weights.append(self.distribution[hint_type]["weight"])

    """
    Method to filter out keys from SotS and Goal item location dictionaries and return a list of tuples of zones, locations, and items
    """

    def loc_dict_filter(self, loc_dict):
        filtered_locations = []
        for loc, item in loc_dict.items():
            if item in self.removed_items:
                continue
            if self.logic.is_restricted_placement_item(item):
                continue

            zone, specific_loc = Logic.split_location_name_by_zone(loc)
            filtered_locations.append((zone, loc, item))
        return filtered_locations

    """
    Uses the distribution to calculate all the hints
    """

    def get_hints(self, count) -> List[GossipStoneHint]:
        hints = self.hints
        while len(hints) < count:
            [next_type] = self.rng.choices(self.weighted_types, self.weights)
            if (limit := self.distribution[next_type].get("max")) is not None:
                if self.counts_by_type[next_type] >= limit:
                    continue
            if hint := self.hintfuncs[next_type]():
                self.counts_by_type[next_type] += 1
                hints.extend([hint] * self.distribution[next_type]["copies"])
        hints = hints[:count]
        return hints

    def _create_sometimes_hint(self):
        if not self.sometimes_hints:
            return None
        hint = self.sometimes_hints.pop()
        if hint in self.hinted_locations:
            return self._create_sometimes_hint()
        self.hinted_locations.append(hint)
        return LocationGossipStoneHint(
            "sometimes",
            hint,
            self.logic.done_item_locations[hint],
            self.logic.item_locations[hint].get("text"),
        )

    def _create_sots_hint(self):
        if not self.sots_locations:
            return None
        zone, loc, item = self.sots_locations.pop()
        if loc in self.hinted_locations:
            return self._create_sots_hint()
        if (
            self.sots_dungeon_placed >= self.dungeon_sots_limit
            and zone in ALL_DUNGEON_AREAS
        ):
            return self._create_sots_hint()
        if zone in ALL_DUNGEON_AREAS:
            self.sots_dungeon_placed += 1
        self.hinted_locations.append(loc)
        if "Goddess Chest" in loc:
            zone = self.logic.rando.item_locations[loc]["cube_region"]
            # place cube sots hint & catch specific zones and fit them into their general zone (as seen in the cube progress options)
            if self.logic.rando.options["cube-sots"]:
                if zone == SV:
                    zone = "Faron Woods"
                elif zone == "Mogma Turf":
                    zone = "Eldin Volcano"
                elif zone == "Lanayru Mines":
                    zone = "Lanayru Desert"
                elif zone == "Lanayru Gorge":
                    zone = "Lanayru Sand Sea"
                return CubeSotsGoalGossipStoneHint(loc, item, zone)
        return SotsGoalGossipStoneHint(loc, item, zone)

    def _create_goal_hint(self):
        if not self.goal_locations[self.goal_index]:
            # if there aren't applicable locations for any goal, return None
            if not any(self.goal_locations):
                return None
            # go to next goal if no locations are left for this goal
            self.goal_index += 1
            self.goal_index %= len(self.goals)
            return self._create_goal_hint()
        zone, loc, item = self.goal_locations[self.goal_index].pop()
        if loc in self.hinted_locations:
            return self._create_goal_hint()
        if (
            self.sots_dungeon_placed >= self.dungeon_sots_limit
            and zone in ALL_DUNGEON_AREAS
        ):
            return self._create_goal_hint()
        if zone in ALL_DUNGEON_AREAS:
            # goal hints will use the same dungeon limits as sots hints
            self.sots_dungeon_placed += 1
        self.hinted_locations.append(loc)
        # move to next goal boss for next goal hint
        self.goal_index += 1
        self.goal_index %= len(self.goals)
        goal = self.goals[self.goal_index - 1]
        if "Goddess Chest" in loc:
            zone = self.logic.rando.item_locations[loc]["cube_region"]
            # place cube sots hint & catch specific zones and fit them into their general zone (as seen in the cube progress options)
            if self.logic.rando.options["cube-sots"]:
                if zone == SV:
                    zone = "Faron Woods"
                elif zone == "Mogma Turf":
                    zone = "Eldin Volcano"
                elif zone == "Lanayru Mines":
                    zone = "Lanayru Desert"
                elif zone == "Lanayru Gorge":
                    zone = "Lanayru Sand Sea"
                return CubeSotsGoalGossipStoneHint(loc, item, zone, goal)
        return SotsGoalGossipStoneHint(loc, item, zone, goal)

    def _create_barren_hint(self):
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
                return None
        if (
            len(self.barren_overworld_zones) == 0
            and self.prev_barren_type == "overworld"
        ):
            self.prev_barren_type = "dungeon"
            if len(self.barren_dungeons) == 0:
                return None

        # generate a hint and remove it from the lists
        if self.prev_barren_type == "dungeon":
            barren_area_list = self.barren_dungeons
        else:
            barren_area_list = self.barren_overworld_zones
        weights = [
            len(self.logic.prog_locations_by_zone_name[area])
            for area in barren_area_list
        ]
        area = self.rng.choices(barren_area_list, weights)[0]
        barren_area_list.remove(area)
        self.barren_hinted_areas.add(area)
        return BarrenGossipStoneHint(area)

    def _create_item_hint(self):
        if not self.hintable_items:
            return None
        hinted_item = self.hintable_items.pop()
        locs = [
            (location, item)
            for location, item in self.logic.done_item_locations.items()
            if item == hinted_item and location not in self.hinted_locations
        ]
        if not locs:
            return None
        location, item = self.rng.choice(locs)
        self.hinted_locations.append(location)
        if self.logic.rando.options["precise-item"]:
            return LocationGossipStoneHint(
                "precise_item",
                location,
                item,
                self.logic.item_locations[location].get("text"),
            )
        zone_override, _ = self.logic.split_location_name_by_zone(location)
        if "Goddess Chest" in location:
            zone_override = self.logic.rando.item_locations[location]["cube_region"]
        return ZoneItemGossipStoneHint(location, item, zone_override)

    def _create_random_hint(self):
        all_locations_without_hint = self.logic.filter_locations_for_progression(
            (
                loc
                for loc in self.logic.done_item_locations
                if not loc in self.hinted_locations
                and not loc in self.logic.prerandomization_item_locations
                and Logic.split_location_name_by_zone(loc)[0]
                not in self.barren_hinted_areas
            )
        )
        loc = self.rng.choice(all_locations_without_hint)
        self.hinted_locations.append(loc)
        return LocationGossipStoneHint(
            "random",
            loc,
            self.logic.done_item_locations[loc],
            self.logic.item_locations[loc].get("text"),
        )

    def _create_bk_hint(self):
        if not self.required_boss_key_locations:
            return None
        loc = self.required_boss_key_locations.pop()
        if loc in self.hinted_locations:
            return self._create_bk_hint()
        self.hinted_locations.append(loc)
        return LocationGossipStoneHint(
            "boss_key",
            loc,
            self.logic.done_item_locations[loc],
            self.logic.item_locations[loc].get("text"),
        )

    def _create_junk_hint(self):
        return EmptyGossipStoneHint(self.junk_hints.pop())

    def get_junk_text(self):
        return self.junk_hints.pop()
