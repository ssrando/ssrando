from hints.hint_distribution import HintDistribution
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


class GossipStoneHint:
    def to_gossip_stone_text(self) -> List[str]:
        """each string in the list appear in a separate textbox and will be line broken"""
        raise NotImplementedError("abstract")

    def to_spoiler_log_text(self) -> str:
        raise NotImplementedError("abstract")


@dataclass
class GossipStoneHintWrapper(GossipStoneHint):
    primary_hint: GossipStoneHint
    secondary_hint: GossipStoneHint

    def to_gossip_stone_text(self) -> List[str]:
        primary_text = self.primary_hint.to_gossip_stone_text()
        secondary_text = self.secondary_hint.to_gossip_stone_text()
        return [*primary_text, *secondary_text]

    def to_spoiler_log_text(self) -> str:
        return f"{self.primary_hint.to_spoiler_log_text()} / {self.secondary_hint.to_spoiler_log_text()}"


@dataclass
class TrialGateGossipStoneHint(GossipStoneHint):
    trial_gate: str
    trial_item: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"They say that opening the <r<{self.trial_gate}>> will reveal <y<{self.trial_item}>>"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.trial_gate} has {self.trial_item}"


@dataclass
class LocationGossipStoneHint(GossipStoneHint):
    location_string: str
    item: str

    def to_gossip_stone_text(self) -> List[str]:
        return [f"They say that {self.location_string} <y<{self.item}>>"]

    def to_spoiler_log_text(self) -> str:
        return f"They say that {self.location_string} <y<{self.item}>>"


@dataclass
class ItemGossipStoneHint(GossipStoneHint):
    location_name: str
    item: str

    def to_gossip_stone_text(self) -> List[str]:
        zone, specific_loc = Logic.split_location_name_by_zone(self.location_name)
        return [f"<y<{self.item}>> can be found at <r<{zone}: {specific_loc}>>"]

    def to_spoiler_log_text(self) -> str:
        return f"{self.item} is on {self.location_name}"


@dataclass
class WayOfTheHeroGossipStoneHint(GossipStoneHint):
    zone: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"The <b+<Spirit of the Sword>> guides the goddess' chosen hero to <r<{self.zone}>>"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is SotS"


@dataclass
class BarrenGossipStoneHint(GossipStoneHint):
    zone: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"They say that those who travel to <r<{self.zone}>> will never find anything for their quest"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is barren"


