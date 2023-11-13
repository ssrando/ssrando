from __future__ import annotations
from dataclasses import dataclass
import random  # Only for typing purposes


from .constants import *
from .logic import Logic
from .inventory import BANNED_BIT, EVERYTHING_UNBANNED_BIT, EXTENDED_ITEM
from .fill_algo_common import RandomizationSettings, UserOutput
from .entrance_rando import EntranceRandoFailure


class FrontFill:
    def __init__(
        self, logic: Logic, rng: random.Random, randosettings: RandomizationSettings
    ):
        self.logic = logic
        self.rng = rng
        self.randosettings = randosettings

        full_inventory = Logic.get_everything_unbanned(self.logic.requirements)

        if not (randosettings.check_bits <= full_inventory):
            raise EntranceRandoFailure(
                f"Could not reach all objectives after entrances randomization."
            )

        truly_progress_item = Logic.aggregate_requirements(
            self.logic.requirements, full_inventory, EVERYTHING_UNBANNED_BIT
        )

        # Initialize item related attributes.
        all_placeable_items = randosettings.must_be_placed_items | dict.fromkeys(
            randosettings.may_be_placed_items
        )

        self.dungeon_items = {
            item: None
            for item, limit in self.logic.placement.item_placement_limit.items()
            if limit != ""
            if item in all_placeable_items
        }

        self.progress_items: Dict[EIN, None] = {
            item: None
            for item in all_placeable_items
            if truly_progress_item[EXTENDED_ITEM[item]]
            if item not in self.dungeon_items
        }

        self.must_be_placed_items = {
            item: None
            for item in self.randosettings.must_be_placed_items
            if item not in self.progress_items
            if item not in self.dungeon_items
        }
        self.may_be_placed_items = {
            item: None
            for item in self.randosettings.may_be_placed_items
            if item not in self.progress_items
            if item not in self.dungeon_items
        }

        for item_name in self.logic.placement.starting_items:
            self.logic.add_item(EXTENDED_ITEM[item_name])

    def get_total_progress_steps(self):
        return 4

    # main randomization method
    def randomize(self, useroutput: UserOutput):
        self.useroutput = useroutput

        self.useroutput.progress_callback("placing dungeon items...")
        self.randomize_dungeon_items()  # this will only randomize the appropriate items
        self.useroutput.progress_callback("placing progress items...")
        self.randomize_progression_items()

        self.logic.add_item(BANNED_BIT)

        self.useroutput.progress_callback("placing nonprogress items...")
        self.randomize_nonprogress_items()
        self.useroutput.progress_callback("placing consumable items...")
        self.randomize_consumable_items()

    def randomize_dungeon_items(self):
        # Places dungeon-specific items first so all the dungeon locations don't get used up by other items.

        small_keys = {key: None for key in ALL_SMALL_KEYS if key in self.dungeon_items}
        boss_keys = {key: None for key in ALL_BOSS_KEYS if key in self.dungeon_items}
        triforces = {tri: None for tri in TRIFORCES if tri in self.dungeon_items}
        maps = {map: None for map in ALL_MAPS if map in self.dungeon_items}

        rest = {
            item: None
            for item in self.dungeon_items
            if item not in small_keys
            if item not in boss_keys
            if item not in triforces
            if item not in maps
        }

        assert not rest

        # Temporarily add all progress items except for dungeon keys while we randomize them.
        temp_items = {
            EXTENDED_ITEM[item_name]
            for item_name in self.progress_items | self.must_be_placed_items
        } | {BANNED_BIT}
        self.logic.add_items(temp_items)

        for item_name in small_keys:
            self.place_dungeon_item(item_name)

        for item_name in boss_keys:
            self.place_dungeon_item(item_name)

        for item_name in triforces:
            self.place_dungeon_item(item_name)

        for item_name in maps:
            self.place_dungeon_item(item_name)

        # Remove the items we temporarily added.
        self.logic.remove_items(temp_items)

    def place_dungeon_item(self, item_name):
        placement_limit = self.logic.placement.item_placement_limit[item_name]
        accessible_locations = self.logic.accessible_checks(placement_limit)

        empty_locations = [
            loc
            for loc in accessible_locations
            if loc not in self.logic.placement.locations
        ]

        if empty_locations:
            location = self.rng.choice(empty_locations)
            result = self.logic.place_item(location, item_name, fill=True)
            assert result  # Undefined if False
            return True

        raise self.useroutput.GenerationFailed(
            f"No more locations accessible for {item_name}."
        )

    def randomize_progression_items(self):
        accessible_undone_locations = [
            loc
            for loc in self.logic.accessible_checks()
            if loc not in self.logic.placement.locations
        ]
        if len(accessible_undone_locations) == 0:
            raise Exception(
                "No progress locations are accessible at the very start of the game."
            )

        unplaced_progress_items = list(self.progress_items)

        # Place progress items.
        location_weights = {}
        current_weight = 1
        while unplaced_progress_items:
            accessible_undone_locations = [
                loc
                for loc in self.logic.accessible_checks()
                if loc not in self.logic.placement.locations
            ]

            if not accessible_undone_locations:
                raise Exception("No locations left to place progress items.")

            for location in accessible_undone_locations:
                if location not in location_weights:
                    location_weights[location] = current_weight
                elif location_weights[location] > 1:
                    location_weights[location] -= 1
            current_weight += 1

            possible_items = unplaced_progress_items.copy()

            assert len(possible_items)

            # Remove duplicates from the list so items like swords and bows aren't so likely to show up early.
            # Don't do this with Eldin Key Pieces or Earth Temple will always be really late in logic. Same with crystals
            unique_names = []
            unique_possible_items = []
            for item_name in possible_items:
                if strip_item_number(item_name) not in unique_names:
                    unique_names.append(strip_item_number(item_name))
                    unique_possible_items.append(item_name)
                elif item_name in KEY_PIECES:
                    unique_possible_items.append(item_name)
                elif item_name in GRATITUDE_CRYSTAL_PACKS:
                    unique_possible_items.append(item_name)
                elif item_name in GRATITUDE_CRYSTALS:
                    unique_possible_items.append(item_name)
            possible_items = unique_possible_items

            must_place_useful_item = False
            should_place_useful_item = True
            if len(accessible_undone_locations) == 1 and len(possible_items) > 1:
                # If we're on the last accessible location but not the last item we HAVE to place an item that unlocks new locations.
                # (Otherwise we will still try to place a useful item, but failing will not result in an error.)
                must_place_useful_item = True
            elif len(accessible_undone_locations) >= 10:
                # If we have a lot of locations open, we don't need to be so strict with prioritizing currently useful items.
                # This can give the randomizer a chance to place things like Delivery Bag or small keys for dungeons that need x2 to do anything.
                should_place_useful_item = False

            possible_items_when_not_placing_useful = [name for name in possible_items]

            # Only exception is when there's exclusively groups left to place. Then we allow groups even if they're not useful.
            if (
                len(possible_items_when_not_placing_useful) == 0
                and len(possible_items) > 0
            ):
                possible_items_when_not_placing_useful = possible_items

            if must_place_useful_item or should_place_useful_item:
                shuffled_list = possible_items.copy()
                self.rng.shuffle(shuffled_list)
                item_name = self.get_first_useful_item(
                    shuffled_list, accessible_undone_locations
                )
                if item_name is None:
                    # This means that no item can unlock a new location
                    if must_place_useful_item:
                        raise Exception("No useful progress items to place.")
                    else:
                        assert False
                        # I didn't want to adapt this part because it's too obscure and apparently useless
            else:
                item_name = self.rng.choice(possible_items_when_not_placing_useful)

            # We weight it so newly accessible locations are more likely to be chosen.
            # This way there is still a good chance it will not choose a new location.
            # Dungeons are prefered
            possible_location_weights = []
            cumul_loc_weight = 0
            for location_name in accessible_undone_locations:
                cumul_loc_weight += location_weights[location_name]
                possible_location_weights.append(cumul_loc_weight)

            location_name = self.rng.choices(
                accessible_undone_locations, cum_weights=possible_location_weights, k=1
            )[0]
            self.logic.place_item(location_name, item_name)
            unplaced_progress_items.remove(item_name)

            # continue loop if items are remaining

    def get_first_useful_item(self, items_to_check, accessible_undone_locations):
        # Searches through a given list of items and returns the first one that opens up at least 1 new ~~location~~ thing.
        # The randomizer shuffles the list before passing it to this function, so in effect it picks a random useful item.

        # Originally, this really looked for opened new checks, so this may cause issues

        for item_name in items_to_check:
            if not Logic.is_full_inventory(
                self.logic.requirements,
                self.logic.full_inventory | EXTENDED_ITEM[item_name],
            ):
                return item_name
        return None

    def randomize_nonprogress_items(self):
        # Place unique non-progress items.
        to_place = list(self.must_be_placed_items)
        while to_place:
            accessible_undone_locations = [
                loc
                for loc in self.logic.accessible_checks()
                if loc not in self.logic.placement.locations
            ]

            item_name = self.rng.choice(to_place)

            if not accessible_undone_locations:
                raise Exception("No valid locations left to place non-progress items.")

            location_name = self.rng.choice(accessible_undone_locations)
            self.logic.place_item(location_name, item_name)
            to_place.remove(item_name)

    def randomize_consumable_items(self):
        # Fill remaining unused locations with consumables (Rupees, treasures).

        assert all(
            self.logic.placement.item_placement_limit[item_name] == EIN("")
            for item_name in self.may_be_placed_items
        )
        empty_locations = [
            loc
            for loc in self.logic.accessible_checks()
            if loc not in self.logic.placement.locations
        ]

        to_place = list(self.may_be_placed_items)
        self.rng.shuffle(to_place)
        junk = list(self.randosettings.duplicable_items)
        for location in empty_locations:
            if to_place:
                item = to_place.pop()
            else:
                item = EIN(self.rng.choice(junk))
            result = self.logic.place_item(location, item, fill=False)
            assert result  # Undefined if False

        self.logic.placement.add_unplaced_items(set(to_place))
