from collections import OrderedDict
import sys
import os
import re
import random
from pathlib import Path
import hashlib
import json
import subprocess

from logic.logic import Logic
from logic.hints import Hints
import logic.constants as constants
from gamepatches import GamePatcher, GAMEPATCH_TOTAL_STEP_COUNT
from paths import RANDO_ROOT_PATH, IS_RUNNING_FROM_SOURCE
from options import OPTIONS, Options
import logic.item_types
from sslib.utils import encodeBytes

from typing import List, Callable


class StartupException(Exception):
    pass


# Try to add the git commit hash to the version number if running from source.
if IS_RUNNING_FROM_SOURCE:
    VERSION = (RANDO_ROOT_PATH / "version.txt").read_text().strip()
    VERSION_WITHOUT_COMMIT = VERSION
    version_suffix = "_NOGIT"

    import subprocess

    try:
        version_suffix = (
            "_"
            + subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], cwd=Path(__file__).parent
            )
            .decode("ASCII")
            .strip()
        )
    except Exception:
        pass  # probably not git installed

    VERSION += version_suffix
else:
    VERSION = (RANDO_ROOT_PATH / "version-with-git.txt").read_text().strip()
    VERSION_WITHOUT_COMMIT = VERSION


def dummy_progress_callback(current_action_name):
    pass