@dataclass
class EmptyGossipStoneHint(GossipStoneHint):
    text: str

    def to_gossip_stone_text(self) -> List[str]:
        return [self.text]

    def to_spoiler_log_text(self) -> str:
        return self.text


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
        with open(RANDO_ROOT_PATH / "hint_locations.yaml") as f:
            hints = yaml.safe_load(f)
            self.always_locations = hints["always"]
            self.sometimes_locations = hints["sometimes"]
            self.hint_defs = {**self.always_locations, **self.sometimes_locations}
        with open(RANDO_ROOT_PATH / f"hints/distributions/standard.json") as f:
            self.dist = HintDistribution()
            self.dist.read_from_file(f)

    def do_junk_hints(self):
        for hintname in self.stonehint_definitions.keys():
            self.hints[hintname] = EmptyGossipStoneHint(text="Useless hint")

    def do_normal_hints(self):
        total_stonehints = len(self.stonehint_definitions) * 2
        needed_always_hints = self.logic.filter_locations_for_progression(
            self.always_locations.keys()
        )
        # in shopsanity, we need to hint some beetle shop items
        # add them manually, cause they need to be kinda weirdly implemented because of bug net
        if (
            self.logic.rando.options["shop-mode"] != "Randomized"
            and "expensive" in self.logic.rando.options["banned-types"]
        ):
            needed_always_hints.remove("Beedle - 1200 Rupee Item")
            needed_always_hints.remove("Beedle - 1600 Rupee Item")
        if self.logic.rando.options["song-hints"] != "None":
            needed_always_hints.remove("Skyloft Silent Realm - Stone of Trials")
            needed_always_hints.remove("Faron Silent Realm - Water Scale")
            needed_always_hints.remove("Lanayru Silent Realm - Clawshots")
            needed_always_hints.remove("Eldin Silent Realm - Fireshield Earrings")
        needed_sometimes_hints = self.logic.filter_locations_for_progression(
            self.sometimes_locations
        )

        self.dist.start(self.logic, needed_always_hints, needed_sometimes_hints)

        hintable_items = HINTABLE_ITEMS.copy()
        # tweak item pool
        if "Sandship" in self.logic.required_dungeons:
            hintable_items.append("Sea Chart")

        hints_left = total_stonehints
        hinted_locations = self.logic.sworded_dungeon_locations
        print(f"placing {hints_left} total hints")

        # create location hints
        location_hints_left = self.logic.rando.options["location-hints"]
        location_hints = []
        for location in needed_always_hints:
            if location_hints_left <= 0:
                break
            if location not in hinted_locations:
                location_hints.append(location)
                hinted_locations.append(location)
                hints_left -= 1
                location_hints_left -= 1
        for location in self.logic.rando.rng.sample(
            needed_sometimes_hints,
            k=min(location_hints_left, len(needed_sometimes_hints)),
        ):
            if location not in hinted_locations:
                location_hints.append(location)
                hinted_locations.append(location)
                hints_left -= 1
                location_hints_left -= 1

        # create sots hints
        sots_hints_count = self.logic.rando.options["sots-hints"]
        sots_hints = []
        if (
            sots_hints_count > 0
        ):  # avoid doing the additional sots calculations if it isn't necessary
            sots_locations = {}
            for sotsloc, item in self.logic.rando.sots_locations.items():
                if self.logic.rando.options["small-key-mode"] not in [
                    "Anywhere",
                    "Lanayru Caves Key Only",
                ]:
                    # don't hint small keys unless keysanity is on
                    if item.endswith("Small Key"):
                        continue
                elif (
                    self.logic.rando.options["small-key-mode"]
                    == "Lanayru Caves Key Only"
                ):
                    if item.endswith("Small Key") and item != "LanayruCaves Small Key":
                        continue

                if self.logic.rando.options["boss-key-mode"] not in ["Anywhere"]:
                    # don't hint boss keys unless keysanity is on
                    if item.endswith("Boss Key"):
                        continue

                zone, specific_loc = Logic.split_location_name_by_zone(sotsloc)
                if (
                    zone not in sots_locations.keys()
                ):  # we only need each zone to appear once
                    sots_locations[zone] = [sotsloc]
                else:
                    sots_locations[zone].append(sotsloc)
            sots_zones = []
            for zone, locations in sots_locations.items():
                sots_zones.append(zone)
            if (
                len(sots_zones) < sots_hints_count
            ):  # there are not enough sots zones to fill the number of hints
                sots_hints_count = len(
                    sots_locations
                )  # so to prevent odd behavior we cap it at the number of zones
                # this also means that the missing hint slots will be filled by random hints
            self.logic.rando.rng.shuffle(sots_zones)
            for i in range(sots_hints_count):
                loc = self.logic.rando.rng.choice(sots_locations[sots_zones[i]])
                if loc not in hinted_locations:
                    sots_hints.append(loc)
                    hinted_locations.append(loc)
                    hints_left -= 1

        # create barren hints
        barren_hints_count = self.logic.rando.options["barren-hints"]
        barren_hints = []
        prev_barren_type = None
        if barren_hints_count > 0:
            region_barren, nonprogress = self.logic.get_barren_regions()
            barren_overworld_zones = []
            barren_dungeons = []
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
                if region_barren[zone]:
                    if zone in ALL_DUNGEON_AREAS:
                        barren_dungeons.append(zone)
                    else:
                        barren_overworld_zones.append(zone)

            if len(barren_overworld_zones) + len(barren_dungeons) < barren_hints_count:
                barren_hints_count = len(barren_overworld_zones) + len(barren_dungeons)
            for i in range(barren_hints_count):
                if len(barren_overworld_zones) <= 0:
                    prev_barren_type = "dungeon"
                elif len(barren_dungeons) <= 0:
                    prev_barren_type = "overworld"
                else:
                    if prev_barren_type is None:
                        # 50/50 between dungeon and overworld on the first hint
                        prev_barren_type = self.logic.rando.rng.choices(
                            ["dungeon", "overworld"], [0.5, 0.5]
                        )[0]
                    elif prev_barren_type == "dungeon":
                        prev_barren_type = self.logic.rando.rng.choices(
                            ["dungeon", "overworld"], [0.25, 0.75]
                        )[0]
                    elif prev_barren_type == "overworld":
                        prev_barren_type = self.logic.rando.rng.choices(
                            ["dungeon", "overworld"], [0.75, 0.25]
                        )[0]
                if prev_barren_type == "dungeon":
                    areas = barren_dungeons
                else:
                    areas = barren_overworld_zones
                if not areas:
                    # something went wrong generating this hint, there are likely no more barren hints able to be placed
                    break

                area_weights = [
                    len(self.logic.locations_by_zone_name(area))
                    for area in areas
                    if area not in barren_hints
                ]

                barren_hints.append(
                    self.logic.rando.rng.choices(barren_overworld_zones, area_weights)
                )
                hints_left -= 1

        # create  the item hints
        item_hints = []
        self.logic.rando.rng.shuffle(hintable_items)
        hinted_locations.extend(self.logic.sworded_dungeon_locations)
        for i in range(self.logic.rando.options["item-hints"]):
            hinted_item = hintable_items.pop()
            for location, item in self.logic.done_item_locations.items():
                if (
                    item == hinted_item
                    and location not in item_hints
                    and location not in hinted_locations
                ):
                    item_hints.append(location)
                    hinted_locations.append(location)
                    hints_left -= 1
                    break

        all_locations_without_hint = self.logic.filter_locations_for_progression(
            (
                loc
                for loc in self.logic.done_item_locations
                if not loc in hinted_locations
                and not loc in self.logic.prerandomization_item_locations
            )
        )
        while hints_left > 0 and all_locations_without_hint:
            # add completely random locations if there are otherwise empty stones
            location_to_hint = self.logic.rando.rng.choice(all_locations_without_hint)
            all_locations_without_hint.remove(location_to_hint)
            # location_hints.append(location_to_hint)
            hints_left -= 1
        self._place_hints_for_locations(
            location_hints, item_hints, sots_hints, barren_hints
        )

    def do_bingo_hints(self):
        total_stonehints = len(self.stonehint_definitions) * 2
        needed_always_hints = self.logic.filter_locations_for_progression(
            ALWAYS_REQUIRED_LOCATIONS
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
            SOMETIMES_LOCATIONS
        )
        hints_left = total_stonehints
        hinted_locations = self.logic.sworded_dungeon_locations

        # create location hints
        location_hints = []
        for location in needed_always_hints:
            if location not in hinted_locations:
                location_hints.append(location)
                hinted_locations.append(location)
                hints_left -= 1
        important_items = [
            "Progressive Sword",
            "Goddess Harp",
            "Clawshots",
            "Water Scale",
            "Fireshield Earrings",
            "Sea Chart",
            "Clawshots",
            "Goddess Harp",
            ["Gratitude Crystal Pack"] * 3,
            ["Progressive Beetle"] * 2,
            ["Gold Rupee"] * 2,
            ["Silver Rupee"] * 2,
            ["Progressive Sword"] * 2,
            "Whip",
            "Gust Bellows",
            "Bomb Bag",
            "Heart Medal",
            "Life Medal",
            "Progressive Pouch",
        ]
        if self.logic.rando.options["shop-mode"] == "Randomized":
            important_items.append("Bug Net")
            # create  the item hints
        item_hints = []
        self.logic.rando.rng.shuffle(important_items)
        for i in range(15):
            hinted_item = important_items.pop()
            for location, item in self.logic.done_item_locations.items():
                if (
                    item == hinted_item
                    and location not in item_hints
                    and location not in hinted_locations
                ):
                    item_hints.append(location)
                    hinted_locations.append(location)
                    hints_left -= 1
                    break
        location_hints_left = hints_left
        for location in self.logic.rando.rng.sample(
            needed_sometimes_hints,
            k=min(location_hints_left, len(needed_sometimes_hints)),
        ):
            if location not in hinted_locations:
                location_hints.append(location)
                hinted_locations.append(location)
                hints_left -= 1
                location_hints_left -= 1

        self._place_hints_for_locations(location_hints, item_hints, [], [])

    def _place_hints_for_locations(
        self, location_hints, item_hints, sots_hints, barren_hints
    ):
        hint_locations = location_hints + item_hints + sots_hints
        # make sure hint locations aren't locked by the item they hint
        hint_banned_stones = defaultdict(set)
        for hint_location in hint_locations:
            if hint_location in SILENT_REALM_CHECKS.keys():
                loc_trial_gate = SILENT_REALM_CHECKS[hint_location]
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
                            hint_banned_stones[gossipstone_name].add(hint_location)
            else:
                hinted_item = self.logic.done_item_locations[hint_location]
                if hinted_item in self.logic.all_progress_items:
                    for (
                        gossipstone_name,
                        gossipstone_def,
                    ) in self.stonehint_definitions.items():
                        if not self.logic.can_reach_restricted(
                            [hint_location], gossipstone_def["Need"]
                        ):
                            hint_banned_stones[gossipstone_name].add(hint_location)

        stones_to_banned_locs_sorted = sorted(
            hint_banned_stones.items(), key=lambda x: len(x[1]), reverse=True
        )

        if len(hint_locations) < len(self.stonehint_definitions) * 2:
            hint_locations.extend(
                [None] * (len(self.stonehint_definitions) * 2 - len(hint_locations))
            )
        unhinted_locations = hint_locations.copy()

        hint_to_location = {}
        # place locations that are restricted in locations
        for gossipstone_name, banned_locations in stones_to_banned_locs_sorted:
            valid_locations = [
                loc for loc in unhinted_locations if not loc in banned_locations
            ]
            if len(valid_locations) == 0:
                print(
                    f"no valid location for {gossipstone_name} in seed {self.logic.rando.seed}"
                )
                loc_to_hint = unhinted_locations[0]
                second_loc_to_hint = unhinted_locations[1]
                # raise Exception('no valid location to place hint!')
            else:
                loc_to_hint = self.logic.rando.rng.choice(valid_locations)
                # ensure we dont try to place the same hint twice
                removed_list = valid_locations.copy()
                removed_list.remove(loc_to_hint)
                second_loc_to_hint = self.logic.rando.rng.choice(removed_list)
            hint_to_location[gossipstone_name] = [loc_to_hint, second_loc_to_hint]
            unhinted_locations.remove(loc_to_hint)
            unhinted_locations.remove(second_loc_to_hint)
        # place locations that aren't restricted and also fill rest of locations
        for gossipstone_name in [
            name for name in self.stonehint_definitions if not name in hint_to_location
        ]:
            if len(unhinted_locations) == 0:
                # placeholder
                hint_to_location[gossipstone_name] = [None]
                continue
            loc_to_hint = self.logic.rando.rng.choice(unhinted_locations)
            unhinted_locations.remove(loc_to_hint)
            second_loc_to_hint = self.logic.rando.rng.choice(unhinted_locations)
            unhinted_locations.remove(second_loc_to_hint)
            hint_to_location[gossipstone_name] = [loc_to_hint, second_loc_to_hint]
        anywhere_hints = barren_hints + []
        self.logic.rando.rng.shuffle(anywhere_hints)

        def create_hint(location):
            if location in location_hints:
                if location in SILENT_REALM_CHECKS.keys():
                    loc_trial_gate = SILENT_REALM_CHECKS[location]
                    trial_gate_dest = self.logic.trial_connections[loc_trial_gate]
                    trial_gate_dest_loc = [
                        trial
                        for trial in SILENT_REALM_CHECKS.keys()
                        if trial_gate_dest in trial
                    ].pop()
                    trial_item = self.logic.done_item_locations[trial_gate_dest_loc]
                    return TrialGateGossipStoneHint(
                        trial_gate=loc_trial_gate,
                        trial_item=trial_item,
                    )
                else:
                    return LocationGossipStoneHint(
                        location_string=self.hint_defs[location],
                        item=self.logic.done_item_locations[location],
                    )
            elif location in item_hints:
                if location in SILENT_REALM_CHECKS.keys():
                    loc_trial_gate = SILENT_REALM_CHECKS[location]
                    trial_gate_dest = self.logic.trial_connections[loc_trial_gate]
                    trial_gate_dest_loc = [
                        trial
                        for trial in SILENT_REALM_CHECKS.keys()
                        if trial_gate_dest in trial
                    ].pop()
                    trial_item = self.logic.done_item_locations[trial_gate_dest_loc]
                    return TrialGateGossipStoneHint(
                        trial_gate=loc_trial_gate,
                        trial_item=trial_item,
                    )
                else:
                    return ItemGossipStoneHint(
                        location_name=location,
                        item=self.logic.done_item_locations[location],
                    )
            elif location in sots_hints:
                zone, specific_loc = Logic.split_location_name_by_zone(location)
                return WayOfTheHeroGossipStoneHint(zone=zone)
            elif location is None:
                return EmptyGossipStoneHint(text="--PLACEHOLDER--")
            else:
                raise Exception(f"Unable to identify hint type for location {location}")

        for gossipstone_name in self.stonehint_definitions:
            locs_to_hint = hint_to_location[gossipstone_name]
            # print(locs_to_hint)
            loc_to_hint = locs_to_hint[0]
            second_loc_to_hint = locs_to_hint[1]
            if second_loc_to_hint is None and loc_to_hint is not None:
                if len(anywhere_hints) > 0:
                    self.hints[gossipstone_name] = GossipStoneHintWrapper(
                        create_hint(loc_to_hint),
                        BarrenGossipStoneHint(zone=anywhere_hints.pop()),
                    )
                else:
                    self.hints[gossipstone_name] = create_hint(loc_to_hint)
            elif second_loc_to_hint is not None and loc_to_hint is None:
                if len(anywhere_hints) > 0:
                    self.hints[gossipstone_name] = GossipStoneHintWrapper(
                        BarrenGossipStoneHint(zone=anywhere_hints.pop()),
                        create_hint(second_loc_to_hint),
                    )
                else:
                    self.hints[gossipstone_name] = create_hint(second_loc_to_hint)
            elif loc_to_hint is None:
                # place barren hints at locations with no hints
                if len(anywhere_hints) < 0:
                    hint = anywhere_hints.pop()
                else:
                    hint = None
                if hint in barren_hints:
                    self.hints[gossipstone_name] = BarrenGossipStoneHint(zone=hint)
                else:
                    self.hints[gossipstone_name] = EmptyGossipStoneHint(
                        text="--PLACEHOLDER--"
                    )
            else:
                self.hints[gossipstone_name] = GossipStoneHintWrapper(
                    create_hint(loc_to_hint), create_hint(second_loc_to_hint)
                )
