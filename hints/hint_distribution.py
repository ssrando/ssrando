from __future__ import annotations
from collections import defaultdict
import json
from random import Random
from typing import Literal, Tuple
from logic.inventory import EXTENDED_ITEM
from logic.logic_input import Areas

from logic.constants import *
from hints.hint_types import *
from options import Options
from logic.randomize import LogicUtils
from logic.fill_algo_common import UserOutput

HINTABLE_ITEMS = (
    dict.fromkeys(
        [
            CLAWSHOTS,
            EMERALD_TABLET,
            RUBY_TABLET,
            AMBER_TABLET,
            GODDESS_HARP,
            WATER_DRAGON_SCALE,
            FIRESHIELD_EARRINGS,
        ]
    )
    | PROGRESSIVE_BEETLES
    | PROGRESSIVE_SWORDS
)

JUNK_TEXT = [
    "They say whenever Spiral Charge is on a trial, a seed roller goes mysteriously missing",
    "They say that Mogmas don't understand Minesweeper",
    "They say that you can win a race by abandoning Lanayru to check Cawlin's Letter",
    'They say that there is something called a "hash" that makes it easier for people to verify that they are playing the right seed',
    "They say that the bad seed rollers are still in the car, seeking for a safe refuge",
    "Have you heard the tragedy of Darth Kolok the Pause? I thought not, it's not a story the admins would tell you",
    "Lanayru Sand Sea is the most hated region in the game, because Sand is coarse, rough and gets everywhere",
    "... astronomically ...",
    "They say that you look like you have a Questions",
    "They say that HD randomizer development is delayed by a day every time someone asks about it in the Discord",
    "They say that a massive storm brews over the Lanayru Sand Sea due to Tentalus' immense size",
    "They say rushing Digspot RBM is always optimal",
    "They say orphaning LMF BK Chest can't hurt you",
    "They say trying to deathwarp at the end of Lightning Node rewards you with a Triforce",
    "They say an optimal Cistern Clip is performed in 4 cycles",
    "They say Jade is on the prowl, looking for innocent Kikwis to eat",
    "They say Batreaux only ever gives refunds",
    "They say Fledge not giving you an item is always a bad sign",
    "DVDRead(): specified area is out of the file",
    "They say Skipper's Retreat originated from a nightmare Aonuma once had",
    "They say RayStormThunder is very excited for this race",
    "They say barren Eldin Volcano probably still has progression",
    "They say Scervo RBM decides races",
    "They say Tentalus is allergic to dust",
    "They say Lanyru Caves - Chest is an omnipotent being",
    "They say Nindy will never stop begging for Bizarre Bazaar",
    "They say East Island Chest requires Digging Mitts",
    "They say a tornado runs through Mallara's house every day",
    "They say that Sledgen is swimming in a volcanic mass of guacamole somewhere",
    "They say Ancient Cistern was called Jannon's Castle throughout most of Skyward Sword's devlopment, and was only changed last-second",
    "You've met with a terrible fait, ouais ouais?",
    "They say the dirtiest woman in the world lives on Skyloft",
    "They say Koloktos' sword is placed somewhere in the seed",
    "Shoutouts to robojumper & cjs07 for the help with this build!",
    "How's the seed so far? Click here to leave TreZ a review:",
    "They say Bokoblin Base is barren blocked by the Bug Net",
]


class HintAssignment:
    """
    A hint assignment is a way to assign hints to various sources, like Fi and Gossip Stones (and maybe more in the future).
    """

    def __init__(self, dist):
        self.dist = dist

    def read_from_json(self, _jsn):
        raise NotImplementedError

    def is_done(self):
        raise NotImplementedError

    def accept_hint(self, hint, hint_def):
        raise NotImplementedError

    def get_hints(self):
        raise NotImplementedError


