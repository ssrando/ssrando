import json
from random import Random

import yaml

from hint_types import *
from paths import RANDO_ROOT_PATH


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
        self.dungeon_barren_limit = 0
        self.distribution = {}
        self.rng = None
        self.hints = []
        self.weighted_types = []
        self.weights = []
        self.ready = False

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

    def start(self, rng: Random, always_hints: list, sometimes_hints: list):
        self.rng = rng

        # load additional resources in
        with open(RANDO_ROOT_PATH / "hint_locations.yaml") as f:
            hints = yaml.safe_load(f)
            always_location_descriptors = hints["always"]
            sometimes_location_descriptors = hints["sometimes"]

        # all always hints are always hinted
        for hint in always_hints:
            self.hints.append(
                LocationGossipStoneHint(always_location_descriptors[hint], "?")
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
        for i in range(num_sometimes):
            self.hints.append(
                LocationGossipStoneHint(
                    sometimes_location_descriptors[sometimes_hints[i]], "?"
                )
            )

        # reverse the list of hints to we can pop off the back in O(1) in next_hint ()
        self.hints.reverse()

        for hint_type in self.distribution.keys():
            self.weighted_types.append(hint_type)
            self.weights.append(self.distribution[hint_type]["weight"])

    """
    Uses the distribution to calculate the next hint
    """

    def next_hint(self):
        if len(self.hints) > 0:
            return self.hints.pop()
        next_type = self.rng.choice(self.weighted_types, self.weights)
        if next_type == "sots":
            pass
        elif next_type == "barren":
            pass
        elif next_type == "item":
            pass
        else:
            # junk hint is the last and also a fallback
            pass
