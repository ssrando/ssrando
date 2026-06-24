"""This file tests logic and option mapping behaviors to
ensure that options have the desired impact on requirements."""

import sys
import os
import random

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ssrando import Rando
from options import Options
from yaml_files import requirements, checks, hints, map_exits
from logic.logic_input import Areas
from logic.inventory import EXTENDED_ITEM


@pytest.fixture
def areas():
    yield Areas(requirements, checks, hints, map_exits)
    EXTENDED_ITEM.reset_for_test()


def get_checks(areas, options):
    rando = Rando(areas, options, random.Random(0))
    logic = rando.extract_hint_logic(test_access_internals=True)
    logic.fill_inventory_i()
    return logic.accessible_checks()


def test_gondo_upgrades(areas):
    options = Options()
    options.reset_to_default()
    options.set_option(
        "starting-items",
        [
            "Clawshots",
            "Lanayru Caves Small Key",
            "Progressive Beetle",
            "Progressive Beetle",
        ],
    )
    options.set_option("starting-tablet-count", 3)
    options.set_option("rupeesanity", True)

    # requires beetle
    first_pillar_check = areas.short_to_full(
        "Lanayru Sand Sea - Ancient Harbour - Rupee on First Pillar"
    )
    # requires quick beetle
    crown_check = areas.short_to_full(
        "Lanayru Sand Sea - Ancient Harbour - Left Rupee on Entrance Crown"
    )

    # with gondo upgrades placed, we can't upgrade to Quick Beetle
    options.set_option("gondo-upgrades", True)
    accessible_checks = get_checks(areas, options)
    assert first_pillar_check in accessible_checks
    assert crown_check not in accessible_checks

    # with gondo upgrades unplaced, we can farm flowers and hornet larvae
    # to upgrade to quick beetle at gondo
    options.set_option("gondo-upgrades", False)
    accessible_checks = get_checks(areas, options)
    assert first_pillar_check in accessible_checks
    assert crown_check in accessible_checks


def test_ban_caves_chest(areas):
    options = Options()
    options.reset_to_default()
    options.set_option("excluded-locations", ["Lanayru Caves - Chest"])
    # TODO this should not throw
    with pytest.raises(ValueError):
        get_checks(areas, options)


def test_damage_multiplier(areas):
    digspot_rbm_check = areas.short_to_full("Eldin Volcano - Digging Spot after Vents")

    options = Options()
    options.reset_to_default()
    options.set_option("starting-tablet-count", 3)
    options.set_option("starting-items", ["Progressive Slingshot", "Progressive Mitts"])
    accessible_checks = get_checks(areas, options)
    assert digspot_rbm_check in accessible_checks

    options.set_option("damage-multiplier", 13)
    accessible_checks = get_checks(areas, options)
    assert digspot_rbm_check not in accessible_checks

    options.set_option(
        "starting-items",
        ["Progressive Slingshot", "Progressive Mitts", "Fireshield Earrings"],
    )
    accessible_checks = get_checks(areas, options)
    assert digspot_rbm_check in accessible_checks