class SplitHintAssignment(HintAssignment):
    """
    "Split" hint assignment assigns the first `fi_hints` hints to Fi and
    (num_unbanned_stones * hints_per_stone) hints to gossip stones, in generation order
    """

    def __init__(self, dist):
        super().__init__(dist)
        self.hints = []
        self.num_total_hints = None

    def read_from_json(self, jsn):
        self.fi_hints = jsn["fi_hints"]
        self.hints_per_stone = jsn["hints_per_stone"]

    def is_done(self):
        if self.num_total_hints == None:
            self.num_total_hints = self.fi_hints + sum(
                0 if stone in self.dist.banned_stones else self.hints_per_stone
                for stone in self.dist.areas.gossip_stones
            )

        return len(self.hints) >= self.num_total_hints

    def accept_hint(self, hint, hint_def):
        self.hints.append(hint)

    def get_hints(self):
        hints = self.hints[: self.num_total_hints]
        return hints[: self.fi_hints], hints[self.fi_hints :]


class SeparateHintAssignment(HintAssignment):
    """
    "Separate" hint assignment assigns `total_hints` to Fi and gossip stones as specified.
    """

    def __init__(self, dist):
        super().__init__(dist)
        self.fi_hints = []
        self.gossip_stone_hints = []

    def read_from_json(self, jsn):
        self.total_hints = jsn["total_hints"]
        self.default_assignment = jsn["default_assignment"]

    def is_done(self):
        return len(self.fi_hints) + len(self.gossip_stone_hints) >= self.total_hints

    def accept_hint(self, hint, hint_def):
        assignment = hint_def.get("assignment", self.default_assignment)
        if assignment == "fi":
            self.fi_hints.append(hint)
        elif assignment == "gossip_stone":
            self.gossip_stone_hints.append(hint)
        else:
            raise ValueError("invalid hint assignment " + assignment)

    def get_hints(self):
        return self.fi_hints, self.gossip_stone_hints


class InvalidHintDistribution(Exception):
    pass


