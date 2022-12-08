from collections import OrderedDict
from typing import TextIO
from hints.hint_types import GossipStoneHintWrapper
from options import OPTIONS, Options
import itertools

from version import VERSION
from logic.constants import DUNGEON_GOALS, DEMISE


def write(file: TextIO, options: Options, logic, hints, sots_locations, hash):
    write_header(file, options, hash)

    if options["no-spoiler-log"]:
        return

    if len(logic.starting_items) > 0:
        file.write("\n\nStarting items:\n  ")
        file.write("\n  ".join(sorted(logic.starting_items)))
    file.write("\n\n\n")

    # Write required dungeons
    for i, dungeon in enumerate(logic.required_dungeons, start=1):
        file.write(f"Required Dungeon {i}: {dungeon}\n")

    file.write("\n\n")

    # Write spirit of the sword (100% required) locations
    file.write("SotS:\n")

    for loc, item in sots_locations[DEMISE]:
        location = loc + ":"
        file.write(f"  {location:53} {item}\n")

    file.write("\n\n")

    # Write path locations; locations 100% required to complete a given required dungeon
    file.write("Path:\n")
    for dungeon in logic.required_dungeons:
        goal = DUNGEON_GOALS[dungeon]
        file.write(f"{goal}:\n")
        for loc, item in sots_locations[goal]:
            location = loc + ":"
            file.write(f"  {location:53} {item}\n")

    file.write("\n\n")

    barren, nonprogress = logic.get_barren_regions()
    file.write("Barren Regions:\n")
    for region in barren:
        file.write("  " + region + "\n")
    file.write("\n\n")

    file.write("Nonprogress Regions:\n")
    for region in nonprogress:
        file.write("  " + region + "\n")
    file.write("\n\n")

    # Write progression spheres.
    file.write("Playthrough:\n")
    prettified_spheres = []
    # First pass for the lengths
    for sphere in logic.calculate_playthrough_progression_spheres():
        pretty_sphere = []
        for loc in sphere:
            if loc == "Past - Demise":
                pretty_sphere.append(("Past", "Demise", "End Credits"))
            elif (item := logic.done_item_locations[loc]) != "Gratitude Crystal":
                hint_region, loc = logic.split_location_name_by_zone(loc)
                pretty_sphere.append((hint_region, loc, item))
        prettified_spheres.append(pretty_sphere)

    max_location_name_length = 1 + max(
        len(loc) for sphere in prettified_spheres for _, loc, _ in sphere
    )

    for i, progression_sphere in enumerate(prettified_spheres, start=1):
        file.write(f"{i}\n")

        for zone_name, locations_in_zone in itertools.groupby(
            progression_sphere, lambda x: x[0]
        ):
            file.write(f"  {zone_name}:\n")

            for _, loc, item in locations_in_zone:
                file.write(f"      {loc + ':':{max_location_name_length}} {item}\n")

    file.write("\n\n\n")

    # Write item locations.
    file.write("All item locations:\n")

    with_regions = [
        (*logic.split_location_name_by_zone(loc), item)
        for loc, item in logic.done_item_locations.items()
        if item != "Gratitude Crystal"
    ]

    max_location_name_length = 1 + max(len(loc) for _, loc, _ in with_regions)

    for zone_name, locations_in_zone in itertools.groupby(with_regions, lambda x: x[0]):
        file.write(zone_name + ":\n")
        for _, loc, item in locations_in_zone:
            file.write(f"    {loc + ':':{max_location_name_length}} {item}\n")

    file.write("\n\n\n")

    # Write dungeon entrances.
    file.write("Entrances:\n")
    for (
        entrance_name,
        dungeon,
    ) in logic.entrance_connections.items():
        file.write(f"  {entrance_name+':':48} {dungeon}\n")

    file.write("\n\n")

    # Write randomized trials
    file.write("Trial Gates:\n")
    for trial_gate, trial in logic.trial_connections.items():
        file.write(f"  {trial_gate+':':48} {trial}\n")

    file.write("\n\n\n")

    # Write hints
    file.write("Hints:\n")
    for hintloc, hint in hints.items():
        hint_stone = hints[hintloc]
        if isinstance(hint_stone, GossipStoneHintWrapper):
            file.write(f"  {hintloc+':'}\n")
            for hint in hint_stone.hints:
                file.write(f"  {'':48} {hint.to_spoiler_log_text()}\n")
        else:
            file.write(f"  {hintloc+':':48} {hint_stone.to_spoiler_log_text()}\n")

    file.write("\n\n\n")


def dump_json(options: Options, logic, hints, sots_locations, hash):
    spoiler_log = dump_header_json(options, hash)
    if options["no-spoiler-log"]:
        return spoiler_log
    spoiler_log["starting-items"] = sorted(logic.starting_items)
    spoiler_log["required-dungeons"] = logic.required_dungeons
    spoiler_log["sots-locations"] = [loc for loc, _ in sots_locations[DEMISE]]
    spoiler_log["barren-regions"] = logic.get_barren_regions()[0]
    spoiler_log["playthrough"] = logic.calculate_playthrough_progression_spheres()
    spoiler_log["item-locations"] = logic.done_item_locations
    spoiler_log["hints"] = {k: v.to_spoiler_log_json() for k, v in hints.items()}
    spoiler_log["entrances"] = logic.entrance_connections
    spoiler_log["trial-connections"] = logic.trial_connections


def dump_header_json(options: Options, hash):
    header_dict = OrderedDict()
    header_dict["version"] = VERSION
    header_dict["permalink"] = options.get_permalink()
    header_dict["seed"] = options["seed"]
    header_dict["hash"] = hash
    non_disabled_options = [
        (name, val)
        for (name, val) in options.options.items()
        if (
            options[name] not in [False, [], {}, OrderedDict()]
            or OPTIONS[name]["type"] == "int"
        )
    ]
    header_dict["options"] = OrderedDict(
        filter(
            lambda tupl: OPTIONS[tupl[0]].get("permalink", True),
            non_disabled_options,
        )
    )
    header_dict["cosmetic-options"] = OrderedDict(
        filter(
            lambda tupl: OPTIONS[tupl[0]].get("cosmetic", False),
            non_disabled_options,
        )
    )
    return header_dict


def write_header(file: TextIO, options: Options, hash):

    file.write("Skyward Sword Randomizer Version %s\n" % VERSION)

    file.write("Permalink: %s\n" % options.get_permalink())

    file.write("Seed: %s\n" % options["seed"])

    file.write("Hash : %s\n" % hash)

    file.write("Options selected:\n")
    non_disabled_options = [
        (name, val)
        for (name, val) in options.options.items()
        if (
            options[name] not in [False, [], {}, OrderedDict()]
            or OPTIONS[name]["type"] == "int"
        )
    ]

    def format_opts(opts):
        option_strings = []
        for option_name, option_value in opts:
            if isinstance(option_value, bool):
                option_strings.append("  %s" % option_name)
            else:
                option_strings.append("  %s: %s" % (option_name, option_value))
        return "\n".join(option_strings)

    file.write(
        format_opts(
            filter(
                lambda tupl: OPTIONS[tupl[0]].get("permalink", True),
                non_disabled_options,
            )
        )
    )
    cosmetic_options = list(
        filter(
            lambda tupl: OPTIONS[tupl[0]].get("cosmetic", False),
            non_disabled_options,
        )
    )
    if cosmetic_options:
        file.write("\n\nCosmetic Options:\n")
        file.write(format_opts(cosmetic_options))
