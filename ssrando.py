from collections import OrderedDict
import sys
import os
import re
import random
from pathlib import Path
import hashlib
import json
import yaml
import subprocess

from logic.logic import Logic
from logic.hints import Hints
import logic.constants as constants
from logic.placement_file import PlacementFile
from gamepatches import GamePatcher, GAMEPATCH_TOTAL_STEP_COUNT
from paths import RANDO_ROOT_PATH, IS_RUNNING_FROM_SOURCE
from options import OPTIONS, Options
import logic.item_types
from sslib.utils import encodeBytes
from version import VERSION, VERSION_WITHOUT_COMMIT

from typing import List, Callable


class StartupException(Exception):
    pass


def dummy_progress_callback(current_action_name):
    pass


class BaseRandomizer:
    """Class holding all the path and callback info for the GamePatcher"""

    def __init__(self, progress_callback=dummy_progress_callback):
        self.progress_callback = progress_callback
        # TODO: maybe make paths configurable?
        # exe root path is where the executable is
        self.exe_root_path = Path(".").resolve()
        # this is where all assets/read only files are
        self.rando_root_path = RANDO_ROOT_PATH
        self.actual_extract_path = self.exe_root_path / "actual-extract"
        self.modified_extract_path = self.exe_root_path / "modified-extract"
        self.oarc_cache_path = self.exe_root_path / "oarc"

        # not happy that is has to land here, it's used by both GamePatches and Logic
        with (self.rando_root_path / "checks.yaml").open("r") as f:
            self.item_locations = yaml.load(f, YamlOrderedDictLoader)

        for location_name in self.item_locations:
            if not "type" in self.item_locations[location_name]:
                print("ERROR, " + location_name + " doesn't have types!")
            types_string = self.item_locations[location_name]["type"]
            types = types_string.split(",")
            types = set((type.strip() for type in types))
            unknown_types = [x for x in types if not x in constants.ALL_TYPES]
            if len(unknown_types) != 0:
                raise Exception(f"unknown types: {unknown_types}")
            self.item_locations[location_name]["type"] = types

        with (RANDO_ROOT_PATH / "hints.yaml").open() as f:
            self.stonehint_definitions: dict = yaml.safe_load(f)

    def randomize(self):
        """patch the game, or only write the spoiler log, depends on the implementation"""
        raise NotImplementedError("abstract")


