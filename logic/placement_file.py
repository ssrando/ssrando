from .constants import *
from options import Options
from version import VERSION

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
        self.hints = {}
        self.trial_connections = {}
        self.map_connections = {}
        self.trial_object_seed = -1
        self.music_rando_seed = -1
        self.bk_angle_seed = -1

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
            "hints": self.hints,
            "map-connections": self.map_connections,
            "trial-object-seed": self.trial_object_seed,
            "music-rando-seed": self.music_rando_seed,
            "bk-angle-seed": self.bk_angle_seed,
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
        self.hints = jsn["hints"]
        self.trial_object_seed = jsn["trial-object-seed"]
        self.map_connections = jsn["map-connections"]
        self.music_rando_seed = jsn["music-rando-seed"]
        self.bk_angle_seed = jsn["bk-angle-seed"]

    def check_valid(self, areas):
        """checks, if the current state is valid, throws an exception otherwise
        This does not check consistency with all the settings"""
        if VERSION != self.version:
            raise InvalidPlacementFile(
                f"Version did not match, requires {self.version} but found {VERSION}."
            )

        for item in self.starting_items:
            if item not in ALLOWED_STARTING_ITEMS:
                raise InvalidPlacementFile(f"Invalid starting item {item}.")

        for req_dungeon in self.required_dungeons:
            if req_dungeon not in REGULAR_DUNGEONS:
                raise InvalidPlacementFile(
                    f"{req_dungeon} is not a valid required dungeon."
                )

        # if sorted(self.map_connections.keys()) != sorted(
        #     k
        #     for k, v in areas.map_exits.items()
        #     if v["type"] == "exit"
        #     if "vanilla" in v
        #     if not v.get("disabled", False)
        # ):
        #     raise InvalidPlacementFile("exit map_connections are wrong!")

        # if sorted(dict.fromkeys(self.map_connections.values())) != sorted(
        #     k
        #     for k, v in areas.map_entrances.items()
        #     if v["type"] == "entrance"
        #     if not v.get("disabled", False)
        # ):
        #     raise InvalidPlacementFile("map_connections entries are wrong!")

        for item in self.item_locations.values():
            if item not in ALL_ITEM_NAMES:
                raise InvalidPlacementFile(f'Invalid item "{item}".')

        check_sets_equal(
            set(areas.checks.keys()),
            set(self.item_locations.keys()),
            "Checks",
        )

        check_sets_equal(
            {FI_HINTS_KEY} | set(areas.gossip_stones.keys()) | set(SONG_HINTS),
            set(self.hints.keys()),
            "Gossip Stone Hints",
        )

        for hintlist in self.hints.values():
            if not isinstance(hintlist, list):
                raise InvalidPlacementFile(
                    "Gossip stone hints need to be LISTS of strings."
                )
            for hint in hintlist:
                if not isinstance(hint, str):
                    raise InvalidPlacementFile(
                        "Gossip stone hints need to be lists of STRINGS."
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
