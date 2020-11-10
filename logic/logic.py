# taken from https://github.com/LagoLunatic/wwrando/blob/master/logic/logic.py

import yaml
import re
from collections import OrderedDict
import copy
from pathlib import Path

import os

from .item_types import PROGRESS_ITEMS, NONPROGRESS_ITEMS, CONSUMABLE_ITEMS, DUPLICATABLE_CONSUMABLE_ITEMS, DUNGEON_PROGRESS_ITEMS, DUNGEON_NONPROGRESS_ITEMS
from .constants import DUNGEON_NAME_TO_SHORT_DUNGEON_NAME, DUNGEON_NAMES, POTENTIALLY_REQUIRED_DUNGEONS, ALL_TYPES

# TODO, path for logic files will probably be params
ROOT_DIR = Path(__file__).parent.parent

ITEM_WITH_COUNT_REGEX = re.compile(r"^(.+) x(\d+)$")

# the event after dungeons break with a map that triggers the fi text
# until that's removed, make sure the map can't appear there
MAP_BANNED_LOCATIONS = [
  'Skyview - Ruby Tablet',
  'Earth Temple - Amber Tablet',
  'Lanayru Mining Facility - Harp',
  'Ancient Cistern - Goddess Longsword',
  "Sandship - Nayru's Flame",
  "Fire Sanctuary - Din's Flame"
]