class Randomizer(BaseRandomizer):
    def __init__(self, options: Options, progress_callback=dummy_progress_callback):
        super().__init__(progress_callback)
        self.options = options
        # hack: if shops are vanilla, disable them as banned types because of bug net and progressive pouches
        if self.options["shop-mode"] == "Vanilla":
            banned_types = self.options["banned-types"]
            for unban_shop_item in ["beedle", "cheap", "medium", "expensive"]:
                if unban_shop_item in banned_types:
                    banned_types.remove(unban_shop_item)
            self.options.set_option("banned-types", banned_types)

        self.dry_run = bool(self.options["dry-run"])
        self.no_logs = self.options["no-spoiler-log"]
        self.seed = self.options["seed"]
        if self.seed == -1:
            self.seed = random.randint(0, 1000000)
        self.options.set_option("seed", self.seed)

        self.randomizer_hash = self._get_rando_hash()
        self.rng = random.Random()
        self.rng.seed(self.seed)
        if self.no_logs:
            self.rng.randint(0, 100)
        self.banned_types = self.options["banned-types"]

        self.logic = Logic(self)
        self.hints = Hints(self.logic)

        # self.logic.set_prerandomization_item_location("Beedle - Second 100 Rupee Item", "Rare Treasure")
        # self.logic.set_prerandomization_item_location("Beedle - Third 100 Rupee Item", "Rare Treasure")
        # self.logic.set_prerandomization_item_location("Beedle - 1000 Rupee Item", "Rare Treasure")
        # self.logic.set_prerandomization_item_location("Knight Academy - Fledge's Gift", "SV Small Key")
        # self.logic.set_prerandomization_item_location("Knight Academy - Owlan's Gift", "ET Map")
        # self.logic.set_prerandomization_item_location("Skyloft - Skyloft above waterfall", "Farore's Courage")
        # self.logic.set_prerandomization_item_location("Skyloft - Shed normal chest", "Potion Medal")
        # self.logic.set_prerandomization_item_location("Skyloft - Skyloft Archer minigame", "Heart Medal")
        # self.logic.set_prerandomization_item_location("Central Skyloft - Item in Bird Nest", "Sea Chart")
        # self.logic.set_prerandomization_item_location("Knight Academy - Sparring Hall Chest", "LanayruCaves Small Key")

    def _get_rando_hash(self):
        # hash of seed, options, version
        current_hash = hashlib.md5()
        current_hash.update(str(self.seed).encode("ASCII"))
        current_hash.update(self.options.get_permalink().encode("ASCII"))
        current_hash.update(VERSION.encode("ASCII"))
        with open(RANDO_ROOT_PATH / "names.txt") as f:
            names = [s.strip() for s in f.readlines()]
        hash_random = random.Random()
        hash_random.seed(current_hash.digest())
        return " ".join(hash_random.choice(names) for _ in range(3))

    def check_valid_directory_setup(self):
        # catch common errors with directory setup
        if not self.actual_extract_path.is_dir():
            raise StartupException(
                "ERROR: directory actual-extract doesn't exist! Make sure you have the ISO extracted into that directory"
            )
        if not self.modified_extract_path.is_dir():
            raise StartupException(
                "ERROR: directory modified-extract doesn't exist! Make sure you have the contents of actual-extract copied over to modified-extract"
            )
        if not (self.actual_extract_path / "DATA").is_dir():
            raise StartupException(
                "ERROR: directory actual-extract doesn't contain a DATA directory! Make sure you have the ISO properly extracted into actual-extract"
            )
        if not (self.modified_extract_path / "DATA").is_dir():
            raise StartupException(
                "ERROR: directory 'DATA' in modified-extract doesn't exist! Make sure you have the contents of actual-extract copied over to modified-extract"
            )
        if not (
            self.modified_extract_path
            / "DATA"
            / "files"
            / "COPYDATE_CODE_2011-09-28_153155"
        ).exists():
            raise StartupException("ERROR: the randomizer only supports NTSC-U 1.00")

    def get_total_progress_steps(self):
        if self.dry_run:
            return 2
        else:
            return 2 + GAMEPATCH_TOTAL_STEP_COUNT

    def set_progress_callback(self, progress_callback: Callable[[str], None]):
        self.progress_callback = progress_callback

    def randomize(self):
        self.progress_callback("randomizing items...")
        self.logic.randomize_items()
        self.woth_locations = self.logic.get_woth_locations()
        if self.options["hint-distribution"] == "Junk":
            self.hints.do_junk_hints()
        elif self.options["hint-distribution"] == "Normal":
            self.hints.do_normal_hints()
        elif self.options["hint-distribution"] == "Bingo":
            self.hints.do_bingo_hints()
        else:
            raise Exception(f"{self.options['hints']} is not a valid hint setting!")
        if self.no_logs:
            self.progress_callback("writing anti spoiler log...")
        else:
            self.progress_callback("writing spoiler log...")
        plcmt_file = self.get_placement_file()
        if self.options["out-placement-file"] and not self.no_logs:
            with open(f"placement_file_{self.seed}.json", "w") as f:
                f.write(plcmt_file.to_json_str())
        if self.options["json"]:
            self.write_spoiler_log_json()
        else:
            self.write_spoiler_log()
        if not self.dry_run:
            GamePatcher(self, plcmt_file).do_all_gamepatches()
        self.progress_callback("patching done")

    def write_spoiler_log(self):
        spoiler_log = self.get_log_header()

        if self.no_logs:
            # We still calculate progression spheres even if we're not going to write them anywhere to catch more errors in testing.
            self.logic.calculate_playthrough_progression_spheres()

            spoiler_log_output_path = self.options["output-folder"] / (
                "SS Random %s - Anti Spoiler Log.txt" % self.seed
            )
            with spoiler_log_output_path.open("w") as f:
                f.write(spoiler_log)

            return

        if len(self.logic.starting_items) > 0:
            spoiler_log += "\n\nStarting items:\n  "
            spoiler_log += "\n  ".join(self.logic.starting_items)
        spoiler_log += "\n\n\n"

        # Write required dungeons
        for i, dungeon in enumerate(self.logic.required_dungeons):
            spoiler_log += f"Required Dungeon {i+1}: " + dungeon + "\n"

        spoiler_log += "\n\n"

        # Write way of the hero (100% required) locations
        spoiler_log += "WotH:\n"
        for wothloc, item in self.woth_locations.items():
            spoiler_log += "  %-53s %s\n" % (wothloc + ":", item)

        spoiler_log += "\n\n"

        # Write progression spheres.
        spoiler_log += "Playthrough:\n"
        progression_spheres = self.logic.calculate_playthrough_progression_spheres()
        all_progression_sphere_locations = [
            loc for locs in progression_spheres for loc in locs
        ]
        zones, max_location_name_length = self.get_zones_and_max_location_name_len(
            all_progression_sphere_locations
        )
        format_string = "      %-" + str(max_location_name_length + 1) + "s %s\n"
        for i, progression_sphere in enumerate(progression_spheres):
            # skip single gratitude crystals
            progression_sphere = [
                loc
                for loc in progression_sphere
                if loc == "Past - Demise"
                or self.logic.done_item_locations[loc] != "Gratitude Crystal"
            ]
            spoiler_log += "%d:\n" % (i + 1)

            for zone_name, locations_in_zone in zones.items():
                if not any(
                    loc for (loc, _) in locations_in_zone if loc in progression_sphere
                ):
                    # No locations in this zone are used in this sphere.
                    continue

                spoiler_log += "  %s:\n" % zone_name

                for (location_name, specific_location_name) in locations_in_zone:
                    if location_name in progression_sphere:
                        if location_name == "Past - Demise":
                            item_name = "Defeat Demise"
                        else:
                            item_name = self.logic.done_item_locations[location_name]
                        spoiler_log += format_string % (
                            specific_location_name + ":",
                            item_name,
                        )

        spoiler_log += "\n\n\n"

        # Write item locations.
        spoiler_log += "All item locations:\n"
        zones, max_location_name_length = self.get_zones_and_max_location_name_len(
            self.logic.done_item_locations
        )
        format_string = "    %-" + str(max_location_name_length + 1) + "s %s\n"
        for zone_name, locations_in_zone in zones.items():
            spoiler_log += zone_name + ":\n"

            for (location_name, specific_location_name) in locations_in_zone:
                item_name = self.logic.done_item_locations[location_name]
                # skip single gratitude crystals, since they are forced vanilla
                if item_name == "Gratitude Crystal":
                    continue
                spoiler_log += format_string % (specific_location_name + ":", item_name)

        spoiler_log += "\n\n\n"

        # Write dungeon/secret cave entrances.
        spoiler_log += "Entrances:\n"
        for (
            entrance_name,
            dungeon_or_cave_name,
        ) in self.logic.entrance_connections.items():
            spoiler_log += "  %-48s %s\n" % (entrance_name + ":", dungeon_or_cave_name)

        spoiler_log += "\n\n"

        # Write randomized trials
        spoiler_log += "Trial Gates:\n"
        for trial_gate, trial in self.logic.trial_connections.items():
            spoiler_log += "  %-48s %s\n" % (trial_gate + ":", trial)

        spoiler_log += "\n\n\n"

        # Write hints
        spoiler_log += "Hints:\n"
        for hintlocation, hint in self.hints.hints.items():
            spoiler_log += "  %-53s %s\n" % (
                hintlocation + ":",
                hint.to_spoiler_log_text(),
            )

        spoiler_log += "\n\n\n"

        spoiler_log_output_path = self.options["output-folder"] / (
            "SS Random %s - Spoiler Log.txt" % self.seed
        )
        with spoiler_log_output_path.open("w") as f:
            f.write(spoiler_log)

    def write_spoiler_log_json(self):
        spoiler_log = self.get_log_header_json()
        if self.no_logs:
            # We still calculate progression spheres even if we're not going to write them anywhere to catch more errors in testing.
            self.logic.calculate_playthrough_progression_spheres()

            spoiler_log_output_path = self.options["output-folder"] / (
                "SS Random %s - Anti Spoiler Log.json" % self.seed
            )
            with spoiler_log_output_path.open("w") as f:
                json.dump(spoiler_log, f, indent=2)

            return
        spoiler_log["starting-items"] = self.logic.starting_items
        spoiler_log["required-dungeons"] = self.logic.required_dungeons
        spoiler_log["woth-locations"] = self.woth_locations
        spoiler_log[
            "playthrough"
        ] = self.logic.calculate_playthrough_progression_spheres()
        spoiler_log["item-locations"] = self.logic.done_item_locations
        spoiler_log["hints"] = dict(
            map(
                lambda kv: (kv[0], kv[1].to_spoiler_log_text()),
                self.hints.hints.items(),
            )
        )
        spoiler_log["entrances"] = self.logic.entrance_connections
        spoiler_log["trial-connections"] = self.logic.trial_connections

        spoiler_log_output_path = self.options["output-folder"] / (
            "SS Random %s - Spoiler Log.json" % self.seed
        )
        with spoiler_log_output_path.open("w") as f:
            json.dump(spoiler_log, f, indent=2)

    def get_log_header_json(self):
        header_dict = OrderedDict()
        header_dict["version"] = VERSION
        header_dict["permalink"] = self.options.get_permalink()
        header_dict["seed"] = self.seed
        header_dict["hash"] = self.randomizer_hash
        non_disabled_options = [
            (name, val)
            for (name, val) in self.options.options.items()
            if (
                self.options[name] not in [False, [], {}, OrderedDict()]
                or OPTIONS[name]["type"] == "int"
            )
        ]
        header_dict["options"] = OrderedDict(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("permalink", True),
                non_disabled_options,
            )
        )
        header_dict["cosmetic-options"] = OrderedDict(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("cosmetic", False),
                non_disabled_options,
            )
        )
        return header_dict

    def get_log_header(self):
        header = ""

        header += "Skyward Sword Randomizer Version %s\n" % VERSION

        header += "Permalink: %s\n" % self.options.get_permalink()

        header += "Seed: %s\n" % self.seed

        header += "Hash : %s\n" % self.randomizer_hash

        header += "Options selected:\n"
        non_disabled_options = [
            (name, val)
            for (name, val) in self.options.options.items()
            if (
                self.options[name] not in [False, [], {}, OrderedDict()]
                or OPTIONS[name]["type"] == "int"
            )
        ]

        def format_opts(opts):
            option_strings = []
            for option_name, option_value in opts:
                if isinstance(option_value, bool):
                    option_strings.append("  %s" % option_name)
                else:
                    option_strings.append("  %s: %s" % (option_name, option_value))
            return "\n".join(option_strings)

        header += format_opts(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("permalink", True),
                non_disabled_options,
            )
        )
        cosmetic_options = list(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("cosmetic", False),
                non_disabled_options,
            )
        )
        if cosmetic_options:
            header += "\n\nCosmetic Options:\n"
            header += format_opts(cosmetic_options)

        return header

    # def calculate_playthrough_progression_spheres(self):
    #     progression_spheres = []

    #     logic = Logic(self)
    #     previously_accessible_locations = []
    #     game_beatable = False
    #     while logic.unplaced_progress_items:
    #         progress_items_in_this_sphere = OrderedDict()

    #         accessible_locations = logic.get_accessible_remaining_locations()
    #         assert len(accessible_locations) >= len(previously_accessible_locations)
    #         locations_in_this_sphere = [
    #             loc
    #             for loc in accessible_locations
    #             if loc not in previously_accessible_locations
    #         ]
    #         if not locations_in_this_sphere:
    #             raise Exception("Failed to calculate progression spheres")

    #         if not self.options.get("keysanity"):
    #             # If the player gained access to any small keys, we need to give them the keys without counting that as a new sphere.
    #             newly_accessible_predetermined_item_locations = [
    #                 loc
    #                 for loc in locations_in_this_sphere
    #                 if loc in self.logic.prerandomization_item_locations
    #             ]
    #             newly_accessible_small_key_locations = [
    #                 loc
    #                 for loc in newly_accessible_predetermined_item_locations
    #                 if self.logic.prerandomization_item_locations[loc].endswith(
    #                     " Small Key"
    #                 )
    #             ]
    #             if newly_accessible_small_key_locations:
    #                 for small_key_location_name in newly_accessible_small_key_locations:
    #                     item_name = self.logic.prerandomization_item_locations[
    #                         small_key_location_name
    #                     ]
    #                     assert item_name.endswith(" Small Key")

    #                     logic.add_owned_item(item_name)

    #                 previously_accessible_locations += (
    #                     newly_accessible_small_key_locations
    #                 )
    #                 continue  # Redo this loop iteration with the small key locations no longer being considered 'remaining'.

    #         for location_name in locations_in_this_sphere:
    #             item_name = self.logic.done_item_locations[location_name]
    #             if item_name in logic.all_progress_items:
    #                 progress_items_in_this_sphere[location_name] = item_name

    #         if not game_beatable:
    #             game_beatable = logic.check_requirement_met(
    #                 "Can Reach and Defeat Demise"
    #             )
    #             if game_beatable:
    #                 progress_items_in_this_sphere["Past - Demise"] = "Defeat Demise"

    #         progression_spheres.append(progress_items_in_this_sphere)

    #         for location_name, item_name in progress_items_in_this_sphere.items():
    #             if item_name == "Defeat Demise":
    #                 continue
    #             logic.add_owned_item(item_name)

    #         previously_accessible_locations = accessible_locations

    #     if not game_beatable:
    #         # If the game wasn't already beatable on a previous progression sphere but it is now we add one final one just for this.
    #         game_beatable = logic.check_requirement_met("Can Reach and Defeat Demise")
    #         if game_beatable:
    #             final_progression_sphere = OrderedDict(
    #                 [
    #                     ("Past - Demise", "Defeat Demise"),
    #                 ]
    #             )
    #             progression_spheres.append(final_progression_sphere)

    #     return progression_spheres

    def get_zones_and_max_location_name_len(self, locations):
        zones = OrderedDict()
        max_location_name_length = 0
        for location_name in locations:
            zone_name, specific_location_name = self.logic.split_location_name_by_zone(
                location_name
            )

            if zone_name not in zones:
                zones[zone_name] = []
            zones[zone_name].append((location_name, specific_location_name))

            if len(specific_location_name) > max_location_name_length:
                max_location_name_length = len(specific_location_name)

        return (zones, max_location_name_length)

    def get_placement_file(self):
        # temporary placement file stuff
        trial_checks = {
            # (getting it text patch, inventory text line)
            "Skyloft Silent Realm - Stone of Trials": "Song of the Hero - Trial Hint",
            "Faron Silent Realm - Water Scale": "Farore's Courage - Trial Hint",
            "Lanayru Silent Realm - Clawshots": "Nayru's Wisdom - Trial Hint",
            "Eldin Silent Realm - Fireshield Earrings": "Din's Power - Trial Hint",
        }
        trial_hints = {}
        for (trial_check_name, hintname) in trial_checks.items():
            trial_gate = constants.SILENT_REALM_CHECKS[trial_check_name]
            randomized_trial = self.logic.trial_connections[trial_gate]
            randomized_trial_check = [
                trial for trial in trial_checks if trial.startswith(randomized_trial)
            ].pop()
            item = self.logic.done_item_locations[randomized_trial_check]
            hint_mode = self.options["song-hints"]
            if hint_mode == "Basic":
                if item in self.logic.all_progress_items:
                    useful_text = "You might need what it reveals..."
                    # print(f'{item} in {trial_check} is useful')
                else:
                    useful_text = "It's probably not too important..."
                    # print(f'{item} in {trial_check} is not useful')
            elif hint_mode == "Advanced":
                if randomized_trial_check in self.woth_locations:
                    useful_text = "Your spirit will grow by completing this trial"
                elif item in self.logic.all_progress_items:
                    useful_text = "You might need what it reveals..."
                else:
                    # barren
                    useful_text = "It's probably not too important..."
            elif hint_mode == "Direct":
                useful_text = f"This trial holds {item}"
            else:
                useful_text = ""
            trial_hints[hintname] = useful_text

        plcmt_file = PlacementFile()
        plcmt_file.entrance_connections = self.logic.entrance_connections
        plcmt_file.trial_connections = self.logic.trial_connections
        plcmt_file.hash_str = self.randomizer_hash
        plcmt_file.gossip_stone_hints = dict(
            (k, v.to_gossip_stone_text()) for (k, v) in self.hints.hints.items()
        )
        plcmt_file.trial_hints = trial_hints
        plcmt_file.item_locations = dict(
            (k, v)
            for (k, v) in self.logic.done_item_locations.items()
            if v != "Gratitude Crystal"
        )
        plcmt_file.options = self.options
        plcmt_file.required_dungeons = self.logic.required_dungeons
        plcmt_file.starting_items = self.logic.starting_items
        plcmt_file.version = VERSION

        plcmt_file.check_valid()

        return plcmt_file


class PlandoRandomizer(BaseRandomizer):
    def __init__(
        self, placement_file: PlacementFile, progress_callback=dummy_progress_callback
    ):
        super().__init__(progress_callback)
        self.placement_file = placement_file

    def get_total_progress_steps(self):
        return GAMEPATCH_TOTAL_STEP_COUNT

    def randomize(self):
        GamePatcher(self, self.placement_file).do_all_gamepatches()


class YamlOrderedDictLoader(yaml.SafeLoader):
    pass


YamlOrderedDictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)),
)
