from .logic import Logic
from paths import RANDO_ROOT_PATH
import yaml
from collections import OrderedDict

ALWAYS_REQUIRED_LOCATIONS = [
    'Thunderhead - Levias',
    'Skyloft Silent Realm - Stone of Trials',
    'Faron Silent Realm - Water Scale',
    'Lanayru Silent Realm - Clawshots',
    'Eldin Silent Realm - Fireshield Earrings',
    'Sky - Kina\'s Crystals',
]

SOMETIMES_LOCATIONS = [
    'Lanayru Sand Sea - Roller Coaster Minigame',
    'Skyloft - Pumpkin Archery - 600 Points',
    'Sky - Lumpy Pumpkin Harp Minigame',
    'Sky - Fun Fun Island Minigame',
    'Thunderhead - Bug Island minigame',
    'Skyloft - Batreaux 80 Crystals',
    'Skyloft - Batreaux 70 Crystals Second Reward',
    'Skyloft - Batreaux 70 Crystals',
    'Skyloft - Batreaux 50 Crystals',
    "Skyloft - Owlan's Crystals",
    "Skyloft - Sparrot's Crystals",
    "Skyloft - Peater/Peatrice's Crystals",
    "Lanayru - On Top of Lanayru Mining Facility",
]

class Hints:
    def __init__(self, logic: Logic):
        with (RANDO_ROOT_PATH / "hints.yaml").open() as f:
            self.stonehint_definitions: dict = yaml.safe_load(f)
        self.logic = logic
        self.hints = OrderedDict()
    
    def do_junk_hints(self):
        for hintname in self.stonehint_definitions.keys():
            self.hints[hintname] = 'Useless hint'
    
    def do_normal_hints(self):
        hint_locations = []
        total_stonehints = len(self.stonehint_definitions)
        needed_always_hints = self.logic.filter_locations_for_progression(ALWAYS_REQUIRED_LOCATIONS)
        needed_sometimes_hints = self.logic.filter_locations_for_progression(SOMETIMES_LOCATIONS)
        # needed_always_hints = [location for location in ALWAYS_REQUIRED_LOCATIONS if not location in self.logic.race_mode_banned_locations]
        # needed_sometimes_hints = [location for location in SOMETIMES_LOCATIONS if not location in self.logic.race_mode_banned_locations]
        hints_left = total_stonehints
        for location in needed_always_hints:
            hint_locations.append(location)
            hints_left -= 1
        for location in self.logic.rando.rng.sample(needed_sometimes_hints, k=min(hints_left, len(needed_sometimes_hints))):
            hint_locations.append(location)
            hints_left -= 1
        hints = [f'{location}\nhas\n{self.logic.done_item_locations[location]}.' for location in hint_locations]
        while len(hints) < total_stonehints:
            hints.append('--PLACEHOLDER--')
        self.logic.rando.rng.shuffle(hints)
        for i, hint_def in enumerate(self.stonehint_definitions):
            self.hints[hint_def] = hints[i]
