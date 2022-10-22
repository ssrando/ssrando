import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ssrando import Randomizer
from options import Options
from yaml_files import graph_requirements, checks, hints, map_exits
from graph_logic.logic_input import Areas
from graph_logic.fill_algo_common import UserOutput

import time
import json

areas = Areas(graph_requirements, checks, hints, map_exits)
useroutput = UserOutput(Exception, lambda s: None)


def check_logs():
    opts = Options()
    opts.update_from_permalink("rQEAAASmAw==")
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(areas, opts)
        old_time = time.process_time()
        rando.rando.randomize(useroutput)
        print(time.process_time() - old_time)
        prog_spheres = rando.logic.calculate_playthrough_progression_spheres()
        with open(f"testlogs/log_{i:02}.json", "r") as f:
            should_prog_spheres = json.load(f)
        assert prog_spheres == should_prog_spheres


def write_logs():
    opts = Options()
    opts.update_from_permalink("rQEAAASmAw==")
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(areas, opts)
        old_time = time.process_time()
        rando.rando.randomize(useroutput)
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
        rando = Randomizer(areas, opts)
        rando.rando.randomize(useroutput)
        woth_items = {}
        not_woth_prog = {}
        # check for every progress item, if it's hard required
        for loc in rando.logic.placement.locations:
            item = rando.logic.placement.locations[loc]
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
        rando = Randomizer(areas, opts)
        rando.rando.randomize(useroutput)
        rando.logic.get_barren_regions()
        # with open(f'testlogs/log4_{i:02}.json','w') as f:
        #     json.dump(rando.logic.get_barren_regions(), f, indent=2)
