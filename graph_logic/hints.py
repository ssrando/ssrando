from graph_logic.constants import *
from graph_logic.inventory import EXTENDED_ITEM
from graph_logic.logic import DNFInventory
from graph_logic.logic_input import Areas
from hints.hint_distribution import MAX_HINTS_PER_STONE, HintDistribution
from hints.hint_types import *
from .randomize import LogicUtils, UserOutput
from options import Options
from paths import RANDO_ROOT_PATH
from typing import Dict, List


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

    def do_hints(self, useroutput: UserOutput):
        self.useroutput = useroutput

        not_banned = self.logic.fill_restricted()
        needed_always_hints: List[EIN] = [
            loc
            for loc, check in self.areas.checks.items()
            if check.get("hint") == "always" and not_banned[check["req_index"]]
        ]
        needed_sometimes_hints = [
            loc
            for loc, check in self.areas.checks.items()
            if check.get("hint") == "sometimes" and not_banned[check["req_index"]]
        ]

        # ensure prerandomized locations cannot be hinted
        unhintables = list(self.logic.known_locations) + [START_ITEM, UNPLACED_ITEM]

        hint_mode = self.options["song-hints"]
        if hint_mode != "None":
            for check in SILENT_REALM_CHECKS.values():
                unhintables.append(self.norm(check))

        trial_hintnames = {
            # (getting it text patch, inventory text line)
            SKYLOFT_TRIAL_GATE: EIN("Song of the Hero - Trial Hint"),
            FARON_TRIAL_GATE: EIN("Farore's Courage - Trial Hint"),
            LANAYRU_TRIAL_GATE: EIN("Nayru's Wisdom - Trial Hint"),
            ELDIN_TRIAL_GATE: EIN("Din's Power - Trial Hint"),
        }

        for (trial_gate, hintname) in trial_hintnames.items():
            randomized_trial = self.logic.randomized_trial_entrance[trial_gate]
            randomized_check = SILENT_REALM_CHECKS[randomized_trial]
            item = self.logic.placement.locations[
                self.areas.short_to_full(randomized_check)
            ]

            if hint_mode == "Basic":
                if item in self.logic.get_useful_items():
                    useful_text = "You might need what it reveals..."
                else:
                    useful_text = "It's probably not too important..."
            elif hint_mode == "Advanced":
                if item in self.logic.get_sots_items():
                    useful_text = "Your spirit will grow by completing this trial"
                elif item in self.logic.get_useful_items():
                    useful_text = "You might need what it reveals..."
                else:  # barren
                    useful_text = "It's probably not too important..."
            elif hint_mode == "Direct":
                useful_text = f"This trial holds {item}"
            else:
                useful_text = ""
            self.placement.song_hints[hintname] = useful_text

        self.dist.start(
            self.areas,
            self.options,
            self.logic,
            self.rng,
            unhintables,
            needed_always_hints,
            needed_sometimes_hints,
        )
        hints = self.dist.get_hints()
        self.useroutput.progress_callback("placing hints...")
        hints = {hintname: hint for hint, hintname in zip(hints, HINTS)}
        self.max_hints_per_stone = self.dist.max_hints_per_stone
        self.randomize(hints)

        def wrap(hintnames):
            assert 0 <= len(hintnames) <= MAX_HINTS_PER_STONE
            return GossipStoneHintWrapper(
                *(hints[name] for name in hintnames),
                *(
                    self.dist._create_junk_hint()
                    for _ in range(MAX_HINTS_PER_STONE - len(hintnames))
                ),
            )

        return {
            stone: wrap(hintnames)
            for stone, hintnames in self.logic.placement.stones.items()
        }

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
                self.max_hints_per_stone[stone]
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
