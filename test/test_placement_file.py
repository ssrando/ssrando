import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ssrando import Hints, Randomizer
from options import Options
from logic.logic_input import Areas
from logic.placement_file import PlacementFile
from logic.fill_algo_common import UserOutput
from yaml_files import requirements, checks, hints, map_exits


@pytest.mark.skip(reason="broken, slow")
def test_roundtrip():
    areas = Areas(requirements, checks, hints, map_exits)
    useroutput = UserOutput(Exception, lambda s: None)
    opts = Options()
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(areas, opts)
        rando.rando.randomize(useroutput)
        rando.logic = rando.rando.extract_hint_logic()
        del rando.rando
        rando.logic.check(useroutput)
        rando.hints = Hints(rando.options, rando.rng, rando.areas, rando.logic)
        rando.hints.do_hints(useroutput)
        plcmt_file = rando.get_placement_file()
        round_tripped_file = PlacementFile()
        round_tripped_file.read_from_str(plcmt_file.to_json_str())
        assert plcmt_file.dungeon_connections == round_tripped_file.dungeon_connections
        assert plcmt_file.hints == round_tripped_file.hints
        assert plcmt_file.hash_str == round_tripped_file.hash_str
        assert plcmt_file.item_locations == round_tripped_file.item_locations
        assert plcmt_file.options.get_permalink(
            exclude_seed=True
        ) == round_tripped_file.options.get_permalink(exclude_seed=True)
        assert plcmt_file.required_dungeons == round_tripped_file.required_dungeons
        assert plcmt_file.starting_items == round_tripped_file.starting_items
        assert plcmt_file.version == round_tripped_file.version
