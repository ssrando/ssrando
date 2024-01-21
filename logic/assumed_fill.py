from __future__ import annotations
from dataclasses import dataclass
import random  # Only for typing purposes


from .constants import *
from .logic import Logic
from .inventory import BANNED_BIT, EVERYTHING_UNBANNED_BIT, EXTENDED_ITEM
from .fill_algo_common import RandomizationSettings, UserOutput

PRINT_PROGRESS = False
PRINT_NONPROGRESS = False


class AssumedFill:
    def __init__(
        self, logic: Logic, rng: random.Random, randosettings: RandomizationSettings
    ):
        self.logic = logic
        self.rng = rng
        self.randosettings = randosettings

        full_inventory = Logic.get_everything_unbanned(self.logic.requirements)
        truly_progress_item = Logic.aggregate_requirements(
            self.logic.requirements, full_inventory, EVERYTHING_UNBANNED_BIT
        )

        # Initialize item related attributes.
        self.restricted_vanilla_items: Dict[EIN, None] = {
            item: None for item in randosettings.restricted_vanilla_items
        }

        self.restricted_non_vanilla_items: Dict[EIN, None] = {
            item: None for item in randosettings.restricted_non_vanilla_items
        }

        self.progress_items: Dict[EIN, None] = {
            item: None
            for item in randosettings.must_be_placed_items
            | dict.fromkeys(randosettings.may_be_placed_items)
            if truly_progress_item[EXTENDED_ITEM[item]]
            if item
            not in self.restricted_vanilla_items | self.restricted_non_vanilla_items
        }

        self.must_be_placed_items = [
            item
            for item in self.randosettings.must_be_placed_items
            if item
            not in self.progress_items
            | self.restricted_vanilla_items
            | self.restricted_non_vanilla_items
        ]

        self.may_be_placed_items = [
            item
            for item in self.randosettings.may_be_placed_items
            if item not in self.progress_items
        ]

    def get_total_progress_steps(self):
        return len(self.progress_items) + len(self.must_be_placed_items) + 1

    def randomize(self, useroutput: UserOutput):
        self.useroutput = useroutput

        # The order of operations (mostly) is a guess at this point
        restricted_vanilla_list = list(self.restricted_vanilla_items)
        restricted_non_vanilla_list = list(self.restricted_non_vanilla_items)

        self.rng.shuffle(restricted_vanilla_list)
        self.rng.shuffle(restricted_non_vanilla_list)

        # Ensure vanilla items get placed 1st by adding it to restricted_items 1st.
        # Otherwise, more loosly restricted items could steal the place of vanilla restricted items.
        restricted_list = restricted_vanilla_list + restricted_non_vanilla_list

        # Allow items with restrictions in banned locations to be placed.
        # Mainly allows for dungeon items to be placed even if they are unrequired.
        # Logic should still fail to place items in banned locations (see logic.py def accessible_checks).
        self.logic.add_item(BANNED_BIT)

        for item in restricted_list:
            self.useroutput.progress_callback("placing restricted items...")

            # Prevents dungeon items being randomized to disabled sanity locations.
            if item in restricted_non_vanilla_list:
                has_placed_item = self.place_item(item, is_progress=True)
            else:
                has_placed_item = self.place_item(item, is_progress=False)

            if not has_placed_item:
                raise self.useroutput.GenerationFailed(
                    f"Could not find a valid location to place {item}. This may be because the settings are too restrictive. Try randomizing a new seed."
                )

        # Re-ban the banned when placing non-restricted progress items.
        self.logic.remove_item(BANNED_BIT)

        progress_list = list(self.progress_items)
        self.rng.shuffle(progress_list)

        for item in progress_list:
            self.useroutput.progress_callback("placing progress items...")

            if not self.place_item(item):
                raise self.useroutput.GenerationFailed(
                    f"Could not find a valid location to place {item}. This may be because the settings are too restrictive. Try randomizing a new seed."
                )

        # for i, (e, _) in enumerate(self.logic.pools):
        #     for _ in range(len(e)):
        #         self.link(i)

        self.rng.shuffle(self.must_be_placed_items)
        self.rng.shuffle(self.may_be_placed_items)

        # Now that progress items have been placed, allow items to be placed in banned locations.
        self.logic.add_item(BANNED_BIT)

        for item in self.must_be_placed_items:
            self.useroutput.progress_callback("placing nonprogress items...")
            assert self.place_item(item, is_progress=False)

        self.useroutput.progress_callback("placing remaining items...")

        unplaced = set()
        for item in self.may_be_placed_items:
            if not unplaced:
                if not self.place_item(item, force=False, is_progress=False):
                    unplaced.add(item)
            else:
                unplaced.add(item)

        self.logic.placement.add_unplaced_items(unplaced)

        if PRINT_NONPROGRESS:
            print(f"Unplaced items: {list(unplaced)}")

        self.fill_with_junk(self.randosettings.duplicable_items)

    def fill_with_junk(self, junk):
        empty_locations = [
            loc
            for loc in self.logic.accessible_checks()
            if loc not in self.logic.placement.locations
        ]
        junk = list(junk)

        for location in empty_locations:
            result = self.logic.place_item(location, self.rng.choice(junk), fill=False)
            assert result

    def place_item(
        self,
        item: EXTENDED_ITEM_NAME,
        depth=0,
        force=True,
        is_progress=True,
    ) -> bool:
        if item in EXTENDED_ITEM:
            self.logic.remove_item(EXTENDED_ITEM[item])

        placement_limit: EIN = self.logic.placement.item_placement_limit.get(
            item, EIN("")
        )

        accessible_locations = self.logic.accessible_checks(placement_limit)

        empty_locations = [
            loc
            for loc in accessible_locations
            if loc not in self.logic.placement.locations
            and not (
                is_progress
                and loc in self.logic.placement.item_placement_limit.values()
            )
        ]

        if empty_locations:
            location = self.rng.choice(empty_locations)
            result = self.logic.place_item(location, item, fill=force)
            if (is_progress and PRINT_PROGRESS) or (
                not is_progress and PRINT_NONPROGRESS
            ):
                print(
                    f"Placed {self.logic.areas.prettify(item)}"
                    f" in {self.logic.areas.prettify(location)}"
                )
            assert result  # Undefined if False
            return True

        # We have to replace an already placed item
        if not force or depth > 50:
            return False
        if not accessible_locations:
            raise self.useroutput.GenerationFailed(
                f"No more locations accessible for {item}."
            )

        self.check_known_failures(item)

        if had_banned := self.logic.inventory[BANNED_BIT]:
            self.logic.remove_item(BANNED_BIT)
        location = self.rng.choice(accessible_locations)
        new_item = self.logic.replace_item(location, item)
        if (is_progress and PRINT_PROGRESS) or (not is_progress and PRINT_NONPROGRESS):
            print(
                f"No empty location, placed {self.logic.areas.prettify(item)}"
                f" in {self.logic.areas.prettify(location)}"
                f" removing {self.logic.areas.prettify(new_item)}"
            )
        if new_item not in self.progress_items and had_banned:
            self.logic.add_item(BANNED_BIT)
        ret = self.place_item(new_item, depth + 1)
        if had_banned:
            self.logic.add_item(BANNED_BIT)
        return ret

    def check_known_failures(self, item):
        if (
            item in SMALL_KEYS[SSH]
            and self.logic.placement.items.get(number(PROGRESSIVE_BOW, 1))
            == UNPLACED_ITEM
            and self.logic.placement.items.get(number(PROGRESSIVE_BOW, 2))
            == UNPLACED_ITEM
            and not self.logic.full_inventory[EXTENDED_ITEM[number(PROGRESSIVE_BOW, 0)]]
        ):
            raise self.useroutput.GenerationFailed(
                f"Known generation failure: Vanilla Bow."
            )

        if (
            item in SMALL_KEYS[AC]
            and not self.logic.full_inventory[EXTENDED_ITEM[CISTERN_CLIP]]
            and not self.logic.full_inventory[EXTENDED_ITEM[WHIP]]
        ):
            raise self.useroutput.GenerationFailed(
                f"Known generation failure: Vanilla Whip."
            )

    def link(self, pool: int, entrance=None, depth=0):
        entrance_pool, exit_pool = self.logic.pools[pool]
        unassigned_entrances = [
            entrance
            for entrance in entrance_pool.values()
            if entrance.entrance not in self.logic.placement.reverse_map_transitions
        ]
        if entrance is None:
            entrance = self.rng.choice(unassigned_entrances)
        else:
            assert entrance in unassigned_entrances

        accessible_exits = list(self.logic.accessible_exits(exit_pool.values()))
        unassigned_exits, assigned_exits = [], []
        for exit in accessible_exits:
            if exit in self.logic.placement.map_transitions:
                assigned_exits.append(exit)
            else:
                unassigned_exits.append(exit)
        self.rng.shuffle(unassigned_exits)

        for exit in unassigned_exits:
            result = self.logic.link_connection(exit, entrance, pool)
            if result:
                return

        # No unassigned exit works, so we try with already assigned exits
        self.rng.shuffle(assigned_exits)
        for exit in unassigned_exits:
            result = self.logic.relink_connection(exit, entrance, pool)
            if result:
                self.link(pool, result, depth + 1)

        raise ValueError("No exit could be found for the entrance.")