class Logic:
  # PROGRESS_ITEM_GROUPS = OrderedDict([
  #   ("Triforce Shards",  [
  #     "Triforce Shard 1",
  #     "Triforce Shard 2",
  #     "Triforce Shard 3",
  #     "Triforce Shard 4",
  #     "Triforce Shard 5",
  #     "Triforce Shard 6",
  #     "Triforce Shard 7",
  #     "Triforce Shard 8",
  #   ]),
  #   ("Goddess Pearls",  [
  #     "Nayru's Pearl",
  #     "Din's Pearl",
  #     "Farore's Pearl",
  #   ]),
  #   ("Tingle Statues",  [
  #     "Dragon Tingle Statue",
  #     "Forbidden Tingle Statue",
  #     "Goddess Tingle Statue",
  #     "Earth Tingle Statue",
  #     "Wind Tingle Statue",
  #   ]),
  # ])
  
  def __init__(self, rando):
    self.rando = rando
    
    
    # Initialize location related attributes.
    self.item_locations = Logic.load_and_parse_item_locations()
    self.load_and_parse_macros()
    
    self.locations_by_zone_name = OrderedDict()
    for location_name in self.item_locations:
      zone_name, specific_location_name = self.split_location_name_by_zone(location_name)
      if zone_name not in self.locations_by_zone_name:
        self.locations_by_zone_name[zone_name] = []
      self.locations_by_zone_name[zone_name].append(location_name)
    
    self.remaining_item_locations = list(self.item_locations.keys())
    self.prerandomization_item_locations = OrderedDict()
    
    self.done_item_locations = OrderedDict()
    for location_name in self.item_locations:
      self.done_item_locations[location_name] = None
    
    
    # Sync the logic macros with the randomizer.
    self.update_entrance_connection_macros()
    self.update_beat_game_macro()
    
    
    # Initialize item related attributes.
    self.all_progress_items = PROGRESS_ITEMS.copy()
    self.all_nonprogress_items = NONPROGRESS_ITEMS.copy()
    self.all_fixed_consumable_items = CONSUMABLE_ITEMS.copy()
    self.duplicatable_consumable_items = DUPLICATABLE_CONSUMABLE_ITEMS.copy()
  
    
    self.all_progress_items += DUNGEON_PROGRESS_ITEMS
    self.all_nonprogress_items += DUNGEON_NONPROGRESS_ITEMS
    
    all_item_names = []
    all_item_names += self.all_progress_items
    all_item_names += self.all_nonprogress_items
    all_item_names += self.all_fixed_consumable_items
    all_item_names += self.duplicatable_consumable_items
    self.all_item_names = all_item_names
    
    self.unplaced_progress_items = self.all_progress_items.copy()
    self.unplaced_nonprogress_items = self.all_nonprogress_items.copy()
    self.unplaced_fixed_consumable_items = self.all_fixed_consumable_items.copy()
    
    self.currently_owned_items = []
    
    for item_name in self.rando.starting_items:
      self.add_owned_item(item_name)
    
    self.make_useless_progress_items_nonprogress()
    
    self.cached_enemies_tested_for_req_string = OrderedDict()
  
  # main randomization method
  def randomize_items(self):
    # collect all items that aren't supposed to be randomized
    for location_name, item in self.item_locations.items():
      item_name = item['original item']
      if item_name == 'Gratitude Crystal':
        self.set_prerandomization_item_location(location_name, item_name)
    self.randomize_dungeon_items()
    self.randomize_progression_items()
    self.randomize_nonprogress_items()
    self.randomize_consumable_items()

  def set_location_to_item(self, location_name, item_name):
    #print("Setting %s to %s" % (location_name, item_name))
    
    if self.done_item_locations[location_name]:
      raise Exception("Location was used twice: " + location_name)
    
    self.done_item_locations[location_name] = item_name
    self.remaining_item_locations.remove(location_name)
    
    self.add_owned_item(item_name)
  
  def set_prerandomization_item_location(self, location_name, item_name):
    # Temporarily keep track of where certain items are placed before the main progression item randomization loop starts.
    
    #print("Setting prerand %s to %s" % (location_name, item_name))
    
    assert location_name in self.item_locations
    self.prerandomization_item_locations[location_name] = item_name
  
  def get_num_progression_items(self):
    return len(self.unplaced_progress_items)
  
  def get_num_progression_locations(self):
    return Logic.get_num_progression_locations_static(self.item_locations, self.rando.banned_types)
  
  @staticmethod
  def get_num_progression_locations_static(item_locations, banned_types):
    progress_locations = Logic.filter_locations_for_progression_static(
      item_locations.keys(),
      item_locations,
      banned_types,
    )
    
    return len(progress_locations)
  
  def get_progress_and_non_progress_locations(self):
    all_locations = self.item_locations.keys()
    progress_locations = self.filter_locations_for_progression(all_locations)
    nonprogress_locations = []
    for location_name in all_locations:
      if location_name in progress_locations:
        continue
      
      nonprogress_locations.append(location_name)
    
    return (progress_locations, nonprogress_locations)
  
  def add_owned_item(self, item_name):
    cleaned_item_name = item_name
    if cleaned_item_name not in self.all_item_names:
      raise Exception("Unknown item name: " + item_name)
    
    else:
      self.currently_owned_items.append(cleaned_item_name)
    
    if item_name in self.unplaced_progress_items:
      self.unplaced_progress_items.remove(item_name)
    elif item_name in self.unplaced_nonprogress_items:
      self.unplaced_nonprogress_items.remove(item_name)
    elif item_name in self.unplaced_fixed_consumable_items:
      self.unplaced_fixed_consumable_items.remove(item_name)
  
  def remove_owned_item(self, item_name):
    cleaned_item_name = item_name
    if cleaned_item_name not in self.all_item_names:
      raise Exception("Unknown item name: " + item_name)
    
    else:
      self.currently_owned_items.remove(cleaned_item_name)
    
    if item_name in self.all_progress_items:
      self.unplaced_progress_items.append(item_name)
    elif item_name in self.all_nonprogress_items:
      self.unplaced_nonprogress_items.append(item_name)
    else:
      # Removing consumable items doesn't work because we don't know if the item is from the fixed list or the duplicatable list
      raise Exception("Cannot remove item from simulated inventory: %s" % item_name)
  
  def get_accessible_remaining_locations(self, for_progression=False):
    accessible_location_names = []
    
    locations_to_check = self.remaining_item_locations
    if for_progression:
      locations_to_check = self.filter_locations_for_progression(locations_to_check)
    
    for location_name in locations_to_check:
      requirement_expression = self.item_locations[location_name]["Need"]
      if self.check_logical_expression_req(requirement_expression):
        accessible_location_names.append(location_name)
    return accessible_location_names
  
  def get_first_useful_item(self, items_to_check):
    # Searches through a given list of items and returns the first one that opens up at least 1 new location.
    # The randomizer shuffles the list before passing it to this function, so in effect it picks a random useful item.
    
    accessible_undone_locations = self.get_accessible_remaining_locations(for_progression=True)
    inaccessible_undone_item_locations = []
    locations_to_check = self.remaining_item_locations
    locations_to_check = self.filter_locations_for_progression(locations_to_check)
    for location_name in locations_to_check:
      if location_name not in accessible_undone_locations:
        inaccessible_undone_item_locations.append(location_name)
    
    # Cache whether each item is useful in order to avoid an absurd number of duplicate recursive calls when checking if a predetermined dungeon item location has a useful item or not.
    self.cached_items_are_useful = {}
    
    for item_name in items_to_check:
      if self.check_item_is_useful(item_name, inaccessible_undone_item_locations):
        self.cached_items_are_useful = None
        return item_name
    
    self.cached_items_are_useful = None
    
    return None
  
  def get_items_by_usefulness_fraction(self, item_names_to_check):
    # Takes a list of items and locations, and determines for each item what the lowest number of items including it the player needs before a new location is opened up, and returns that in a dict.
    # For example, say there are 3 items A B and C, and 2 locations X and Y.
    # Location X requires items A and B while location Y requires items A B and C.
    # This function would return {A: 2, B: 2, C: 3} because A requires 1 other item (B) to help access anything, B also requires one other item (A) to help access anything, but C requires 2 other items (both A and B) before it becomes useful.
    # In other words, items A and B have 1/2 usefulness, while item C has 1/3 usefulness.
    # In addition to the usefulness, we also return the number of locations that this item can potentially unlock (not necessarely immediately)
    # We will multiply that number to the usefulness fraction. This is to make sure the game choses to place items that unlock a lot of locations even if we're far from unlocking those yet
    # Doing this fixes some randomization failures (for exemple we often want the rando to place key pieces rather than song of the hero parts even if we're far from having all key pieces)
    
    accessible_undone_locations = self.get_accessible_remaining_locations(for_progression=True)
    inaccessible_undone_item_locations = []
    locations_to_check = self.remaining_item_locations
    locations_to_check = self.filter_locations_for_progression(locations_to_check)
    for location_name in locations_to_check:
      if location_name not in accessible_undone_locations:
        if location_name in self.rando.race_mode_banned_locations:
          # Don't consider locations inside unchosen dungeons in race mode when calculating usefulness.
          continue
        if location_name in self.prerandomization_item_locations:
          # We just ignore items with predetermined items when calculating usefulness fractions.
          # TODO: In the future, we might want to consider recursively checking if the item here is useful, and if so include this location.
          continue
        inaccessible_undone_item_locations.append(location_name)
    
    # Generate a list of what items are needed for each inaccessible location (+beating the game).
    # Note: Performance could be improved somewhat by only calculating which items are needed for each location at the start of item randomization, instead of once per call to this function. But this seems unnecessary.
    item_names_for_all_locations = []
    for location_name in inaccessible_undone_item_locations:
      requirement_expression = self.item_locations[location_name]["Need"]
      item_names_for_loc = self.get_item_names_from_logical_expression_req(requirement_expression)
      item_names_for_all_locations.append(item_names_for_loc)
    item_names_to_beat_game = self.get_item_names_by_req_name("Can Reach and Defeat Demise")
    item_names_for_all_locations.append(item_names_to_beat_game)
    
    # Now calculate the best case scenario usefulness fraction for all items given.
    item_by_usefulness_fraction = OrderedDict()
    location_count_unlocked_by_items = OrderedDict()
    for item_name in item_names_to_check:
      item_by_usefulness_fraction[item_name] = 9999
      location_count_unlocked_by_items[item_name] = 0
    
    for item_names_for_loc in item_names_for_all_locations:
      item_names_for_loc_without_owned = item_names_for_loc.copy()
      for item_name in self.currently_owned_items:
        if item_name in item_names_for_loc_without_owned:
          item_names_for_loc_without_owned.remove(item_name)
      
      for item_name in item_names_for_loc_without_owned:
        if item_name not in item_by_usefulness_fraction:
          continue
        usefulness_fraction_for_item = len(item_names_for_loc_without_owned)
        location_count_unlocked_by_items[item_name] += 1
        if usefulness_fraction_for_item < item_by_usefulness_fraction[item_name]:
          item_by_usefulness_fraction[item_name] = usefulness_fraction_for_item
    return item_by_usefulness_fraction, location_count_unlocked_by_items
  
  def get_all_useless_items(self, items_to_check):
    # Searches through a given list of items and returns which of them do not open up even 1 new location.
    
    if len(items_to_check) == 0:
      return []
    
    accessible_undone_locations = self.get_accessible_remaining_locations(for_progression=True)
    inaccessible_undone_item_locations = []
    locations_to_check = self.remaining_item_locations
    locations_to_check = self.filter_locations_for_progression(locations_to_check)
    for location_name in locations_to_check:
      if location_name not in accessible_undone_locations:
        inaccessible_undone_item_locations.append(location_name)
    
    self.cached_items_are_useful = {}
    
    useless_items = []
    for item_name in items_to_check:
      if not self.check_item_is_useful(item_name, inaccessible_undone_item_locations):
        useless_items.append(item_name)
    
    self.cached_items_are_useful = None
    
    return useless_items
  
  def check_item_is_useful(self, item_name, inaccessible_undone_item_locations):
    # Checks whether a specific item unlocks any new locations or not.
    # This function should only be called by get_first_useful_item, get_all_useless_items, or by itself for recursion purposes.
    
    if item_name in self.cached_items_are_useful:
      return self.cached_items_are_useful[item_name]
    
    self.add_owned_item(item_name)
    
    for location_name in inaccessible_undone_item_locations:
      if location_name in self.rando.race_mode_banned_locations:
        # Don't consider locations inside unchosen dungeons in race mode when calculating usefulness.
        continue
      
      if location_name in self.prerandomization_item_locations:
        # If this location has a predetermined item in it, we need to recursively check if that item is useful.
        unlocked_prerand_item = self.prerandomization_item_locations[location_name]
        # Need to exclude the current location from recursive checks to prevent infinite recursion.
        temp_inaccessible_undone_item_locations = [
          loc for loc in inaccessible_undone_item_locations
          if not loc == location_name
        ]
        if not self.check_item_is_useful(unlocked_prerand_item, temp_inaccessible_undone_item_locations):
          # If that item is not useful, don't consider the current item useful for unlocking it.
          continue
        
        requirement_expression = self.item_locations[location_name]["Need"]
        if self.check_logical_expression_req(requirement_expression):
          self.remove_owned_item(item_name)
          self.cached_items_are_useful[item_name] = True
          return True
      
      requirement_expression = self.item_locations[location_name]["Need"]
      if self.check_logical_expression_req(requirement_expression):
        self.remove_owned_item(item_name)
        self.cached_items_are_useful[item_name] = True
        return True
    
    self.remove_owned_item(item_name)
    self.cached_items_are_useful[item_name] = False
    return False
  
  def filter_locations_for_progression(self, locations_to_filter):
    return Logic.filter_locations_for_progression_static(
      locations_to_filter,
      self.item_locations,
      self.rando.banned_types,
    )
  
  @staticmethod
  def filter_locations_for_progression_static(locations_to_filter, item_locations, banned_types):
    filtered_locations = []
    for location_name in locations_to_filter:
      types: set = item_locations[location_name]["type"]
      if types.isdisjoint(banned_types):
        filtered_locations.append(location_name)
    
    return filtered_locations
  
  def check_item_valid_in_location(self, item_name, location_name):
    # Don't allow dungeon items to appear outside their proper dungeon when Key-Lunacy is off.
    if self.is_dungeon_item(item_name) and not self.rando.options.get("keylunacy"):
      short_dungeon_name = item_name.split(" ")[0]
      dungeon_name = DUNGEON_NAMES[short_dungeon_name]
      if not self.is_dungeon_location(location_name, dungeon_name_to_match=dungeon_name):
        return False
    
    # ban maps in events where it breaks things
    if item_name.endswith('Map') and location_name in MAP_BANNED_LOCATIONS:
      return False
    return True
  
  def filter_items_by_any_valid_location(self, items, locations):
    # Filters out items that cannot be in any of the given possible locations.
    valid_items = []
    for item_name in items:
      for location_name in locations:
        if self.check_item_valid_in_location(item_name, location_name):
          valid_items.append(item_name)
          break
    return valid_items
  
  def filter_locations_valid_for_item(self, locations, item_name):
    valid_locations = []
    for location_name in locations:
      if self.check_item_valid_in_location(item_name, location_name):
        valid_locations.append(location_name)
    return valid_locations
  
  def filter_items_valid_for_location(self, items, location_name):
    valid_items = []
    for item_name in items:
      if self.check_item_valid_in_location(item_name, location_name):
        valid_items.append(item_name)
    return valid_items
  
  @staticmethod
  def load_and_parse_item_locations():
    with (ROOT_DIR / "SS Rando Logic - Item Location.yaml").open('r') as f:
      item_locations = yaml.load(f, YamlOrderedDictLoader)
    
    for location_name in item_locations:
      req_string = item_locations[location_name]["Need"]
      if req_string is None:
        # TODO, blank reqs should be an error. Temporarily we will just consider them to be impossible.
        item_locations[location_name]["Need"] = Logic.parse_logic_expression("TODO")
      else:
        item_locations[location_name]["Need"] = Logic.parse_logic_expression(req_string)
      
      if not "type" in item_locations[location_name]:
        print("ERROR, "+location_name+" doesn't have types!")
      types_string = item_locations[location_name]["type"]
      types = types_string.split(",")
      types = set((type.strip() for type in types))
      unknown_types = [x for x in types if not x in ALL_TYPES]
      if len(unknown_types) != 0:
        raise Exception(f"unknown types: {unknown_types}")
      item_locations[location_name]["type"] = types
    
    return item_locations
    
  def load_and_parse_macros(self):
    with (ROOT_DIR / "SS Rando Logic - Macros.yaml").open('r') as f:
      macro_strings = yaml.safe_load(f)
    self.macros = {}
    for macro_name, req_string in macro_strings.items():
      self.set_macro(macro_name, req_string)
  
  def set_macro(self, macro_name, req_string):
    self.macros[macro_name] = Logic.parse_logic_expression(req_string)
  
  def update_beat_game_macro(self):
    # needs to be able to open GoT and open it, requires required dungeons
    access_past_requirements = ['Can Access Sealed Temple', 'Master Sword','Can Raise Gate of Time']
    for dungeon in self.rando.required_dungeons:
      access_past_requirements.append(f'Can Beat {dungeon}')
    ' & '.join(f'Can Beat {dungeon}' for dungeon in self.rando.required_dungeons)
    self.set_macro('Can Access Past',' & '.join(access_past_requirements))

  def update_entrance_connection_macros(self):
    # Update all the macros to take randomized entrances into account.
    for entrance_name, zone_name in self.rando.entrance_connections.items():
      zone_access_macro_name = "Can Access " + zone_name
      entrance_access_macro_name = "Can Access " + entrance_name
      self.set_macro(zone_access_macro_name, entrance_access_macro_name)
  
  def temporarily_make_dungeon_entrance_macros_impossible(self):
    # Update all the dungeon access macros to be considered "Impossible".
    # Useful when the item randomizer is deciding how to place keys in DRC.
    pass #TODO: entrance rando
    # for zone_exit in entrances.DUNGEON_EXITS:
    #   dungeon_access_macro_name = "Can Access " + zone_exit.unique_name
    #   self.set_macro(dungeon_access_macro_name, "Impossible")
  
  def temporarily_make_entrance_macros_impossible(self):
    # Update all the dungeon/secret cave access macros to be considered "Impossible".
    # Useful when the entrance randomizer is selecting which dungeons/secret caves should be allowed where.
    pass #TODO: entrance rando
    # for entrance_name, zone_name in self.rando.entrance_connections.items():
    #   zone_access_macro_name = "Can Access " + zone_name
    #   self.set_macro(zone_access_macro_name, "Impossible")
  
  def temporarily_make_entrance_macros_worst_case_scenario(self):
    # Update all the dungeon/secret cave access macros to be a combination of all the macros for accessing dungeons/secret caves that can have their entrance randomized.
    
    pass #TODO: entrance rando
    # if self.rando.options.get("randomize_entrances") == "Dungeons":
    #   self.temporarily_make_one_set_of_entrance_macros_worst_case_scenario(include_dungeons=True, include_caves=False)
    # elif self.rando.options.get("randomize_entrances") == "Secret Caves":
    #   self.temporarily_make_one_set_of_entrance_macros_worst_case_scenario(include_dungeons=False, include_caves=True)
    # elif self.rando.options.get("randomize_entrances") == "Dungeons & Secret Caves (Separately)":
    #   self.temporarily_make_one_set_of_entrance_macros_worst_case_scenario(include_dungeons=True, include_caves=False)
    #   self.temporarily_make_one_set_of_entrance_macros_worst_case_scenario(include_dungeons=False, include_caves=True)
    # elif self.rando.options.get("randomize_entrances") == "Dungeons & Secret Caves (Together)":
    #   self.temporarily_make_one_set_of_entrance_macros_worst_case_scenario(include_dungeons=True, include_caves=True)
    # else:
    #   raise Exception("Invalid entrance randomizer option: %s" % self.rando.options.get("randomize_entrances"))
  
  def temporarily_make_one_set_of_entrance_macros_worst_case_scenario(self, include_dungeons=False, include_caves=False):
    pass #TODO: entrance rando
    # relevant_entrances = []
    # zones = []
    # if include_dungeons:
    #   relevant_entrances += entrances.DUNGEON_ENTRANCES
    #   zones += entrances.DUNGEON_EXITS
    # if include_caves:
    #   relevant_entrances += entrances.SECRET_CAVE_ENTRANCES
    #   zones += entrances.SECRET_CAVE_EXITS
    
    # all_entrance_access_macro_names = []
    # for entrance in relevant_entrances:
    #   entrance_access_macro_name = "Can Access " + entrance.entrance_name
    #   all_entrance_access_macro_names.append(entrance_access_macro_name)
    # can_access_all_entrances = " & ".join(all_entrance_access_macro_names)
    # for zone in zones:
    #   zone_access_macro_name = "Can Access " + zone.unique_name
    #   self.set_macro(zone_access_macro_name, can_access_all_entrances)
  
  def make_useless_progress_items_nonprogress(self):
    # Detect which progress items don't actually help access any locations with the user's current settings, and move those over to the nonprogress item list instead.
    # This is so things like dungeons-only runs don't have a lot of useless items hogging the progress locations.
    
    if self.rando.options.get("randomize_entrances") not in ["Disabled", None]:
      # Since the randomizer hasn't decided which dungeon/secret cave will be where yet, we have to assume the worst case scenario by considering that you need to be able to access all dungeon/secret cave entrances in order to access each individual one.
      self.temporarily_make_entrance_macros_worst_case_scenario()
  
    progress_locations = Logic.filter_locations_for_progression_static(
      self.item_locations.keys(),
      self.item_locations,
      self.rando.banned_types,
    )
    
    useful_items = []
    for location_name in progress_locations:
      requirement_expression = self.item_locations[location_name]["Need"]
      useful_items += self.get_item_names_from_logical_expression_req(requirement_expression)
    useful_items += self.get_item_names_by_req_name("Can Reach and Defeat Demise")
    
    all_progress_items_filtered = []
    for item_name in useful_items:
      if item_name == "Progressive Sword" and self.rando.options.get("sword_mode") == "Swordless":
        continue
      # if self.is_dungeon_item(item_name) and not self.rando.options.get("progression_dungeons"):
      #   continue
      if item_name not in self.all_progress_items:
        if not (item_name.startswith("Triforce Chart ") or item_name.startswith("Treasure Chart")):
          raise Exception("Item %s opens up progress locations but is not in the list of all progress items." % item_name)
      if item_name in all_progress_items_filtered:
        # Avoid duplicates
        continue
      all_progress_items_filtered.append(item_name)
    
    items_to_make_nonprogress = [
      item_name for item_name in self.all_progress_items
      if item_name not in all_progress_items_filtered
      and item_name not in self.currently_owned_items
    ]
    for item_name in items_to_make_nonprogress:
      #print(item_name)
      self.all_progress_items.remove(item_name)
      self.all_nonprogress_items.append(item_name)
      self.unplaced_progress_items.remove(item_name)
      self.unplaced_nonprogress_items.append(item_name)
    
    if self.rando.options.get("randomize_entrances") not in ["Disabled", None]:
      # Reset the dungeon/secret cave access macros if we changed them earlier.
      self.update_entrance_connection_macros()
  
  @staticmethod
  def split_location_name_by_zone(location_name):
    if " - " in location_name:
      zone_name, specific_location_name = location_name.split(" - ", 1)
    else:
      zone_name = specific_location_name = location_name
    
    return zone_name, specific_location_name
  
  def is_dungeon_item(self, item_name):
    return (item_name in DUNGEON_PROGRESS_ITEMS or item_name in DUNGEON_NONPROGRESS_ITEMS)
  
  def is_dungeon_location(self, location_name, dungeon_name_to_match=None):
    zone_name, specific_location_name = self.split_location_name_by_zone(location_name)
    if zone_name not in DUNGEON_NAME_TO_SHORT_DUNGEON_NAME:
      # Not a dungeon.
      return False
    if dungeon_name_to_match and dungeon_name_to_match != zone_name:
      # Wrong dungeon.
      return False
    return True
  
  @staticmethod
  def parse_logic_expression(string):
    tokens = [str.strip() for str in re.split("([&|()])", string)]
    tokens = [token for token in tokens if token != ""]
    
    stack = []
    for token in tokens:
      if token == "(":
        stack.append("(")
      elif token == ")":
        nested_tokens = []
        
        nested_parentheses_level = 0
        while len(stack) != 0:
          exp = stack.pop()
          if exp == "(":
            if nested_parentheses_level == 0:
              break
            else:
              nested_parentheses_level -= 1
          if exp == ")":
            nested_parentheses_level += 1
          nested_tokens.append(exp)
        
        nested_tokens.reverse()
        stack.append("(")
        stack.append(nested_tokens)
        stack.append(")")
      else:
        stack.append(token)
    
    return stack
  
  def check_requirement_met(self, req_name):
    match = ITEM_WITH_COUNT_REGEX.match(req_name)
    if match:
      item_name = match.group(1)
      num_required = int(match.group(2))
      
      num_owned = self.currently_owned_items.count(item_name)
      return num_owned >= num_required
    elif req_name.startswith("Can Access Other Location \""):
      return self.check_other_location_requirement(req_name)
    elif req_name.startswith("Option \""):
      return self.check_option_enabled_requirement(req_name)
    elif req_name in self.all_item_names:
      return req_name in self.currently_owned_items
    elif req_name in self.macros:
      logical_expression = self.macros[req_name]
      return self.check_logical_expression_req(logical_expression)
    elif req_name == "Nothing":
      return True
    elif req_name == "Impossible":
      return False
    else:
      raise Exception("Unknown requirement name: " + req_name)
      # print("Unknown requirement name: " + req_name)
      # return True
  
  def check_logical_expression_string_req(self, logical_expression_str):
    return self.check_logical_expression_req(Logic.parse_logic_expression(logical_expression_str))

  def check_logical_expression_req(self, logical_expression):
    expression_type = None
    subexpression_results = []
    tokens = logical_expression.copy()
    tokens.reverse()
    while tokens:
      token = tokens.pop()
      if token == "|":
        if expression_type == "AND":
          raise Exception("Error parsing progression requirements: & and | must not be within the same nesting level.")
        expression_type = "OR"
      elif token == "&":
        if expression_type == "OR":
          raise Exception("Error parsing progression requirements: & and | must not be within the same nesting level.")
        expression_type = "AND"
      elif token == "(":
        nested_expression = tokens.pop()
        if nested_expression == "(":
          # Nested parentheses
          nested_expression = ["("] + tokens.pop()
        result = self.check_logical_expression_req(nested_expression)
        subexpression_results.append(result)
        assert tokens.pop() == ")"
      else:
        # Subexpression.
        result = self.check_requirement_met(token)
        subexpression_results.append(result)
    
    if expression_type == "OR":
      return any(subexpression_results)
    else:
      return all(subexpression_results)
  
  def get_item_names_by_req_name(self, req_name):
    items_needed = self.get_items_needed_by_req_name(req_name)
    return self.flatten_items_needed_to_item_names(items_needed)
  
  def get_item_names_from_logical_expression_req(self, logical_expression):
    items_needed = self.get_items_needed_from_logical_expression_req(logical_expression)
    return self.flatten_items_needed_to_item_names(items_needed)
  
  def flatten_items_needed_to_item_names(self, items_needed):
    item_names = []
    for item_name, num_required in items_needed.items():
      item_names += [item_name]*num_required
    return item_names
  
  def get_items_needed_by_req_name(self, req_name):
    items_needed = OrderedDict()
    match = ITEM_WITH_COUNT_REGEX.match(req_name)
    if match:
      item_name = match.group(1)
      num_required = int(match.group(2))
      
      items_needed[item_name] = max(num_required, items_needed.setdefault(item_name, 0))
    elif req_name.startswith("Can Access Other Location \""):
      match = re.search(r"^Can Access Other Location \"([^\"]+)\"$", req_name)
      other_location_name = match.group(1)
      requirement_expression = self.item_locations[other_location_name]["Need"]
      sub_items_needed = self.get_items_needed_from_logical_expression_req(requirement_expression)
      for item_name, num_required in sub_items_needed.items():
        items_needed[item_name] = max(num_required, items_needed.setdefault(item_name, 0))
    elif req_name.startswith("Option \""):
      pass
    elif req_name in self.all_item_names:
      items_needed[req_name] = max(1, items_needed.setdefault(req_name, 0))
    elif req_name in self.macros:
      logical_expression = self.macros[req_name]
      sub_items_needed = self.get_items_needed_from_logical_expression_req(logical_expression)
      for item_name, num_required in sub_items_needed.items():
        items_needed[item_name] = max(num_required, items_needed.setdefault(item_name, 0))
    elif req_name == "Nothing":
      pass
    elif req_name == "Impossible":
      pass
    else:
      # print("Unknown requirement name: " + req_name)
      raise Exception("Unknown requirement name: " + req_name)
    
    return items_needed
  
  def get_items_needed_from_logical_expression_req(self, logical_expression):
    if self.check_logical_expression_req(logical_expression):
      # If this expression is already satisfied, we don't want to include any other items in the OR statement.
      return OrderedDict()
    
    items_needed = OrderedDict()
    tokens = logical_expression.copy()
    tokens.reverse()
    while tokens:
      token = tokens.pop()
      if token == "|":
        pass
      elif token == "&":
        pass
      elif token == "(":
        nested_expression = tokens.pop()
        if nested_expression == "(":
          # Nested parentheses
          nested_expression = ["("] + tokens.pop()
        sub_items_needed = self.get_items_needed_from_logical_expression_req(nested_expression)
        for item_name, num_required in sub_items_needed.items():
          items_needed[item_name] = max(num_required, items_needed.setdefault(item_name, 0))
        assert tokens.pop() == ")"
      else:
        # Subexpression.
        sub_items_needed = self.get_items_needed_by_req_name(token)
        for item_name, num_required in sub_items_needed.items():
          items_needed[item_name] = max(num_required, items_needed.setdefault(item_name, 0))
    
    return items_needed
  
  # def check_progressive_item_req(self, req_name):
  #   match = re.search(r"^(Progressive .+) x(\d+)$", req_name)
  #   item_name = match.group(1)
  #   num_required = int(match.group(2))
    
  #   num_owned = self.currently_owned_items.count(item_name)
  #   return num_owned >= num_required
  
  # def check_small_key_req(self, req_name):
  #   match = re.search(r"^(.+ Small Key) x(\d+)$", req_name)
  #   small_key_name = match.group(1)
  #   num_keys_required = int(match.group(2))
    
  #   num_small_keys_owned = self.currently_owned_items.count(small_key_name)
  #   return num_small_keys_owned >= num_keys_required
  
  def check_other_location_requirement(self, req_name):
    match = re.search(r"^Can Access Other Location \"([^\"]+)\"$", req_name)
    other_location_name = match.group(1)
    
    requirement_expression = self.item_locations[other_location_name]["Need"]
    return self.check_logical_expression_req(requirement_expression)
  
  def check_option_enabled_requirement(self, req_name):
    positive_boolean_match = re.search(r"^Option \"([^\"]+)\" Enabled$", req_name)
    negative_boolean_match = re.search(r"^Option \"([^\"]+)\" Disabled$", req_name)
    positive_dropdown_match = re.search(r"^Option \"([^\"]+)\" Is \"([^\"]+)\"$", req_name)
    negative_dropdown_match = re.search(r"^Option \"([^\"]+)\" Is Not \"([^\"]+)\"$", req_name)
    positive_list_match = re.search(r"^Option \"([^\"]+)\" Contains \"([^\"]+)\"$", req_name)
    negative_list_match = re.search(r"^Option \"([^\"]+)\" Does Not Contain \"([^\"]+)\"$", req_name)
    if positive_boolean_match:
      option_name = positive_boolean_match.group(1)
      return not not self.rando.options.get(option_name)
    elif negative_boolean_match:
      option_name = negative_boolean_match.group(1)
      return not self.rando.options.get(option_name)
    elif positive_dropdown_match:
      option_name = positive_dropdown_match.group(1)
      value = positive_dropdown_match.group(2)
      return self.rando.options.get(option_name) == value
    elif negative_dropdown_match:
      option_name = negative_dropdown_match.group(1)
      value = negative_dropdown_match.group(2)
      return self.rando.options.get(option_name) != value
    elif positive_list_match:
      option_name = positive_list_match.group(1)
      value = positive_list_match.group(2)
      return value in self.rando.options.get(option_name, [])
    elif negative_list_match:
      option_name = negative_list_match.group(1)
      value = negative_list_match.group(2)
      return value not in self.rando.options.get(option_name, [])
    else:
      raise Exception("Invalid option check requirement: %s" % req_name)

  def randomize_progression_items(self):
    accessible_undone_locations = self.get_accessible_remaining_locations(for_progression=True)
    if len(accessible_undone_locations) == 0:
      raise Exception("No progress locations are accessible at the very start of the game!")
    
    # Place progress items.
    location_weights = {}
    current_weight = 1
    while self.unplaced_progress_items:
      accessible_undone_locations = self.get_accessible_remaining_locations(for_progression=True)
      
      if not accessible_undone_locations:
        raise Exception("No locations left to place progress items!")
      
      # If the player gained access to any predetermined item locations, we need to give them those items.
      newly_accessible_predetermined_item_locations = [
        loc for loc in accessible_undone_locations
        if loc in self.prerandomization_item_locations
      ]
      if newly_accessible_predetermined_item_locations:
        for predetermined_item_location_name in newly_accessible_predetermined_item_locations:
          predetermined_item_name = self.prerandomization_item_locations[predetermined_item_location_name]
          self.set_location_to_item(predetermined_item_location_name, predetermined_item_name)
        
        continue # Redo this loop iteration with the predetermined item locations no longer being considered 'remaining'.
      
      for location in accessible_undone_locations:
        if location not in location_weights:
          location_weights[location] = current_weight
        elif location_weights[location] > 1:
          location_weights[location] -= 1
      current_weight += 1
      
      possible_items = self.unplaced_progress_items.copy()
      
      # Don't randomly place items that already had their location predetermined.
      unfound_prerand_locs = [
        loc for loc in self.prerandomization_item_locations
        if loc in self.remaining_item_locations
      ]
      for location_name in unfound_prerand_locs:
        prerand_item = self.prerandomization_item_locations[location_name]
        if prerand_item not in possible_items:
          continue
        possible_items.remove(prerand_item)
      
      if len(possible_items) == 0:
        raise Exception("Only items left to place are predetermined items at inaccessible locations!")
      
      # Filter out items that are not valid in any of the locations we might use.
      possible_items = self.filter_items_by_any_valid_location(possible_items, accessible_undone_locations)
      
      if len(possible_items) == 0:
        raise Exception("No valid locations left for any of the unplaced progress items!")
      
      # Remove duplicates from the list so items like swords and bows aren't so likely to show up early.
      # Don't do this with Eldin Key Pieces or Earth Temple will always be really late in logic. Same with crystals
      unique_possible_items = []
      for item_name in possible_items:
        if item_name not in unique_possible_items:
          unique_possible_items.append(item_name)
        elif item_name == 'Key Piece':
          unique_possible_items.append(item_name)
        elif item_name == '5 Gratitude Crystals':
          unique_possible_items.append(item_name)
        elif item_name == 'Gratitude Crystal':
          unique_possible_items.append(item_name)
      possible_items = unique_possible_items
      
      must_place_useful_item = False
      should_place_useful_item = True
      if len(accessible_undone_locations) == 1 and len(possible_items) > 1:
        # If we're on the last accessible location but not the last item we HAVE to place an item that unlocks new locations.
        # (Otherwise we will still try to place a useful item, but failing will not result in an error.)
        must_place_useful_item = True
      elif len(accessible_undone_locations) >= 8:
        # If we have a lot of locations open, we don't need to be so strict with prioritizing currently useful items.
        # This can give the randomizer a chance to place things like Delivery Bag or small keys for dungeons that need x2 to do anything.
        should_place_useful_item = False

      possible_items_when_not_placing_useful = [name for name in possible_items]      

      # Only exception is when there's exclusively groups left to place. Then we allow groups even if they're not useful.
      if len(possible_items_when_not_placing_useful) == 0 and len(possible_items) > 0:
        possible_items_when_not_placing_useful = possible_items
      
      if must_place_useful_item or should_place_useful_item:
        shuffled_list = possible_items.copy()
        self.rando.rng.shuffle(shuffled_list)
        item_name = self.get_first_useful_item(shuffled_list)
        if item_name is None:
          # This means that no item can unlock a new location
          if must_place_useful_item:
            raise Exception("No useful progress items to place!")
          else:
            # We'd like to be placing a useful item, but there are no immediately useful items to place.
            # Instead we choose an item that isn't useful yet by itself, but has a high usefulness fraction.
            # In other words, which item has the smallest number of other items needed before it becomes useful?
            # We'd prefer to place an item which is 1/2 of what you need to access a new location over one which is 1/5 for example.
            # The number of locations an item can potentially unlock also matters (think key pieces)
          
            item_by_usefulness_fraction, locations_unlocked_by_item = self.get_items_by_usefulness_fraction(possible_items_when_not_placing_useful)
          
            # We want to limit it to choosing items at the maximum usefulness fraction.
            # Since the values we have are the denominator of the fraction, we actually call min() instead of max().
            max_usefulness_num, = item_by_usefulness_fraction.values()
            max_usefulness_denom = locations_unlocked_by_item.values()
            max_usefulness_frac = []
            for i in range(len(max_usefulness_num)):
              max_usefulness_frac.append(max_usefulness_num[i]/max_usefulness_denom[i])
            max_usefulness = min(max_usefulness_frac)
            items_at_max_usefulness = [
              item_name for item_name, usefulness in item_by_usefulness_fraction.items()
              if usefulness == max_usefulness
            ]
            
            item_name = self.rando.rng.choice(items_at_max_usefulness)
      else:
        item_name = self.rando.rng.choice(possible_items_when_not_placing_useful)
      
      locations_filtered = [
        loc for loc in accessible_undone_locations
        if loc not in self.rando.race_mode_banned_locations
      ]
      if len(locations_filtered) >= 1:
        accessible_undone_locations = locations_filtered
      else:
        raise Exception("Failed to prevent progress items from appearing in banned locations!")
      
      possible_locations = self.filter_locations_valid_for_item(accessible_undone_locations, item_name)

      
      # We weight it so newly accessible locations are more likely to be chosen.
      # This way there is still a good chance it will not choose a new location.
      # Dungeons are prefered
      possible_locations_with_weighting = []
      for location_name in possible_locations:
        if self.is_dungeon_location(location_name):
          weight = location_weights[location_name]*2
        else:
          weight = location_weights[location_name]
        possible_locations_with_weighting += [location_name]*weight

      location_name = self.rando.rng.choice(possible_locations_with_weighting)
      self.set_location_to_item(location_name, item_name)

      # continue loop if items are remaining

    # Make sure locations that should have predetermined items in them have them properly placed, even if the above logic missed them for some reason.
    for location_name in self.prerandomization_item_locations:
      if location_name in self.remaining_item_locations:
        dungeon_item_name = self.prerandomization_item_locations[location_name]
        self.set_location_to_item(location_name, dungeon_item_name)
    
    game_beatable = self.check_requirement_met("Can Reach and Defeat Demise")
    if not game_beatable:
      raise Exception("Game is not beatable on this seed! This error shouldn't happen.")
  
  def randomize_dungeon_items(self):
    # Places dungeon-specific items first so all the dungeon locations don't get used up by other items.
    
    # Temporarily add all progress items except for dungeon keys while we randomize them.
    items_to_temporarily_add = [
      item_name for item_name in (self.unplaced_progress_items + self.unplaced_nonprogress_items)
      if not self.is_dungeon_item(item_name)
    ]
    for item_name in items_to_temporarily_add:
      self.add_owned_item(item_name)
    
    
    # Randomize small keys.
    small_keys_to_place = [
      item_name for item_name in (self.unplaced_progress_items + self.unplaced_nonprogress_items)
      if item_name.endswith(" Small Key")
    ]
    assert len(small_keys_to_place) > 0, f'no small '
    for item_name in small_keys_to_place:
      self.place_dungeon_item(item_name)
      self.add_owned_item(item_name) # Temporarily add small keys to the player's inventory while placing them.
    
    # Randomize big keys.
    big_keys_to_place = [
      item_name for item_name in (self.unplaced_progress_items + self.unplaced_nonprogress_items)
      if item_name.endswith(" Boss Key")
    ]
    assert len(big_keys_to_place) > 0
    for item_name in big_keys_to_place:
      self.place_dungeon_item(item_name)
      self.add_owned_item(item_name) # Temporarily add big keys to the player's inventory while placing them.
    
    # Randomize dungeon maps and compasses.
    other_dungeon_items_to_place = [
      item_name for item_name in (self.unplaced_progress_items + self.unplaced_nonprogress_items)
      if item_name.endswith(" Map")
    ]
    assert len(other_dungeon_items_to_place) > 0
    for item_name in other_dungeon_items_to_place:
      self.place_dungeon_item(item_name)
    
    # Remove the items we temporarily added.
    for item_name in items_to_temporarily_add:
      self.remove_owned_item(item_name)
    for item_name in small_keys_to_place:
      self.remove_owned_item(item_name)
    for item_name in big_keys_to_place:
      self.remove_owned_item(item_name)

  def place_dungeon_item(self, item_name):
    accessible_undone_locations = self.get_accessible_remaining_locations()
    accessible_undone_locations = [
      loc for loc in accessible_undone_locations
      if loc not in self.prerandomization_item_locations
    ]
    
    possible_locations = self.filter_locations_valid_for_item(accessible_undone_locations, item_name)
    
    # if self.dungeons_only_start and item_name == "DRC Small Key":
    #   # If we're in a dungeons-only-start, we have to ban small keys from appearing in the path that sequence breaks the hanging platform.
    #   # A key you need to progress appearing there can cause issues that dead-end the item placement logic when there are no locations outside DRC for the randomizer to give you other items at.
    #   possible_locations = [
    #     loc for loc in possible_locations
    #     if not loc in ["Dragon Roost Cavern - Big Key Chest", "Dragon Roost Cavern - Tingle Statue Chest"]
    #   ]
    # if self.dungeons_only_start and item_name in ["DRC Big Key", "DRC Dungeon Map", "DRC Compass"]:
    #   # If we're in a dungeons-only start, we have to ban dungeon items except small keys from appearing in all 6 of the 6 easiest locations to access in DRC.
    #   # If we don't do this, there is a small chance that those 6 locations will be filled with 3 small keys, the dungeon map, and the compass. The 4th small key will be in the path that sequence breaks the hanging platform, but there will be no open spots to put any non-dungeon items like grappling hook.
    #   # To prevent this specific problem, one location (chosen randomly) is not allowed to have these items at all in dungeons-only-start. It can still have small keys and non-dungeon items.
    #   possible_locations = [
    #     loc for loc in possible_locations
    #     if loc != self.drc_failsafe_location
    #   ]
    
    if not possible_locations:
      raise Exception(f"No valid locations left to place dungeon item {item_name}!")
    
    location_name = self.rando.rng.choice(possible_locations)
    self.set_prerandomization_item_location(location_name, item_name)

  def randomize_nonprogress_items(self):
    # Place unique non-progress items.
    while self.unplaced_nonprogress_items:
      accessible_undone_locations = self.get_accessible_remaining_locations()
      
      item_name = self.rando.rng.choice(self.unplaced_nonprogress_items)
      
      possible_locations = self.filter_locations_valid_for_item(accessible_undone_locations, item_name)
      
      if not possible_locations:
        raise Exception("No valid locations left to place non-progress items!")
      
      location_name = self.rando.rng.choice(possible_locations)
      self.set_location_to_item(location_name, item_name)
    
  def randomize_consumable_items(self):
    accessible_undone_locations = self.get_accessible_remaining_locations()
    inaccessible_locations = [loc for loc in self.remaining_item_locations if loc not in accessible_undone_locations]
    if inaccessible_locations:
      print("Inaccessible locations:")
      for location_name in inaccessible_locations:
        print(location_name)
    
    # Fill remaining unused locations with consumables (Rupees, treasures).
    locations_to_place_consumables_at = self.remaining_item_locations.copy()
    for location_name in locations_to_place_consumables_at:
      possible_items = self.filter_items_valid_for_location(self.unplaced_fixed_consumable_items, location_name)
      if len(possible_items) == 0:
        possible_items = self.filter_items_valid_for_location(self.duplicatable_consumable_items, location_name)
        if len(possible_items) == 0:
          raise Exception("No valid consumable items for location %s" % location_name)
      
      item_name = self.rando.rng.choice(possible_items)
      self.set_location_to_item(location_name, item_name)

class YamlOrderedDictLoader(yaml.SafeLoader):
  pass

YamlOrderedDictLoader.add_constructor(
  yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
  lambda loader, node: OrderedDict(loader.construct_pairs(node))
)
