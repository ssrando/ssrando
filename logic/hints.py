from enum import Enum
from logic.constants import *
from logic.inventory import EXTENDED_ITEM
from logic.logic import DNFInventory
from logic.logic_input import Areas
from hints.hint_distribution import HintDistribution
from hints.hint_types import *
from .randomize import LogicUtils, UserOutput
from options import Options
from paths import RANDO_ROOT_PATH
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

        with open(
            RANDO_ROOT_PATH
            / f"hints/distributions/{self.options['hint-distribution']}.json"
        ) as f:
            self.dist = HintDistribution()
            self.dist.read_from_file(f)

    def do_hint_per_status(self, hintmodes, does_hint, hintcls, get_check, hintpack):
        for (hintname, raw_check) in hintpack.items():
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
            raise ValueError(f'Unknown value for setting "song-hints": "{hint_mode}"')

        does_hint = hint_mode != "None"
        get_check = lambda trial_gate: self.norm(
            SILENT_REALM_CHECKS[self.logic.randomized_trial_entrance[trial_gate]]
        )

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
        hintstone_hints = self.dist.get_hints()
        self.useroutput.progress_callback("placing hints...")
        hintstone_hints = {
            hintname: hint for hint, hintname in zip(hintstone_hints, HINTS)
        }
        self.hints_per_stone = self.dist.hints_per_stone
        self.randomize(hintstone_hints)

        placed_hintstone_hints = {
            stone: GossipStoneHintWrapper(
                [hintstone_hints[hintname] for hintname in hintnames]
            )
            for stone, hintnames in self.logic.placement.stones.items()
        }

        self.logic.placement.hints = placed_hintstone_hints | non_hintstone_hints

    def randomize(self, hints: Dict[EIN, GossipStoneHint]):
        for hintname, hint in hints.items():
            hint_bit = EXTENDED_ITEM[hintname]
            if isinstance(hint, LocationGossipStoneHint) and hint.item in EXTENDED_ITEM:
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
                raise self.useroutput.GenerationFailed(f"could not place {hintname}")

    def place_hint(self, hintname: EXTENDED_ITEM_NAME, depth=0) -> bool:
        hint_bit = EXTENDED_ITEM[hintname]
        self.logic.remove_item(hint_bit)

        accessible_stones = list(self.logic.accessible_stones())

        available_stones = [
            stone
            for stone in accessible_stones
            for spot in range(
                self.dist.hints_per_stone[stone]
                - len(self.logic.placement.stones[stone])
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
                f"no more location accessible for {hintname}"
            )

        spots = [
            (stone, old_hint)
            for stone in accessible_stones
            for old_hint in self.placement.stones[stone]
        ]
        stone, old_hint = self.rng.choice(spots)
        old_removed_hint = self.logic.replace_item(stone, hintname, old_hint)
        return self.place_hint(old_removed_hint, depth + 1)
