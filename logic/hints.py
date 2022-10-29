from enum import Enum
from logic.constants import *
from logic.inventory import EXTENDED_ITEM
from logic.logic import DNFInventory
from logic.logic_input import Areas

from hints.hint_distribution import HintDistribution
from hints.hint_types import *
from .randomize import LogicUtils, UserOutput
from options import Options
from paths import CUSTOM_HINT_DISTRIBUTION_PATH, RANDO_ROOT_PATH
from typing import Dict, List

STATUS = Enum("STATUS", ["required", "useful", "useless"])


class Hints:
    def __init__(self, options: Options, rng, areas: Areas, logic: LogicUtils):
        self.logic = logic
        self.areas = areas
        self.norm = areas.short_to_full
        self.placement = logic.placement
        self.options = options
        self.rng = rng

        self.dist = HintDistribution()
        if self.options["hint-distribution"] == "Custom":
            if not CUSTOM_HINT_DISTRIBUTION_PATH.exists():
                raise Exception(
                    "Custom distro file not found. Ensure that custom_hint_distribution.json exists in the same directory as the randomizer"
                )
            with CUSTOM_HINT_DISTRIBUTION_PATH.open("r") as f:
                self.dist.read_from_file(f)
        else:
            with open(
                RANDO_ROOT_PATH
                / f"hints/distributions/{self.options['hint-distribution']}.json"
            ) as f:
                self.dist.read_from_file(f)

    def do_hint_per_status(self, hintmodes, does_hint, hintcls, get_check, hintpack):
        for hintname, raw_check in hintpack.items():
            check = get_check(raw_check)
            item = self.logic.placement.locations[check]

            if does_hint:
                self.hinted_checks.append(check)

            status: Enum
            if item in self.logic.get_sots_items():
                status = STATUS.required
            elif item in self.logic.get_useful_items():
                status = STATUS.useful
            else:
                status = STATUS.useless

            self.hints[hintname] = hintcls(hintmodes[status], hintname, item)

    def do_non_hintstone_hints(self):
        self.hinted_checks: List[EIN] = []
        self.hints: Dict[EIN, SongHint] = {}

        hint_mode = self.options["song-hints"]

        hintmodes: Dict[Enum, Enum]
        if hint_mode == "None":
            hintmodes = {k: HINT_MODES.Empty for k in STATUS}
        elif hint_mode == "Direct":
            hintmodes = {k: HINT_MODES.Direct for k in STATUS}
        elif hint_mode == "Basic":
            hintmodes = {
                STATUS.required: HINT_MODES.Useful,
                STATUS.useful: HINT_MODES.Useful,
                STATUS.useless: HINT_MODES.Useless,
            }
        elif hint_mode == "Advanced":
            hintmodes = {
                STATUS.required: HINT_MODES.Required,
                STATUS.useful: HINT_MODES.Useful,
                STATUS.useless: HINT_MODES.Useless,
            }
        else:
            raise ValueError(f'Unknown value for setting "song-hints": "{hint_mode}".')

        does_hint = hint_mode != "None"

        def get_check(trial_gate):
            gate_exit = TRIAL_GATE_EXITS[trial_gate]
            associated_entrance = self.logic.placement.map_transitions[
                self.norm(gate_exit)
            ]
            trial_of_entrance = {
                self.norm(entrance_of_exit(exit)): trial
                for trial, exit in SILENT_REALM_EXITS.items()
            }.get(associated_entrance)
            if trial_of_entrance is None:
                raise self.useroutput.GenerationFailed(
                    "Cannot generate trial hint for non-trial check"
                )
            return self.norm(SILENT_REALM_CHECKS[trial_of_entrance])

        self.do_hint_per_status(hintmodes, does_hint, SongHint, get_check, SONG_HINTS)

        return self.hints, self.hinted_checks

    def do_hints(self, useroutput: UserOutput):
        self.useroutput = useroutput

        check_hint_status = {
            loc: check.get("hint") for loc, check in self.areas.checks.items()
        }

        # ensure prerandomized and banned locations cannot be hinted
        not_banned = self.logic.fill_restricted()
        banned_locs = [
            loc
            for loc, check in self.areas.checks.items()
            if not not_banned[check["req_index"]]
        ]
        unhintables = (
            banned_locs + self.logic.known_locations + [START_ITEM, UNPLACED_ITEM]
        )

        non_hintstone_hints, hinted_checks = self.do_non_hintstone_hints()

        self.dist.start(
            self.areas,
            self.options,
            self.logic,
            self.rng,
            unhintables + hinted_checks,
            check_hint_status,
        )

        self.logic.fill_inventory_i(monotonic=True)
        accessible_stones = list(self.logic.accessible_stones())

        self.hints_per_stone = {
            stone: (
                self.dist.hints_per_stone
                if stone in accessible_stones and stone not in self.dist.banned_stones
                else 0
            )
            for stone in self.areas.gossip_stones
        }

        nb_hints = sum(self.hints_per_stone.values())
        assert nb_hints <= MAX_STONE_HINTS
        nb_hints += self.dist.fi_hints
        assert self.dist.fi_hints <= MAX_FI_HINTS

        fi_hints, hintstone_hints = self.dist.get_hints(nb_hints)
        self.useroutput.progress_callback("placing hints...")
        hintstone_hints = {
            hintname: hint for hint, hintname in zip(hintstone_hints, HINTS)
        }

        self.randomize(hintstone_hints)
        placed_fi_hints = {FI_HINTS_KEY: FiHintWrapper(fi_hints)}
        placed_hintstone_hints = {
            stone: GossipStoneHintWrapper(
                [
                    hintstone_hints[hintname]
                    for hintname in self.logic.placement.stones[stone]
                ]
            )
            for stone in self.areas.gossip_stones
        }
        self.logic.placement.hints = (
            placed_fi_hints | placed_hintstone_hints | non_hintstone_hints
        )

    def randomize(self, hints: Dict[EIN, RegularHint]):
        for hintname, hint in hints.items():
            hint_bit = EXTENDED_ITEM[hintname]
            if isinstance(hint, LocationHint) and hint.item in EXTENDED_ITEM:
                itembit = EXTENDED_ITEM[hint.item]
                hint_req = DNFInventory(hint_bit)
                self.logic.backup_requirements[itembit] &= hint_req
                self.logic.requirements[itembit] &= hint_req

            self.logic.inventory |= hint_bit

        self.logic.aggregate = self.logic.aggregate_requirements(
            self.logic.requirements, None
        )
        self.logic.fill_inventory_i(monotonic=False)

        for hintname in hints:
            if not self.place_hint(hintname):
                raise self.useroutput.GenerationFailed(
                    f"Could not find a valid location to place {hintname}. This may be because the settings are too restrictive. Try randomizing a new seed."
                )

    def place_hint(self, hintname: EXTENDED_ITEM_NAME, depth=0) -> bool:
        hint_bit = EXTENDED_ITEM[hintname]
        self.logic.remove_item(hint_bit)

        accessible_stones = list(self.logic.accessible_stones())

        available_stones = [
            stone
            for stone in accessible_stones
            for spot in range(
                self.hints_per_stone[stone] - len(self.logic.placement.stones[stone])
            )
        ]

        if available_stones:
            stone = self.rng.choice(available_stones)
            result = self.logic.place_item(stone, hintname, hint_mode=True)
            assert result  # Undefined if False
            return True

        # We have to replace an already placed hint
        if depth > 50:
            return False
        if not accessible_stones:
            raise self.useroutput.GenerationFailed(
                f"No more locations accessible for {hintname}."
            )

        spots = [
            (stone, old_hint)
            for stone in accessible_stones
            for old_hint in self.placement.stones[stone]
        ]
        stone, old_hint = self.rng.choice(spots)
        old_removed_hint = self.logic.replace_item(stone, hintname, old_hint)
        return self.place_hint(old_removed_hint, depth + 1)
