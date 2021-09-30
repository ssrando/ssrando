import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ssrando import Randomizer
from options import Options
from logic.placement_file import PlacementFile


def test_roundtrip():
    opts = Options()
    opts.set_option("dry-run", True)
    for i in range(5):
        opts.set_option("seed", i)
        rando = Randomizer(opts)
        rando.logic.randomize_items()
        # this belongs to the randomizer
        rando.woth_locations = rando.logic.get_woth_locations()
        if rando.options["hint-distribution"] == "Junk":
            rando.hints.do_junk_hints()
        elif rando.options["hint-distribution"] == "Normal":
            rando.hints.do_normal_hints()
        elif rando.options["hint-distribution"] == "Bingo":
            rando.hints.do_bingo_hints()
        else:
            raise Exception(f"{rando.options['hints']} is not a valid hint setting!")
        plcmt_file = rando.get_placement_file()
        round_tripped_file = PlacementFile()
        round_tripped_file.read_from_str(plcmt_file.to_json_str())
        assert (
            plcmt_file.entrance_connections == round_tripped_file.entrance_connections
        )
        assert plcmt_file.gossip_stone_hints == round_tripped_file.gossip_stone_hints
        assert plcmt_file.hash_str == round_tripped_file.hash_str
        assert plcmt_file.item_locations == round_tripped_file.item_locations
        assert plcmt_file.options.get_permalink(
            exclude_seed=True
        ) == round_tripped_file.options.get_permalink(exclude_seed=True)
        assert plcmt_file.required_dungeons == round_tripped_file.required_dungeons
        assert plcmt_file.starting_items == round_tripped_file.starting_items
        assert plcmt_file.trial_hints == round_tripped_file.trial_hints
        assert plcmt_file.version == round_tripped_file.version
