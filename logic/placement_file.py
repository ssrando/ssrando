from options import Options
from version import VERSION
from logic.item_types import ALL_ITEM_NAMES
from logic.constants import *
from util.file_accessor import read_yaml_file_cached, get_entrance_table

import json


class InvalidPlacementFile(Exception):
    pass


class PlacementFile:
    def __init__(self):
        self.version = ""
        self.options = Options()
        self.hash_str = ""
        self.starting_items = []
        self.required_dungeons = []
        self.item_locations = {}
        self.chest_dowsing = {}
        self.gossip_stone_hints = {}
        self.trial_hints = {}
        self.dungeon_connections = {}
        self.trial_connections = {}
        self.trial_object_seed = -1
        self.music_rando_seed = -1
        self.exits_connections = {}

    def read_from_file(self, f):
        self._read_from_json(json.load(f))

    def read_from_str(self, s):
        self._read_from_json(json.loads(s))

    def to_json_str(self):
        retval = {
            "version": self.version,
            "permalink": self.options.get_permalink(exclude_seed=True),
            "hash": self.hash_str,
            "starting-items": self.starting_items,
            "required-dungeons": self.required_dungeons,
            "item-locations": self.item_locations,
            "chest-dowsing": self.chest_dowsing,
            "gossip-stone-hints": self.gossip_stone_hints,
            "trial-hints": self.trial_hints,
            "entrance-connections": self.dungeon_connections,
            "trial-connections": self.trial_connections,
            "trial-object-seed": self.trial_object_seed,
            "music-rando-seed": self.music_rando_seed,
            "exits-connections": self.exits_connections,
        }
        return json.dumps(retval, indent=2)

    def _read_from_json(self, jsn):
        self.version = jsn["version"]
        self.options.update_from_permalink(jsn["permalink"])
        self.options.set_option("seed", -1)
        self.hash_str = jsn["hash"]
        self.starting_items = jsn["starting-items"]
        self.required_dungeons = jsn["required-dungeons"]
        self.item_locations = jsn["item-locations"]
        self.chest_dowsing = jsn["chest-dowsing"]
        self.gossip_stone_hints = jsn["gossip-stone-hints"]
        self.trial_hints = jsn["trial-hints"]
        self.dungeon_connections = jsn["entrance-connections"]
        self.trial_connections = jsn["trial-connections"]
        self.trial_object_seed = jsn["trial-object-seed"]
        self.music_rando_seed = jsn["music-rando-seed"]
        self.exits_connections = jsn["exits-connections"]

    def check_valid(self):
        """checks, if the current state is valid, throws an exception otherwise
        This does not check consistency with all the settings"""
        if VERSION != self.version:
            raise InvalidPlacementFile(
                f"Version did not match, requires {self.version} but found {VERSION}"
            )

        ALLOWED_STARTING_ITEMS = {
            "Emerald Tablet": 1,
            "Amber Tablet": 1,
            "Ruby Tablet": 1,
            "Progressive Sword": 6,
            "Progressive Pouch": 1,
        }

        if any(item not in ALLOWED_STARTING_ITEMS for item in self.starting_items):
            raise InvalidPlacementFile("invalid starting item!")
        for start_item, count in ALLOWED_STARTING_ITEMS.items():
            if self.starting_items.count(start_item) > count:
                raise InvalidPlacementFile(f"{start_item} too often in starting items!")

        for req_dungeon in self.required_dungeons:
            if req_dungeon not in POTENTIALLY_REQUIRED_DUNGEONS:
                raise InvalidPlacementFile(
                    f"{req_dungeon} is not a valid required dungeon!"
                )

        if sorted(self.dungeon_connections.keys()) != sorted(
            ENTRANCE_CONNECTIONS.keys()
        ):
            raise InvalidPlacementFile("dungeon entrance_connections are wrong!")

        if sorted(self.dungeon_connections.values()) != sorted(
            ENTRANCE_CONNECTIONS.values()
        ):
            raise InvalidPlacementFile("dungeon entries are wrong!")

        item_names = ALL_ITEM_NAMES.copy()
        item_names.remove("Gratitude Crystal")

        for item in self.item_locations.values():
            if item not in item_names:
                raise InvalidPlacementFile(f'invalid item "{item}"')

        checks_file = read_yaml_file_cached("checks.yaml")
        check_sets_equal(
            set(
                k
                for (k, v) in checks_file.items()
                if v["original item"] != "Gratitude Crystal"
            ),
            set(self.item_locations.keys()),
            "Checks",
        )

        hint_file = read_yaml_file_cached("hints.yaml")
        check_sets_equal(
            set(hint_file.keys()),
            set(self.gossip_stone_hints.keys()),
            "Gossip Stone Hints",
        )

        for hintlist in self.gossip_stone_hints.values():
            if not isinstance(hintlist, list):
                raise InvalidPlacementFile(
                    "gossip stone hints need to be LISTS of strings!"
                )
            for hint in hintlist:
                if not isinstance(hint, str):
                    raise InvalidPlacementFile(
                        "gossip stone hints need to be lists of STRINGS!"
                    )

        trial_check_names = set(
            (
                "Song of the Hero - Trial Hint",
                "Farore's Courage - Trial Hint",
                "Nayru's Wisdom - Trial Hint",
                "Din's Power - Trial Hint",
            )
        )

        check_sets_equal(trial_check_names, set(self.trial_hints.keys()), "Trial Hints")

        entrance_table = get_entrance_table()
        # all exits needs to be connected
        check_sets_equal(
            set(entrance_table.exits) | set(entrance_table.statue_exits),
            set(self.exits_connections.keys()),
            "exits",
        )
        # but not all entrances need to be connected by something,
        check_all_in_set(
            set(entrance_table.entrances),
            set(self.exits_connections.values()),
            "entrances",
        )


def check_sets_equal(orig: set, actual: set, name: str):
    if orig != actual:
        additional = actual - orig
        missing = orig - actual
        error_msg = ""
        if additional:
            error_msg += f"Additional {name}:\n"
            error_msg += ", ".join(additional) + "\n"
        if missing:
            error_msg += f"Missing {name}:\n"
            error_msg += ", ".join(missing) + "\n"
        raise InvalidPlacementFile(error_msg)


def check_all_in_set(orig: set, actual: set, name: str):
    additional = actual - orig
    if additional:
        error_msg = f"Additional {name}:\n"
        error_msg += ", ".join(additional) + "\n"
        raise InvalidPlacementFile(error_msg)
