from collections import OrderedDict
from functools import cached_property
import sys
import re
import random
from pathlib import Path
import hashlib
import json
import yaml
import subprocess

from logic.constants import *
from logic.inventory import EXTENDED_ITEM
from logic.fill_algo_common import UserOutput
from logic.randomize import Rando
from logic.hints import Hints
from logic.logic_input import Areas
from logic.placement_file import PlacementFile
import SpoilerLog

from gamepatches import GamePatcher, GAMEPATCH_TOTAL_STEP_COUNT
from paths import CUSTOM_HINT_DISTRIBUTION_PATH, RANDO_ROOT_PATH, IS_RUNNING_FROM_SOURCE
from options import OPTIONS, Options
from sslib.utils import encodeBytes
from version import VERSION, VERSION_WITHOUT_COMMIT

from typing import List, Callable


class StartupException(Exception):
    pass


class GenerationFailed(Exception):
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

    def randomize(self):
        """patch the game, or only write the spoiler log, depends on the implementation"""
        raise NotImplementedError("abstract")


def calculate_rando_hash(seed: int, options: Options):
    assert seed != -1
    # hash of seed, options, version
    current_hash = hashlib.md5()
    current_hash.update(str(seed).encode("ASCII"))
    current_hash.update(options.get_permalink().encode("ASCII"))
    current_hash.update(VERSION.encode("ASCII"))
    if options["hint-distribution"] == "Custom":
        if not CUSTOM_HINT_DISTRIBUTION_PATH.exists():
            raise Exception(
                "Custom hint distribution file not found. Make sure custom_hint_distribution.json exists at the same location as the randomizer"
            )
        with CUSTOM_HINT_DISTRIBUTION_PATH.open("r") as f:
            normalized_json = json.dumps(json.load(f))
            current_hash.update(normalized_json.encode("ASCII"))
    with open(RANDO_ROOT_PATH / "names.txt") as f:
        names = [s.strip() for s in f.readlines()]
    hash_random = random.Random()
    hash_random.seed(current_hash.digest())
    return " ".join(hash_random.choice(names) for _ in range(3))