class HintDistribution:
    def __init__(self):
        self.hints_per_stone = 0
        self.banned_stones = []
        self.added_locations = []
        self.removed_locations = []
        self.added_items = []
        self.removed_items = []
        self.dungeon_sots_limit = 0
        self.sots_dungeon_placed = 0
        self.dungeon_barren_limit = 0
        self.distribution = {}
        self.goal_index = 0
        self.barren_overworld_zones = []
        self.placed_ow_barren = 0
        self.barren_dungeons = []
        self.placed_dungeon_barren = 0
        self.prev_barren_type = None
        self.barren_hinted_areas = set()
        self.counts_by_type = defaultdict(int)

        self.hintfuncs = {
            "always": self._create_always_hint,
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
        try:
            self._read_from_json(json.load(f))
        except Exception as e:
            print(e)
            raise InvalidHintDistribution(
                "Provided hint distribution was unable to be read"
            )

    def read_from_str(self, s):
        self._read_from_json(json.loads(s))

    def _read_from_json(self, jsn):
        if "fi_hints" in jsn and "hints_per_stone" in jsn:
            if "assignment" in jsn:
                raise ValueError("conflicting hint assignment modes")
            self.assignment = SplitHintAssignment(self)
            self.assignment.read_from_json(jsn)
        elif "assignment" in jsn:
            assignment_jsn = jsn["assignment"]
            mode = assignment_jsn["mode"]
            if mode == "split":
                self.assignment = SplitHintAssignment(self)
            elif mode == "separate":
                self.assignment = SeparateHintAssignment(self)
            else:
                raise ValueError("unknown hint assignment mode " + mode)
            self.assignment.read_from_json(assignment_jsn)
        else:
            raise ValueError("no hint assignment modes found")

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

    def start(
        self,
        useroutput: UserOutput,
        areas: Areas,
        options: Options,
        logic: LogicUtils,
        rng: Random,
        unhintable: List[EIN],
        check_hint_status: Dict[EIN, Literal[None, "sometimes", "always"]],
    ):
        self.useroutput = useroutput
        self.rng = rng
        self.logic = logic
        self.areas = areas
        self.options = options

        self.hinted_locations = unhintable

        self.banned_stones = list(map(areas.short_to_full, self.banned_stones))

        check_hint_status2 = (
            check_hint_status
            | {
                areas.short_to_full(loc["location"]): loc["type"]
                for loc in self.added_locations
            }
            | {areas.short_to_full(loc): None for loc in self.removed_locations}
        )
        # Combines those 3 dictionaries, the right-most dict has priority when keys are shared

        self.always_hints = [
            loc for loc, status in check_hint_status2.items() if status == "always"
        ]
        self.sometimes_hints = [
            loc for loc, status in check_hint_status2.items() if status == "sometimes"
        ]
        self.rng.shuffle(self.always_hints)
        self.rng.shuffle(self.sometimes_hints)

        # creates a list of boss keys for required dungeons
        self.required_boss_keys = [
            boss_key
            for dungeon in self.logic.required_dungeons
            for boss_key in BOSS_KEYS[dungeon]
        ]
        self.rng.shuffle(self.required_boss_keys)

        # populate our internal list copies for later manipulation
        self.sots_locations = list(self.logic.get_sots_locations())
        self.rng.shuffle(self.sots_locations)

        self.goals = [
            DUNGEON_GOALS[dungeon] for dungeon in self.logic.required_dungeons
        ]
        # shuffle the goal names that will be chosen in sequence when goal hints are placed to try to ensure one is placed for each goal
        self.rng.shuffle(self.goals)
        # create corresponding list of shuffled goal items

        self.goal_locations = []
        for goal in self.goals:
            check = areas.short_to_full(GOAL_CHECKS[goal])
            goal_locations = list(self.logic.get_sots_locations(EXTENDED_ITEM[check]))
            self.rng.shuffle(goal_locations)
            self.goal_locations.append(goal_locations)

        self.hintable_items = list(HINTABLE_ITEMS)
        self.removed_sots_items = []
        for item in self.added_items:
            self.hintable_items.extend([item["name"]] * item["amount"])
        if SEA_CHART in self.logic.get_useful_items():
            self.hintable_items.append(SEA_CHART)
        for item in self.removed_items:
            if item["type"] == "sots":
                self.removed_sots_items.append(item["name"])
            if (item["name"] in self.hintable_items) and (item["type"] == "item"):
                self.hintable_items.remove(item["name"])
        self.rng.shuffle(self.hintable_items)

        region_barren, nonprogress = self.logic.get_barren_regions()
        for zone in region_barren:
            if all(
                loc in self.hinted_locations or loc in self.always_hints
                for loc in self.logic.locations_by_hint_region(zone)
            ):
                continue

            if zone in ALL_DUNGEONS:
                self.barren_dungeons.append(zone)
            else:
                self.barren_overworld_zones.append(zone)

        self.junk_hints = JUNK_TEXT.copy()
        self.rng.shuffle(self.junk_hints)

        # for each fixed goal hint, place one for each required dungeon
        if "goal" in self.distribution.keys():
            self.distribution["goal"]["fixed"] *= len(self.logic.required_dungeons)
        # all always hints are always hinted
        self.distribution["always"]["fixed"] = len(self.always_hints)

        needed_fixed = []
        for hint_type in self.distribution.keys():
            if self.distribution[hint_type]["fixed"] > 0:
                needed_fixed.append(hint_type)
        needed_fixed.sort(key=lambda hint_type: self.distribution[hint_type]["order"])

        for hint_type in needed_fixed:
            curr_type = self.distribution[hint_type]
            func = self.hintfuncs[hint_type]
            for _ in range(curr_type["fixed"]):
                if (loc := func()) is not None:
                    self.counts_by_type[hint_type] += 1
                    for _ in range(curr_type["copies"]):
                        self.assignment.accept_hint(loc, curr_type)

        self.weighted_types = []
        self.weights = []
        for hint_type in self.distribution.keys():
            self.weighted_types.append(hint_type)
            self.weights.append(self.distribution[hint_type]["weight"])

    """
    Uses the distribution to calculate all the hints
    """

    def get_hints(self) -> Tuple[List[RegularHint], List[RegularHint]]:
        while not self.assignment.is_done():
            [hint_type] = self.rng.choices(self.weighted_types, self.weights)
            func = self.hintfuncs[hint_type]
            curr_type = self.distribution[hint_type]
            limit = curr_type.get("max")

            if limit is not None and self.counts_by_type[hint_type] >= limit:
                continue

            if (hint := func()) is not None:
                self.counts_by_type[hint_type] += 1
                for _ in range(curr_type["copies"]):
                    self.assignment.accept_hint(hint, curr_type)
            else:
                self.weights[self.weighted_types.index(hint_type)] = 0
                if not sum(self.weights):
                    raise self.useroutput.GenerationFailed(
                        f"Could not generate enough hints. This may be because the settings are too restrictive. Try changing the hint distribution."
                    )

        fi_hints, hintstone_hints = self.assignment.get_hints()
        assert len(fi_hints) <= MAX_FI_HINTS

        unbanned_hintstones = list(
            stone
            for stone in self.areas.gossip_stones
            if not stone in self.banned_stones
        )
        num_unbanned_hintstones = len(unbanned_hintstones)

        # evenly assign all hintstone hints to the unbanned hintstones
        # first, assign the same number of hints to our stones
        floor_hints_per_stone = len(hintstone_hints) // num_unbanned_hintstones
        self.hints_per_stone = {
            stone: 0 if stone in self.banned_stones else floor_hints_per_stone
            for stone in self.areas.gossip_stones
        }

        # then, randomly spread the remainder across our stones
        residual = len(hintstone_hints) - (
            floor_hints_per_stone * num_unbanned_hintstones
        )
        plus_one_stones = self.rng.sample(unbanned_hintstones, residual)
        for stone in plus_one_stones:
            self.hints_per_stone[stone] += 1

        assert max(self.hints_per_stone.values()) < MAX_HINTS_PER_STONE

        return fi_hints, hintstone_hints

    def _create_always_hint(self):
        if not self.always_hints:
            return None

        loc = self.always_hints.pop()
        item = self.logic.placement.locations[loc]
        if not self.options["cryptic-location-hints"]:
            text = None
        else:
            text = self.areas.checks[loc].get("text")

        if loc in self.hinted_locations:
            return self._create_always_hint()
        self.hinted_locations.append(loc)

        silent_realm_checks_rev = SILENT_REALM_CHECKS_REV(self.areas.short_to_full)
        trial_rando = self.options["randomize-trials"]

        if trial_rando and loc in silent_realm_checks_rev:
            trial = silent_realm_checks_rev[loc]
            trial_gate = {
                v: k for k, v in self.logic.randomized_trial_entrance.items()
            }[trial]
            return TrialGateHint(loc, item, trial_gate)
        else:
            return LocationHint("always", loc, item, text)

    def _create_sometimes_hint(self):
        if not self.sometimes_hints:
            return None

        loc = self.sometimes_hints.pop()
        item = self.logic.placement.locations[loc]
        if not self.options["cryptic-location-hints"]:
            text = None
        else:
            text = self.areas.checks[loc].get("text")

        if loc in self.hinted_locations:
            return self._create_sometimes_hint()
        self.hinted_locations.append(loc)

        return LocationHint("sometimes", loc, item, text)

    def _create_bk_hint(self):
        if not self.required_boss_keys:
            return None

        item = self.required_boss_keys.pop()
        loc = self.logic.placement.items[item]
        if not self.options["cryptic-location-hints"]:
            text = None
        else:
            text = self.areas.checks[loc].get("text")

        if loc in self.hinted_locations:
            return self._create_bk_hint()
        self.hinted_locations.append(loc)

        return LocationHint("boss_key", loc, item, text)

    def _create_item_hint(self):
        if not self.hintable_items:
            return None

        item = self.hintable_items.pop()
        loc = self.logic.placement.items[item]

        if loc in self.hinted_locations:
            return self._create_item_hint()
        self.hinted_locations.append(loc)

        if self.options["precise-item"]:
            text = self.areas.checks[loc].get("text")
            return LocationHint("precise_item", loc, item, text)

        if (zone_override := self.areas.checks[loc].get("cube_region")) is None:
            zone_override = self.areas.checks[loc]["hint_region"]

        return ZoneItemHint(loc, item, zone_override)

    def _create_random_hint(self):
        all_locations_without_hint = [
            loc
            for loc in self.logic.placement.locations
            if loc not in self.hinted_locations
            and self.areas.checks[loc]["hint_region"] not in self.barren_hinted_areas
            and EXTENDED_ITEM[loc] in self.logic.fill_restricted()
        ]

        assert all_locations_without_hint

        loc = self.rng.choice(all_locations_without_hint)
        item = self.logic.placement.locations[loc]
        if not self.options["cryptic-location-hints"]:
            text = None
        else:
            text = self.areas.checks[loc].get("text")
        self.hinted_locations.append(loc)

        return LocationHint("random", loc, item, text)

    def _create_sots_goal_hint(self, goal_mode=False):
        if goal_mode:
            locs = self.goal_locations[self.goal_index]
        else:
            locs = self.sots_locations

        if not locs:
            if not goal_mode:
                return None

            # if there aren't applicable locations for any goal, return None
            if not any(self.goal_locations):
                return None
            # go to next goal if no locations are left for this goal
            self.goal_index += 1
            self.goal_index %= len(self.goals)
            return self._create_sots_goal_hint(goal_mode)

        zone, loc, item = locs.pop()

        if item in self.removed_sots_items:
            return self._create_sots_goal_hint(goal_mode)

        if loc in self.hinted_locations:
            return self._create_sots_goal_hint(goal_mode)

        if self.sots_dungeon_placed >= self.dungeon_sots_limit and zone in ALL_DUNGEONS:
            return self._create_sots_goal_hint(goal_mode)

        if zone in ALL_DUNGEONS:
            # goal hints will use the same dungeon limits as sots hints
            self.sots_dungeon_placed += 1

        self.hinted_locations.append(loc)

        if goal_mode:
            # move to next goal boss for next goal hint
            goal = self.goals[self.goal_index]
            self.goal_index += 1
            self.goal_index %= len(self.goals)
        else:
            goal = None

        if (zone := self.areas.checks[loc].get("cube_region")) is not None:
            # place cube sots hint & catch specific zones and fit them into their general zone (as seen in the cube progress options)
            if self.options["cube-sots"]:
                if zone == SV:
                    zone = FARON_WOODS
                elif zone == MOGMA_TURF:
                    zone = ELDIN_VOLCANO
                elif zone == LANAYRU_MINE:
                    zone = LANAYRU_DESERT
                elif zone == LANAYRU_GORGE:
                    zone = LANAYRU_SAND_SEA
                return CubeSotsGoalHint(loc, item, zone, goal)
        else:
            zone = self.areas.checks[loc]["hint_region"]
        return SotsGoalHint(loc, item, zone, goal)

    def _create_sots_hint(self):
        return self._create_sots_goal_hint(goal_mode=False)

    def _create_goal_hint(self):
        return self._create_sots_goal_hint(goal_mode=True)

    def _create_barren_hint(self):
        # weights = (dungeon_weight, overworld_weight)
        if self.prev_barren_type is None:
            # 50/50 between dungeon and overworld on the first hint
            weights = (0.5, 0.5)
        elif self.prev_barren_type == "dungeon":
            weights = (0.25, 0.75)
        elif self.prev_barren_type == "overworld":
            weights = (0.75, 0.25)
        else:
            assert False

        barren_type = self.rng.choices(["dungeon", "overworld"], weights)[0]

        # Check against caps
        if self.placed_dungeon_barren > self.dungeon_barren_limit:
            barren_type = "overworld"

        # Failsafes if there are not enough barren hints to fill out the generated hint
        for barren_area_list in (self.barren_dungeons, self.barren_overworld_zones):
            for region in barren_area_list:
                if not len(self.logic.locations_by_hint_region(region)):
                    barren_area_list.remove(region)

        if len(self.barren_dungeons) == 0:
            if len(self.barren_overworld_zones) == 0:
                return None
            barren_type = "overworld"
        if len(self.barren_overworld_zones) == 0:
            barren_type = "dungeon"

        # generate a hint and remove it from the lists
        if barren_type == "dungeon":
            barren_area_list = self.barren_dungeons
        else:
            barren_area_list = self.barren_overworld_zones

        weights = [
            len(self.logic.locations_by_hint_region(area)) for area in barren_area_list
        ]

        area = self.rng.choices(barren_area_list, weights)[0]
        barren_area_list.remove(area)
        self.hinted_locations.extend(self.logic.locations_by_hint_region(area))
        self.barren_hinted_areas.add(area)
        self.prev_barren_type = barren_type

        return BarrenHint(area)

    def _create_junk_hint(self):
        return EmptyHint(self.rng.choice(self.junk_hints))

    def get_junk_text(self):
        return self.junk_hints.pop()