class Randomizer:
    def __init__(self, options: Options, progress_callback=dummy_progress_callback):
        self.options = options
        # hack: if shops are vanilla, disable them as banned types because of bug net and progressive pouches
        if self.options["shop-mode"] == "Vanilla":
            banned_types = self.options["banned-types"]
            for unban_shop_item in ["beedle", "cheap", "medium", "expensive"]:
                if unban_shop_item in banned_types:
                    banned_types.remove(unban_shop_item)
            self.options.set_option("banned-types", banned_types)

        self.progress_callback = progress_callback
        self.dry_run = bool(self.options["dry-run"])
        # TODO: maybe make paths configurable?
        # exe root path is where the executable is
        self.exe_root_path = Path(".").resolve()
        # this is where all assets/read only files are
        self.rando_root_path = RANDO_ROOT_PATH
        if not self.dry_run:
            self.actual_extract_path = self.exe_root_path / "actual-extract"
            self.modified_extract_path = self.exe_root_path / "modified-extract"
            self.oarc_cache_path = self.exe_root_path / "oarc"
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
        dungeons = [
            "Skyview",
            "Earth Temple",
            "Lanayru Mining Facility",
            "Ancient Cistern",
            "Sandship",
            "Fire Sanctuary",
        ]
        if self.options["randomize-entrances"] == "None":
            dungeons.append("Sky Keep")
            dungeons.reverse()
        else:
            if self.options["randomize-entrances"] == "Dungeons":
                self.rng.shuffle(dungeons)
                dungeons.append("Sky Keep")
                dungeons.reverse()
            else:
                dungeons.append("Sky Keep")
                self.rng.shuffle(dungeons)
        self.entrance_connections = OrderedDict(
            [
                ("Dungeon Entrance In Deep Woods", dungeons.pop()),
                ("Dungeon Entrance In Eldin Volcano", dungeons.pop()),
                ("Dungeon Entrance In Lanayru Desert", dungeons.pop()),
                ("Dungeon Entrance In Lake Floria", dungeons.pop()),
                ("Dungeon Entrance In Sand Sea", dungeons.pop()),
                ("Dungeon Entrance In Volcano Summit", dungeons.pop()),
                ("Dungeon Entrance On Skyloft", dungeons.pop()),
            ]
        )
        assert len(dungeons) == 0, "Not all dungeons linked to an entrance"

        trials = [
            "Faron Silent Realm",
            "Lanayru Silent Realm",
            "Eldin Silent Realm",
            "Skyloft Silent Realm",
        ]

        trial_gates = [
            "Trial Gate in Faron Woods",
            "Trial Gate in Lanayru Desert",
            "Trial Gate in Eldin Volcano",
            "Trial Gate on Skyloft",
        ]

        if self.options["randomize-trials"] == True:
            self.rng.shuffle(trials)
        self.trial_connections = OrderedDict(zip(trial_gates, trials))

        # self.starting_items = (x.strip() for x in self.options['starting_items']
        # self.starting_items: List[str] = list(filter(lambda x: x != '', self.starting_items))
        self.starting_items = []

        self.required_dungeons = self.rng.sample(
            constants.POTENTIALLY_REQUIRED_DUNGEONS,
            k=self.options["required-dungeon-count"],
        )
        # make the order always consistent
        self.required_dungeons = [
            dungeon
            for dungeon in constants.POTENTIALLY_REQUIRED_DUNGEONS
            if dungeon in self.required_dungeons
        ]

        tablets = ["Emerald Tablet", "Ruby Tablet", "Amber Tablet"]
        self.starting_items.extend(
            self.rng.sample(tablets, k=self.options["starting-tablet-count"])
        )

        starting_sword_count = {
            "Swordless": 0,
            "Practice Sword": 1,
            "Goddess Sword": 2,
            "Goddess Longsword": 3,
            "Goddess White Sword": 4,
            "Master Sword": 5,
            "True Master Sword": 6,
        }

        for i in range(starting_sword_count[self.options["starting-sword"]]):
            self.starting_items.append("Progressive Sword")

        # if not self.options.get('randomize-sailcloth',False):
        #   self.starting_items.append('Sailcloth')
        if self.options["start-with-pouch"]:
            self.starting_items.append("Progressive Pouch")
        self.banned_types = self.options["banned-types"]
        self.race_mode_banned_locations = []
        self.non_required_dungeons = [
            dungeon
            for dungeon in constants.POTENTIALLY_REQUIRED_DUNGEONS
            if not dungeon in self.required_dungeons
        ]

        self.logic = Logic(self)
        # self.logic.set_prerandomization_item_location("Beedle - Second 100 Rupee Item", "Rare Treasure")
        # self.logic.set_prerandomization_item_location("Beedle - Third 100 Rupee Item", "Rare Treasure")
        # self.logic.set_prerandomization_item_location("Beedle - 1000 Rupee Item", "Rare Treasure")
        self.hints = Hints(self.logic)
        # self.logic.set_prerandomization_item_location("Skyloft Academy - Fledge", "SV Small Key")
        # self.logic.set_prerandomization_item_location("Skyloft Academy - Owlan's Shield", "ET Map")
        # self.logic.set_prerandomization_item_location("Skyloft - Skyloft above waterfall", "Farore's Courage")
        # self.logic.set_prerandomization_item_location("Skyloft - Shed normal chest", "Potion Medal")
        # self.logic.set_prerandomization_item_location("Skyloft - Skyloft Archer minigame", "Heart Medal")
        # self.logic.set_prerandomization_item_location("Skyloft - Baby Rattle", "Sea Chart")
        # self.logic.set_prerandomization_item_location("Skyloft Academy - Practice Sword", "LanayruCaves Small Key")

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
        if self.options["json"]:
            self.write_spoiler_log_json()
        else:
            self.write_spoiler_log()
        if not self.dry_run:
            GamePatcher(self).do_all_gamepatches()
        self.progress_callback("patching done")

    def write_spoiler_log(self):
        spoiler_log = self.get_log_header()

        if self.no_logs:
            # We still calculate progression spheres even if we're not going to write them anywhere to catch more errors in testing.
            self.calculate_playthrough_progression_spheres()

            spoiler_log_output_path = self.options["output-folder"] / (
                "SS Random %s - Anti Spoiler Log.txt" % self.seed
            )
            with spoiler_log_output_path.open("w") as f:
                f.write(spoiler_log)

            return

        if len(self.starting_items) > 0:
            spoiler_log += "\n\nStarting items:\n  "
            spoiler_log += "\n  ".join(self.starting_items)
        spoiler_log += "\n\n\n"

        # Write required dungeons
        for i, dungeon in enumerate(self.required_dungeons):
            spoiler_log += f"Required Dungeon {i+1}: " + dungeon + "\n"

        spoiler_log += "\n\n"

        # Write way of the hero (100% required) locations
        spoiler_log += "WotH:\n"
        for wothloc, item in self.woth_locations.items():
            spoiler_log += "  %-53s %s\n" % (wothloc + ":", item)

        spoiler_log += "\n\n"

        # Write progression spheres.
        spoiler_log += "Playthrough:\n"
        progression_spheres = self.calculate_playthrough_progression_spheres()
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
        for entrance_name, dungeon_or_cave_name in self.entrance_connections.items():
            spoiler_log += "  %-48s %s\n" % (entrance_name + ":", dungeon_or_cave_name)

        spoiler_log += "\n\n"

        # Write randomized trials
        spoiler_log += "Trial Gates:\n"
        for trial_gate, trial in self.trial_connections.items():
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
            self.calculate_playthrough_progression_spheres()

            spoiler_log_output_path = self.options["output-folder"] / (
                "SS Random %s - Anti Spoiler Log.json" % self.seed
            )
            with spoiler_log_output_path.open("w") as f:
                json.dump(spoiler_log, f, indent=2)

            return
        spoiler_log["starting-items"] = self.starting_items
        spoiler_log["required-dungeons"] = self.required_dungeons
        spoiler_log["woth-locations"] = self.woth_locations
        spoiler_log["playthrough"] = self.calculate_playthrough_progression_spheres()
        spoiler_log["item-locations"] = self.logic.done_item_locations
        spoiler_log["hints"] = dict(
            map(
                lambda kv: (kv[0], kv[1].to_spoiler_log_text()),
                self.hints.hints.items(),
            )
        )
        spoiler_log["entrances"] = self.entrance_connections

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
            name
            for name in self.options.options
            if (
                self.options[name] not in [False, [], {}, OrderedDict()]
                or OPTIONS[name]["type"] == "int"
            )
            and OPTIONS[name].get("permalink", True) == True
        ]
        header_dict["options"] = OrderedDict()
        for option_name in non_disabled_options:
            header_dict["options"][option_name] = self.options[option_name]
        return header_dict

    def get_log_header(self):
        header = ""

        header += "Skyward Sword Randomizer Version %s\n" % VERSION

        header += "Permalink: %s\n" % self.options.get_permalink()

        header += "Seed: %s\n" % self.seed

        header += "Hash : %s\n" % self.randomizer_hash

        header += "Options selected:\n"
        non_disabled_options = [
            name
            for name in self.options.options
            if (
                self.options[name] not in [False, [], {}, OrderedDict()]
                or OPTIONS[name]["type"] == "int"
            )
            and OPTIONS[name].get("permalink", True) == True
        ]
        option_strings = []
        for option_name in non_disabled_options:
            if isinstance(self.options[option_name], bool):
                option_strings.append("  %s" % option_name)
            else:
                value = self.options[option_name]
                option_strings.append("  %s: %s" % (option_name, value))
        header += "\n".join(option_strings)

        return header

    def calculate_playthrough_progression_spheres(self):
        progression_spheres = []

        logic = Logic(self)
        previously_accessible_locations = []
        game_beatable = False
        while logic.unplaced_progress_items:
            progress_items_in_this_sphere = OrderedDict()

            accessible_locations = logic.get_accessible_remaining_locations()
            assert len(accessible_locations) >= len(previously_accessible_locations)
            locations_in_this_sphere = [
                loc
                for loc in accessible_locations
                if loc not in previously_accessible_locations
            ]
            if not locations_in_this_sphere:
                raise Exception("Failed to calculate progression spheres")

            if not self.options.get("keysanity"):
                # If the player gained access to any small keys, we need to give them the keys without counting that as a new sphere.
                newly_accessible_predetermined_item_locations = [
                    loc
                    for loc in locations_in_this_sphere
                    if loc in self.logic.prerandomization_item_locations
                ]
                newly_accessible_small_key_locations = [
                    loc
                    for loc in newly_accessible_predetermined_item_locations
                    if self.logic.prerandomization_item_locations[loc].endswith(
                        " Small Key"
                    )
                ]
                if newly_accessible_small_key_locations:
                    for small_key_location_name in newly_accessible_small_key_locations:
                        item_name = self.logic.prerandomization_item_locations[
                            small_key_location_name
                        ]
                        assert item_name.endswith(" Small Key")

                        logic.add_owned_item(item_name)

                    previously_accessible_locations += (
                        newly_accessible_small_key_locations
                    )
                    continue  # Redo this loop iteration with the small key locations no longer being considered 'remaining'.

            for location_name in locations_in_this_sphere:
                item_name = self.logic.done_item_locations[location_name]
                if item_name in logic.all_progress_items:
                    progress_items_in_this_sphere[location_name] = item_name

            if not game_beatable:
                game_beatable = logic.check_requirement_met(
                    "Can Reach and Defeat Demise"
                )
                if game_beatable:
                    progress_items_in_this_sphere["Past - Demise"] = "Defeat Demise"

            progression_spheres.append(progress_items_in_this_sphere)

            for location_name, item_name in progress_items_in_this_sphere.items():
                if item_name == "Defeat Demise":
                    continue
                logic.add_owned_item(item_name)

            previously_accessible_locations = accessible_locations

        if not game_beatable:
            # If the game wasn't already beatable on a previous progression sphere but it is now we add one final one just for this.
            game_beatable = logic.check_requirement_met("Can Reach and Defeat Demise")
            if game_beatable:
                final_progression_sphere = OrderedDict(
                    [
                        ("Past - Demise", "Defeat Demise"),
                    ]
                )
                progression_spheres.append(final_progression_sphere)

        return progression_spheres

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
