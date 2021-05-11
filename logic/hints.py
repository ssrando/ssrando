from .logic import Logic
from paths import RANDO_ROOT_PATH
import yaml
from collections import OrderedDict, defaultdict
from dataclasses import dataclass

ALWAYS_REQUIRED_LOCATIONS = [
    'Thunderhead - Levias',
    'Skyloft Silent Realm - Stone of Trials',
    'Faron Silent Realm - Water Scale',
    'Lanayru Silent Realm - Clawshots',
    'Eldin Silent Realm - Fireshield Earrings',
    'Sky - Kina\'s Crystals',
    "Skyloft - Peater/Peatrice's Crystals",
    'Skyloft - Batreaux 80 Crystals',
]

SOMETIMES_LOCATIONS = [
    'Lanayru Sand Sea - Roller Coaster Minigame',
    'Skyloft - Pumpkin Archery - 600 Points',
    'Sky - Lumpy Pumpkin Harp Minigame',
    'Sky - Fun Fun Island Minigame',
    'Thunderhead - Bug Island minigame',
    'Skyloft - Batreaux 70 Crystals Second Reward',
    'Skyloft - Batreaux 70 Crystals',
    'Skyloft - Batreaux 50 Crystals',
    "Skyloft - Owlan's Crystals",
    "Skyloft - Sparrot's Crystals",
    "Lanayru - On Top of Lanayru Mining Facility",
    "Skyloft - Waterfall Goddess Chest", # stronghold cube
    "Sky - Beedle's Island Goddess Chest", # goddess cube in ToT area
]

HINTABLE_ITEMS = \
    ["Clawshots"] + \
   [ "Progressive Beetle"] * 2 + \
    ["Progressive Sword"] * 4 + \
    ["Emerald Tablet"] * 1 + \
    ["Ruby Tablet"] * 1 + \
    ["Amber Tablet"] * 1 + \
    ["Goddess Harp"] * 1 + \
    ["Water Scale"] * 1 + \
    ["Fireshield Earrings"] * 1


class GossipStoneHint:
    def to_gossip_stone_text(self) -> str:
        raise NotImplementedError("abstract")
    
    def to_spoiler_log_text(self) -> str:
        raise NotImplementedError("abstract")

@dataclass
class LocationGossipStoneHint(GossipStoneHint):
    location_name: str
    item: str

    def to_gossip_stone_text(self) -> str:
        zone, specific_loc = Logic.split_location_name_by_zone(self.location_name)
        return f"{zone}\n{specific_loc}\nhas {self.item}"
    
    def to_spoiler_log_text(self) -> str:
        return f"{self.location_name} has {self.item}"

@dataclass
class ItemGossipStoneHint(GossipStoneHint):
    location_name: str
    item: str

    def to_gossip_stone_text(self) -> str:
        zone, specific_loc = Logic.split_location_name_by_zone(self.location_name)
        return f"{self.item} can be found at\n{zone}\n{specific_loc}"

    def to_spoiler_log_text(self) -> str:
        return f"{self.item} is on {self.location_name}"


@dataclass
class EmptyGossipStoneHint(GossipStoneHint):
    text: str

    def to_gossip_stone_text(self) -> str:
        return self.text
    
    def to_spoiler_log_text(self) -> str:
        return self.text

