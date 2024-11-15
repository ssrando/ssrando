from enum import Enum
from logic.bool_expression import check_static_option_req
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

    def do_hint_per_status(self, hintmodes, does_hint, hintcls, get_checks, hintpack):
        for hintname, raw_check in hintpack.items():
            checks = get_checks(raw_check)
            item, num_useful = self.most_important_item(
                [self.logic.placement.locations[check] for check in checks]
            )

            if does_hint:
                self.hinted_checks.extend(checks)

            status = self.logic.get_importance_for_item(item)

            if self.options["hint-importance"]:
                importance = status
            else:
                importance = HINT_IMPORTANCE.Null

            self.hints[hintname] = hintcls(
                hintmodes[status], hintname, item, importance, num_useful
            )

    def do_non_hintstone_hints(self):
        self.hinted_checks: List[EIN] = []
        self.hints: Dict[EIN, SongHint] = {}

        hint_mode = self.options["song-hints"]

        hintmodes: Dict[Enum, Enum]
        if hint_mode == "None":
            hintmodes = {k: HINT_MODES.Empty for k in HINT_IMPORTANCE}
        elif hint_mode == "Direct":
            hintmodes = {k: HINT_MODES.Direct for k in HINT_IMPORTANCE}
        elif hint_mode == "Comprehensive":
            hintmodes = {k: HINT_MODES.Comprehensive for k in HINT_IMPORTANCE}
        elif hint_mode == "Basic":
            hintmodes = {
                HINT_IMPORTANCE.Required: HINT_MODES.Useful,
                HINT_IMPORTANCE.PossiblyRequired: HINT_MODES.Useful,
                HINT_IMPORTANCE.NotRequired: HINT_MODES.Useless,
                HINT_IMPORTANCE.Null: HINT_MODES.Useless,
            }
        elif hint_mode == "Advanced":
            hintmodes = {
                HINT_IMPORTANCE.Required: HINT_MODES.Required,
                HINT_IMPORTANCE.PossiblyRequired: HINT_MODES.Useful,
                HINT_IMPORTANCE.NotRequired: HINT_MODES.Useless,
                HINT_IMPORTANCE.Null: HINT_MODES.Useless,
            }
        else:
            raise ValueError(f'Unknown value for setting "song-hints": "{hint_mode}".')

        does_hint = hint_mode != "None"
        if hint_mode != "Comprehensive":
            get_checks = lambda trial_gate: [
                self.norm(
                    SILENT_REALM_CHECKS[
                        self.logic.randomized_trial_entrance[trial_gate]
                    ]
                )
            ]
        else:
            get_checks = lambda trial_gate: self.logic.locations_by_hint_region(
                self.logic.randomized_trial_entrance[trial_gate]
            )

        self.do_hint_per_status(hintmodes, does_hint, SongHint, get_checks, SONG_HINTS)

        return self.hints, self.hinted_checks

    def do_hints(self, useroutput: UserOutput):
        self.useroutput = useroutput

        def get_hint_pool(check):
            if not (hint := check.get("hint", None)):
                return None

            if type(hint) == str:
                # simple hint type, e.g. hint: always
                return hint

            # the always condition is always checked first!
            for pool in ["always", "sometimes"]:
                condition = hint.get(pool, None)
                if condition and check_static_option_req(
                    condition, self.options, self.logic.required_dungeons
                ):
                    return pool

            return None

        check_hint_status = {
            loc: hint
            for loc, check in self.areas.checks.items()
            if (hint := get_hint_pool(check))
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
            self.useroutput,
            self.areas,
            self.options,
            self.logic,
            self.rng,
            unhintables + hinted_checks,
            check_hint_status,
        )
        fi_hints, hintstone_hints = self.dist.get_hints()
        self.useroutput.progress_callback("placing hints...")
        hintstone_hints = {
            hintname: hint for hint, hintname in zip(hintstone_hints, HINTS)
        }
        self.hints_per_stone = self.dist.hints_per_stone
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
        for _, hintlist in placed_hintstone_hints.items():
            if not hintlist.hints:
                # make sure there are no empty textboxes
                hintlist.hints = [EmptyHint("I have nothing to tell you")]
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

    # Given a list of items, returns (in this priority)...
    # - a random SotS item if one exists
    # - a random possibly required item if one exists
    # - a random item if one exists
    # along with a count of how many useful items are in the list
    def most_important_item(self, items: List[EIN]) -> tuple[EIN, int]:
        num_useful = 0
        req_items = []
        possibly_req_items = []
        for item in items:
            importance = self.logic.get_importance_for_item(item)
            if importance == HINT_IMPORTANCE.Required:
                req_items.append(item)
                num_useful += 1
            elif importance == HINT_IMPORTANCE.PossiblyRequired:
                possibly_req_items.append(item)
                num_useful += 1

        if req_items:
            return (self.rng.choice(req_items), num_useful)

        if possibly_req_items:
            return (self.rng.choice(possibly_req_items), num_useful)

        return (self.rng.choice(items), 0)
