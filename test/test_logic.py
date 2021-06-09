import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ssrando import Randomizer
from options import Options

import time
import json


def check_logs():
    opts = Options()
    opts.update_from_permalink("rQEAAASmAw==")
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(opts)
        old_time = time.process_time()
        rando.logic.randomize_items()
        print(time.process_time() - old_time)
        prog_spheres = rando.calculate_playthrough_progression_spheres()
        with open(f"testlogs/log_{i:02}.json", "r") as f:
            should_prog_spheres = json.load(f)
        assert prog_spheres == should_prog_spheres


def write_logs():
    opts = Options()
    opts.update_from_permalink("rQEAAASmAw==")
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(opts)
        old_time = time.process_time()
        rando.logic.randomize_items()
        print(time.process_time() - old_time)
        prog_spheres = rando.logic.calculate_playthrough_progression_spheres()
        # prog_spheres = rando.calculate_playthrough_progression_spheres()
        # with open(f'testlogs/log2_{i:02}.json','w') as f:
        #     json.dump(prog_spheres, f, indent=2, sort_keys=True)


def test_woth():
    opts = Options()
    opts.update_from_permalink("rQEAAASmAw==")
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(opts)
        rando.logic.randomize_items()
        woth_items = {}
        not_woth_prog = {}
        # check for every progress item, if it's hard required
        for loc in rando.logic.item_locations:
            item = rando.logic.done_item_locations[loc]
            if item in rando.logic.all_progress_items:
                if rando.logic.can_finish_without_locations([loc]):
                    not_woth_prog[loc] = item
                else:
                    woth_items[loc] = item
        # with open(f'testlogs/log3_{i:02}.json','w') as f:
        #     json.dump({'not':not_woth_prog, 'woth': woth_items}, f, indent=2)


def test_barren():
    opts = Options()
    opts.update_from_permalink("rQEAAASmAw==")
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(opts)
        rando.logic.randomize_items()
        rando.logic.get_barren_regions()
        # with open(f'testlogs/log4_{i:02}.json','w') as f:
        #     json.dump(rando.logic.get_barren_regions(), f, indent=2)