class Hints:
    def __init__(self, logic: Logic):
        with (RANDO_ROOT_PATH / "hints.yaml").open() as f:
            self.stonehint_definitions: dict = yaml.safe_load(f)
        self.logic = logic
        for hintdef in self.stonehint_definitions.values():
            if self.logic.rando.options['logic-mode'] == 'No Logic':
                hintdef["Need"] = Logic.parse_logic_expression("Nothing")
            else:
                hintdef["Need"] = Logic.parse_logic_expression(hintdef["Need"])
        self.hints = OrderedDict()
    
    def do_junk_hints(self):
        for hintname in self.stonehint_definitions.keys():
            self.hints[hintname] = EmptyGossipStoneHint(text='Useless hint')
    
    def do_normal_hints(self):
        location_hints = []
        item_hints = []
        total_stonehints = len(self.stonehint_definitions)
        needed_always_hints = self.logic.filter_locations_for_progression(ALWAYS_REQUIRED_LOCATIONS)
        # in shopsanity, we need to hint some beetle shop items
        # add them manually, cause they need to be kinda weirdly implemented because of bug net
        if self.logic.rando.options['shop-mode'] == 'Randomized' and \
                'expensive' not in self.logic.rando.options['banned-types']:
            needed_always_hints.append('Skyloft - Beedle 1200 Rupee Item')
            needed_always_hints.append('Skyloft - Beedle 1600 Rupee Item')
        needed_sometimes_hints = self.logic.filter_locations_for_progression(SOMETIMES_LOCATIONS)
        hints_left = total_stonehints
        location_hints_left = self.logic.rando.options['location-hints']
        for location in needed_always_hints:
            if location_hints_left <= 0:
                break
            location_hints.append(location)
            hints_left -= 1
            location_hints_left -= 1
        while location_hints_left > 0:
            for location in self.logic.rando.rng.sample(needed_sometimes_hints,
                                                        k=min(hints_left, len(needed_sometimes_hints))):
                location_hints.append(location)
                hints_left -= 1
                location_hints_left -= 1
        hintable_items = HINTABLE_ITEMS.copy()
        self.logic.rando.rng.shuffle(hintable_items)
        for i in range(self.logic.rando.options['item-hints']):
            hinted_item = hintable_items.pop()
            for location, item in self.logic.done_item_locations.items():
                if item == hinted_item:
                    item_hints.append(location)
                    hints_left -= 1
                    break

        all_locations_without_hint = self.logic.filter_locations_for_progression((loc for loc in self.logic.done_item_locations if not loc in location_hints and not loc in self.logic.prerandomization_item_locations))
        while hints_left > 0 and all_locations_without_hint:
            # add completely random locations if there are otherwise empty stones
            location_to_hint = self.logic.rando.rng.choice(all_locations_without_hint)
            all_locations_without_hint.remove(location_to_hint)
            location_hints.append(location_to_hint)
            hints_left -= 1
        self._place_hints_for_locations(location_hints, item_hints)

    def do_bingo_hints(self):
        important_items = {"Progressive Sword", "Goddess Harp", "Clawshots", "Water Scale", "Fireshield Earrings"}
        if self.logic.rando.options['shop-mode'] == 'Randomized':
            important_items.add("Bug Net")
        hint_locations = []
        for location, item in self.logic.done_item_locations.items():
            if item in important_items:
                hint_locations.append(location)
        assert len(hint_locations) <= len(self.stonehint_definitions), f"need {len(hint_locations)} locations, but only {len(self.stonehint_definitions)} stones available"

        all_locations_without_hint = self.logic.filter_locations_for_progression((loc for loc in self.logic.done_item_locations if not loc in hint_locations and not loc in self.logic.prerandomization_item_locations))
        while len(hint_locations) < len(self.stonehint_definitions) and all_locations_without_hint:
            # add completely random locations if there are otherwise empty stones
            location_to_hint = self.logic.rando.rng.choice(all_locations_without_hint)
            all_locations_without_hint.remove(location_to_hint)
            hint_locations.append(location_to_hint)

        self._place_hints_for_locations(hint_locations, [])
        
    def _place_hints_for_locations(self, location_hints, item_hints):
        print(f"location hints: {len(location_hints)}")
        for location in location_hints:
            print(f"\t{location}")
        print(f"location hints: {len(item_hints)}")
        for location in item_hints:
            print(f"\t{location}")
        hint_locations = location_hints + item_hints
        print(hint_locations)
        print(len(hint_locations))
        # make sure hint locations aren't locked by the item they hint
        hint_banned_stones = defaultdict(set)
        for hint_location in hint_locations:
            hinted_item = self.logic.done_item_locations[hint_location]
            if hinted_item in self.logic.all_progress_items:
                for gossipstone_name, gossipstone_def in self.stonehint_definitions.items():
                    if not self.logic.can_reach_restricted([hint_location], gossipstone_def["Need"]):
                        hint_banned_stones[gossipstone_name].add(hint_location)
        stones_to_banned_locs_sorted = sorted(hint_banned_stones.items(), key=lambda x: len(x[1]), reverse=True)

        if len(hint_locations) < len(self.stonehint_definitions):
            hint_locations.extend([None]*(len(self.stonehint_definitions) - len(hint_locations)))
        unhinted_locations = hint_locations.copy()

        hint_to_location = {}
        # place locations that are restricted in locations
        for gossipstone_name, banned_locations in stones_to_banned_locs_sorted:
            valid_locations = [loc for loc in unhinted_locations if not loc in banned_locations]
            if len(valid_locations) == 0:
                print(f"no valid location for {gossipstone_name} in seed {self.logic.rando.seed}")
                loc_to_hint = unhinted_locations[0]
                # raise Exception('no valid location to place hint!')
            else:
                loc_to_hint = self.logic.rando.rng.choice(valid_locations)
            hint_to_location[gossipstone_name] = loc_to_hint
            unhinted_locations.remove(loc_to_hint)
        # place locations that aren't restricted and also fill rest of locations
        for gossipstone_name in [name for name in self.stonehint_definitions if not name in hint_to_location]:
            if len(unhinted_locations) == 0:
                # placeholder
                hint_to_location[gossipstone_name] = None
                continue
            loc_to_hint = self.logic.rando.rng.choice(unhinted_locations)
            unhinted_locations.remove(loc_to_hint)
            hint_to_location[gossipstone_name] = loc_to_hint
        for gossipstone_name in self.stonehint_definitions:
            loc_to_hint = hint_to_location[gossipstone_name]
            if loc_to_hint is None:
                self.hints[gossipstone_name] = EmptyGossipStoneHint(text='--PLACEHOLDER--')
            else:
                if loc_to_hint in location_hints:
                    self.hints[gossipstone_name] = LocationGossipStoneHint(
                            location_name=loc_to_hint,
                            item=self.logic.done_item_locations[loc_to_hint]
                    )
                elif loc_to_hint in item_hints:
                    self.hints[gossipstone_name] = ItemGossipStoneHint(
                        location_name=loc_to_hint,
                        item=self.logic.done_item_locations[loc_to_hint]
                    )
                else:
                    raise Exception(f"Unable to identify hint type for location {loc_to_hint}")