class Randomizer(BaseRandomizer):
    def __init__(
        self, areas: Areas, options: Options, progress_callback=dummy_progress_callback
    ):
        super().__init__(progress_callback)
        self.areas = areas
        self.options = options

        self.no_logs = self.options["no-spoiler-log"]

        self.seed = self.options["seed"]
        if self.seed == -1:
            self.seed = random.randint(0, 1000000)
        self.options.set_option("seed", self.seed)

        print(f"Seed: {self.seed}")
        self.rng = random.Random(self.seed)
        if self.no_logs:
            for _ in range(100):
                self.rng.random()
        self.rando = Rando(self.areas, self.options, self.rng)
        self.excluded_locations = self.options["excluded-locations"]
        self.dry_run = bool(self.options["dry-run"])
        self.randomizer_hash = calculate_rando_hash(self.seed, self.options)

    def check_valid_directory_setup(self):
        # catch common errors with directory setup
        if not self.actual_extract_path.is_dir():
            raise StartupException(
                "ERROR: directory actual-extract doesn't exist! Make sure you have the ISO extracted into that directory."
            )
        if not self.modified_extract_path.is_dir():
            raise StartupException(
                "ERROR: directory modified-extract doesn't exist! Make sure you have the contents of actual-extract copied over to modified-extract."
            )
        if not (self.actual_extract_path / "DATA").is_dir():
            raise StartupException(
                "ERROR: directory actual-extract doesn't contain a DATA directory! Make sure you have the ISO properly extracted into actual-extract."
            )
        if not (self.modified_extract_path / "DATA").is_dir():
            raise StartupException(
                "ERROR: directory 'DATA' in modified-extract doesn't exist! Make sure you have the contents of actual-extract copied over to modified-extract."
            )
        if not (
            self.modified_extract_path
            / "DATA"
            / "files"
            / "COPYDATE_CODE_2011-09-28_153155"
        ).exists():
            raise StartupException(
                "ERROR: the randomizer only supports NTSC-U 1.00 (North American)."
            )

    @cached_property
    def get_total_progress_steps(self):
        rando_steps = self.rando.get_total_progress_steps() + 3
        if self.dry_run:
            return rando_steps + 1
        else:
            return rando_steps + 1 + 1 + GAMEPATCH_TOTAL_STEP_COUNT

    def set_progress_callback(self, progress_callback: Callable[[str], None]):
        self.progress_callback = progress_callback

    def randomize(self):
        # make sure the output path is valid if we're writing the patched game
        if not (
            self.options["dry-run"] or (dir := self.options["output-folder"]).is_dir()
        ):
            raise ValueError(
                f"Path {dir} is not a directory. Please specify a valid output folder."
            )
        useroutput = UserOutput(GenerationFailed, self.progress_callback)
        self.progress_callback("randomizing items...")
        self.rando.randomize(useroutput)
        self.progress_callback("preparing for hints...")
        self.logic = self.rando.extract_hint_logic()
        del self.rando
        self.logic.check(useroutput)
        self.progress_callback("generating hints...")
        self.hints = Hints(self.options, self.rng, self.areas, self.logic)
        self.hints.do_hints(useroutput)
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

        goals = [DUNGEON_GOALS[dun] for dun in self.logic.required_dungeons] + [DEMISE]
        sots_items = {
            goal: self.logic.get_sots_items(
                EXTENDED_ITEM[self.areas.short_to_full(GOAL_CHECKS[goal])]
            )
            for goal in goals
        }

        if self.options["json"]:
            dump = SpoilerLog.dump_json(
                self.logic.placement,
                self.options,
                hash=self.randomizer_hash,
                progression_spheres=self.logic.calculate_playthrough_progression_spheres(),
                hints=self.logic.placement.hints,
                required_dungeons=self.logic.required_dungeons,
                sots_items=sots_items,
                barren_nonprogress=self.logic.get_barren_regions(),
                randomized_dungeon_entrance=self.logic.randomized_dungeon_entrance,
                randomized_trial_entrance=self.logic.randomized_trial_entrance,
                randomized_start_entrance=self.logic.randomized_start_entrance,
                randomized_start_statues=self.logic.randomized_start_statues,
                puzzles=self.logic.puzzles,
            )
            with log_address.open("w") as f:
                json.dump(dump, f, indent=2)
        else:
            with log_address.open("w") as f:
                SpoilerLog.write(
                    f,
                    self.logic.placement,
                    self.options,
                    self.areas,
                    hash=self.randomizer_hash,
                    progression_spheres=self.logic.calculate_playthrough_progression_spheres(),
                    hints=self.logic.placement.hints,
                    required_dungeons=self.logic.required_dungeons,
                    sots_items=sots_items,
                    barren_nonprogress=self.logic.get_barren_regions(),
                    randomized_dungeon_entrance=self.logic.randomized_dungeon_entrance,
                    randomized_trial_entrance=self.logic.randomized_trial_entrance,
                    randomized_start_entrance=self.logic.randomized_start_entrance,
                    randomized_start_statues=self.logic.randomized_start_statues,
                    puzzles=self.logic.puzzles,
                )
        if not self.dry_run:
            GamePatcher(
                self.areas,
                self.options,
                self.progress_callback,
                self.actual_extract_path,
                self.rando_root_path,
                self.exe_root_path,
                self.modified_extract_path,
                self.oarc_cache_path,
                self.arc_replacement_path,
                plcmt_file,
            ).do_all_gamepatches()
            self.progress_callback("patching done")

    def get_placement_file(self):
        MAX_SEED = 1_000_000
        # temporary placement file stuff

        plcmt_file = PlacementFile()
        plcmt_file.dungeon_connections = self.logic.randomized_dungeon_entrance
        plcmt_file.trial_connections = self.logic.randomized_trial_entrance
        plcmt_file.start_entrance = self.logic.randomized_start_entrance
        plcmt_file.start_statues = self.logic.randomized_start_statues
        plcmt_file.puzzles = self.logic.puzzles
        plcmt_file.hash_str = self.randomizer_hash
        plcmt_file.hints = {
            k: v.to_ingame_text(lambda s: self.areas.prettify(s))
            for (k, v) in self.logic.placement.hints.items()
        }
        plcmt_file.item_locations = self.logic.placement.locations
        dowsing_setting = self.options["chest-dowsing"]
        plcmt_file.chest_dowsing = self.logic.get_dowsing(dowsing_setting)
        plcmt_file.options = self.options
        plcmt_file.required_dungeons = self.logic.required_dungeons
        plcmt_file.starting_items = sorted(self.logic.placement.starting_items)
        plcmt_file.version = VERSION
        plcmt_file.trial_object_seed = self.rng.randint(1, MAX_SEED)
        plcmt_file.music_rando_seed = self.rng.randint(1, MAX_SEED)
        plcmt_file.bk_angle_seed = self.rng.randint(0, 2**32 - 1)
        plcmt_file.check_valid(self.areas)

        return plcmt_file


class PlandoRandomizer(BaseRandomizer):
    def __init__(
        self,
        placement_file: PlacementFile,
        areas,
        progress_callback=dummy_progress_callback,
    ):
        super().__init__(progress_callback)
        self.areas = areas
        self.placement_file = placement_file

    @cached_property
    def get_total_progress_steps(self):
        return GAMEPATCH_TOTAL_STEP_COUNT

    def randomize(self):
        GamePatcher(
            self.areas,
            self.placement_file.options,
            self.progress_callback,
            self.actual_extract_path,
            self.rando_root_path,
            self.exe_root_path,
            self.modified_extract_path,
            self.oarc_cache_path,
            self.arc_replacement_path,
            self.placement_file,
        ).do_all_gamepatches()


class YamlOrderedDictLoader(yaml.SafeLoader):
    pass


YamlOrderedDictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)),
)
