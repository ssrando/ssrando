from options import Options
from version import VERSION
from logic.item_types import ALL_ITEM_NAMES
from logic.constants import POTENTIALLY_REQUIRED_DUNGEONS, ENTRANCE_CONNECTIONS

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
        self.hints = {}
        self.entrance_connections = {}

    def read_from_file(self, f):
        self._read_from_json(json.load(f))

    def read_from_str(self, s):
        self._read_from_json(json.loads(s))

    def to_json_str(self):
        retval = {
            "version": self.version,
            "permalink": self.options.get_permalink(),
            "hash": self.hash_str,
            "starting-items": self.starting_items,
            "required-dungeons": self.required_dungeons,
            "item-locations": self.item_locations,
            "hints": self.hints,
            "entrance_connections": self.entrance_connections,
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
        self.hints = jsn["hints"]
        self.entrance_connections = jsn["entrance_connections"]

    def check_valid(self, all_check_names, all_hint_names):
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

        if sorted(self.entrance_connections.keys()) != sorted(
            ENTRANCE_CONNECTIONS.keys()
        ):
            raise InvalidPlacementFile("dungeon entrance_connections are wrong!")

        if sorted(self.entrance_connections.values()) != sorted(
            ENTRANCE_CONNECTIONS.values()
        ):
            raise InvalidPlacementFile("dungeon entries are wrong!")

        item_names = ALL_ITEM_NAMES.copy()
        item_names.remove("Gratitude Crystal")

        for item in self.item_locations.values():
            if item not in item_names:
                raise InvalidPlacementFile(f'invalid item "{item}"')

        orig_check_names = set(all_check_names)
        check_names = set(self.item_locations.keys())
        if all_check_names != self.item_locations.keys():
            additional = check_names - orig_check_names
            missing = orig_check_names - check_names
            error_msg = ""
            if additional:
                error_msg += "Additional checks:\n"
                error_msg += ", ".join(additional) + "\n"
            if missing:
                error_msg += "Missing checks:\n"
                error_msg += ", ".join(missing) + "\n"
            raise InvalidPlacementFile(error_msg)

        orig_hints = set(all_hint_names)
        hint_names = set(self.hints.keys())
        if orig_hints != hint_names:
            additional = hint_names - orig_hints
            missing = orig_hints - hint_names
            error_msg = ""
            if additional:
                error_msg += "Additional hints:\n"
                error_msg += ", ".join(additional) + "\n"
            if missing:
                error_msg += "Missing hints:\n"
                error_msg += ", ".join(missing) + "\n"
            raise InvalidPlacementFile(error_msg)
