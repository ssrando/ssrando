from __future__ import annotations
from dataclasses import dataclass
import random  # Only for typing purposes
from typing import List


from .constants import *
from .logic import Logic
from .inventory import BANNED_BIT, EVERYTHING_UNBANNED_BIT, EXTENDED_ITEM
from .fill_algo_common import RandomizationSettings, UserOutput


class RandomFill:
    def __init__(
        self, logic: Logic, rng: random.Random, randosettings: RandomizationSettings
    ):

        self.logic = logic
        self.rng = rng
        self.randosettings = randosettings

    def randomize(self, useroutput: UserOutput):
        self.useroutput = useroutput

        must_be_placed_items = list(self.randosettings.must_be_placed_items)
        may_be_placed_items = list(self.randosettings.may_be_placed_items)

        self.rng.shuffle(must_be_placed_items)
        self.rng.shuffle(may_be_placed_items)

        self.useroutput.progress_callback("placing unique items...")
        for item in must_be_placed_items:
            assert self.place_item(item)
        self.useroutput.progress_callback("placing remaining items...")
        for item in may_be_placed_items:
            if not self.place_item(item, force=False):
                break
        self.fill_with_junk(self.randosettings.duplicable_items)

    def get_total_progress_steps(self):
        return 2

    def fill_with_junk(self, junk):
        empty_locations = [
            loc
            for loc in self.logic.check_list(EIN(""))
            if loc not in self.logic.placement.locations
        ]
        junk = list(junk)

        for location in empty_locations:
            result = self.logic.place_item(location, self.rng.choice(junk), fill=False)
            assert result

    def place_item(self, item: EXTENDED_ITEM_NAME, depth=0, force=True) -> bool:
        placement_limit: EIN = self.logic.placement.item_placement_limit.get(
            item, EIN("")
        )
        accessible_locations = self.logic.check_list(placement_limit)

        empty_locations = [
            loc
            for loc in accessible_locations
            if loc not in self.logic.placement.locations
        ]

        if empty_locations:
            location = self.rng.choice(empty_locations)
            result = self.logic.place_item(location, item, fill=force)
            assert result  # Undefined if False
            return True

        raise self.useroutput.GenerationFailed(
            f"no more location accessible for {item}"
        )
