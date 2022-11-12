from collections import OrderedDict
from functools import cached_property
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
from hints.hint_types import GossipStoneHintWrapper, SongHint
from gamepatches import GamePatcher, GAMEPATCH_TOTAL_STEP_COUNT
from paths import RANDO_ROOT_PATH, IS_RUNNING_FROM_SOURCE
from options import OPTIONS, Options
import logic.item_types
from sslib.utils import encodeBytes
from version import VERSION, VERSION_WITHOUT_COMMIT
import SpoilerLog

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
        self.arc_replacement_path = self.exe_root_path / "arc-replacements"
        self.log_file_path = self.exe_root_path / "logs"
        self.log_file_path.mkdir(exist_ok=True, parents=True)

        # not happy that is has to land here, it's used by both GamePatches and Logic
        with (self.rando_root_path / "checks.yaml").open("r") as f:
            self.item_locations = yaml.load(f, YamlOrderedDictLoader)

        for location_name in self.item_locations:
            if not "type" in self.item_locations[location_name]:
                print("ERROR, " + location_name + " doesn't have types!")
            types_string = self.item_locations[location_name]["type"]
            types = types_string.split(",")
            types = set((type.strip() for type in types))
            unknown_types = [x for x in types if not x in constants.BANNABLE_TYPES]
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
            for _ in range(100):
                self.rng.random()
        self.banned_types = self.options["banned-types"]

        self.logic = Logic(self)
        self.hints = Hints(self.logic)

        # self.logic.set_prerandomization_item_location("Beedle - Second 100 Rupee Item", "Rare Treasure")
        # self.logic.set_prerandomization_item_location("Beedle - Third 100 Rupee Item", "Rare Treasure")
        # self.logic.set_prerandomization_item_location("Beedle - 1000 Rupee Item", "Rare Treasure")
        # self.logic.set_prerandomization_item_location("Knight Academy - Fledge's Gift", "Skyview Small Key")
        # self.logic.set_prerandomization_item_location("Knight Academy - Owlan's Gift", "Earth Temple Map")
        # self.logic.set_prerandomization_item_location("Skyloft - Skyloft above waterfall", "Farore's Courage")
        # self.logic.set_prerandomization_item_location("Skyloft - Shed normal chest", "Potion Medal")
        # self.logic.set_prerandomization_item_location("Skyloft - Skyloft Archer minigame", "Heart Medal")
        # self.logic.set_prerandomization_item_location("Central Skyloft - Item in Bird Nest", "Sea Chart")
        # self.logic.set_prerandomization_item_location("Knight Academy - Sparring Hall Chest", "Lanayru Caves Small Key")

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

    @cached_property
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
        self.sots_locations, self.goal_locations = self.logic.get_sots_goal_locations()
        self.hints.do_hints()
        if self.no_logs:
            self.progress_callback("writing anti spoiler log...")
        else:
            self.progress_callback("writing spoiler log...")
        plcmt_file = self.get_placement_file()
        if self.options["out-placement-file"] and not self.no_logs:
            (self.log_file_path / f"placement_file_{self.seed}.json").write_text(
                plcmt_file.to_json_str()
            )

        anti = "Anti " if self.no_logs else ""
        ext = "json" if self.options["json"] else "txt"
        log_address = self.log_file_path / (
            f"SS Random {self.seed} - {anti}Spoiler Log.{ext}"
        )

        sots_locations: dict[str, list[tuple[str, str]]] = {
            goal: list(locs.items()) for goal, locs in self.goal_locations.items()
        } | {constants.DEMISE: list(self.sots_locations.items())}

        if self.options["json"]:
            dump = SpoilerLog.dump_json(
                self.options,
                self.logic,
                self.hints.hints,
                sots_locations,
                self.randomizer_hash,
            )

            with log_address.open("w") as f:
                json.dump(dump, f, indent=2)

        else:
            with log_address.open("w") as f:
                SpoilerLog.write(
                    f,
                    self.options,
                    self.logic,
                    self.hints.hints,
                    sots_locations,
                    self.randomizer_hash,
                )

        if not self.dry_run:
            GamePatcher(self, plcmt_file).do_all_gamepatches()
        self.progress_callback("patching done")

    def get_placement_file(self):
        MAX_SEED = 1_000_000
        # temporary placement file stuff

        plcmt_file = PlacementFile()
        plcmt_file.dungeon_connections = self.logic.entrance_connections
        plcmt_file.trial_connections = self.logic.trial_connections
        plcmt_file.hash_str = self.randomizer_hash
        plcmt_file.hints = {
            k: v.to_ingame_text() for (k, v) in self.hints.hints.items()
        }
        plcmt_file.item_locations = dict(
            (k, v)
            for (k, v) in self.logic.done_item_locations.items()
            if v != "Gratitude Crystal"
        )
        plcmt_file.chest_dowsing = self.logic.calculate_chest_dowsing_info()
        plcmt_file.options = self.options
        plcmt_file.required_dungeons = self.logic.required_dungeons
        plcmt_file.starting_items = self.logic.starting_items
        plcmt_file.version = VERSION
        plcmt_file.trial_object_seed = self.rng.randint(1, MAX_SEED)
        plcmt_file.music_rando_seed = self.rng.randint(1, MAX_SEED)

        plcmt_file.check_valid()

        return plcmt_file


class PlandoRandomizer(BaseRandomizer):
    def __init__(
        self, placement_file: PlacementFile, progress_callback=dummy_progress_callback
    ):
        super().__init__(progress_callback)
        self.placement_file = placement_file

    @cached_property
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
