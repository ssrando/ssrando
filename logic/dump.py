from logic.constants import *


def dump_constants(short_to_full):
    # dungeons = [SV, ET, LMF, AC, SSH, FS, SK]

    return {
        "silent_realms": { p: silent_realm(p, short_to_full) for p in ALL_SILENT_REALMS },
        "dungeons": { p: dungeon(p, short_to_full) for p in ALL_DUNGEONS }
    }

def silent_realm(pool, short_to_full):
    return {
        "exit_from_outside": short_to_full(TRIAL_GATE_EXITS[SILENT_REALM_GATES[pool]]),
        # "entrance_from_outside": short_to_full(entrance_of_exit(SILENT_REALM_EXITS[pool])),
        "exit_from_inside": short_to_full(SILENT_REALM_EXITS[pool]),
        # "entrance_from_inside": short_to_full(entrance_of_exit(TRIAL_GATE_EXITS[SILENT_REALM_GATES[pool]])),
    }

def dungeon(pool, short_to_full):
    entrance = DUNGEON_OVERWORLD_ENTRANCES[pool]
    exit_to_dungeon = DUNGEON_ENTRANCE_EXITS[entrance]
    exit_from_dungeon = DUNGEON_MAIN_EXITS[pool]

    return {
        "exit_from_outside": [short_to_full(e) for e in exit_to_dungeon] if len(exit_to_dungeon) > 1 else short_to_full(exit_to_dungeon[0]),
        # "entrance_from_outside": short_to_full(entrance_of_exit(exit_from_dungeon)),
        "exit_from_inside": short_to_full(exit_from_dungeon),
        # "entrance_from_inside": short_to_full(entrance_of_exit(exit_to_dungeon[0])),
    }