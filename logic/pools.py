from .constants import *
from .logic import PoolEntrance, PoolExit

DUNGEON_MAIN_ENTRANCES_POOL = {
    entrance_of_exit(exit): PoolEntrance(entrance_of_exit(exit), [exit])
    for exit in DUNGEON_MAIN_EXITS.values()
}
DUNGEON_REVERSE_ENTRANCES_POOL = {
    exit: PoolExit(exit, [entrance_of_exit(exit)])
    for exit in DUNGEON_MAIN_EXITS.values()
}

VANILLA_DUNGEON_ACCESSES = {
    SV: EIN("Faron - Deep Woods - Exit to Skyview Temple"),
    ET: EIN("Eldin - Volcano - Exit to Earth Temple"),
    LMF: EIN("Lanayru - Desert - Exit to Lanayru Mining Facility"),
    AC: EIN("Faron - Lake Floria - Exit to Ancient Cistern"),
    SSH: EIN("Lanayru - Lanayru Sand Sea - Sandship Dock Exit"),
    FS: EIN("Eldin - Volcano Summit - Exit to Fire Sanctuary"),
    SK: EIN("Skyloft - Exit to Sky Keep"),
}

DUNGEON_ACCESSES_POOL = {
    exit: PoolExit(exit, [entrance_of_exit(exit)])
    for exit in VANILLA_DUNGEON_ACCESSES.values()
}
DUNGEON_REVERSE_ACCESSES_POOL = {
    entrance_of_exit(exit): PoolEntrance(entrance_of_exit(exit), [exit])
    for exit in VANILLA_DUNGEON_ACCESSES.values()
}

DUNGEON_ENTRANCES_COMPLETE_POOLS = [
    (DUNGEON_MAIN_ENTRANCES_POOL, DUNGEON_ACCESSES_POOL),
    (DUNGEON_REVERSE_ACCESSES_POOL, DUNGEON_REVERSE_ENTRANCES_POOL),
]

# Silent Realms
SILENT_REALMS_EXITS = {
    EIN("Skyloft - Silent Realm - Exit"),
    EIN("Faron - Silent Realm - Exit"),
    EIN("Lanayru - Silent Realm - Exit"),
    EIN("Eldin - Silent Realm - Exit"),
}

SILENT_REALM_ENTRANCES_POOL = {
    entrance_of_exit(exit): PoolEntrance(entrance_of_exit(exit), [exit])
    for exit in SILENT_REALMS_EXITS
}
SILENT_REALM_EXITS_POOL = {
    exit: PoolExit(exit, [entrance_of_exit(exit)]) for exit in SILENT_REALMS_EXITS
}

SILENT_REALM_ACCESSES = {
    EIN("Skyloft - Trial Gate Exit"),
    EIN("Faron - Faron Woods - Trial Gate Exit"),
    EIN("Lanayru - Desert - Trial Gate Exit"),
    EIN("Eldin - Volcano - Trial Gate Exit"),
}
SILENT_REALM_ACCESSES_POOL = {
    exit: PoolExit(exit, [entrance_of_exit(exit)]) for exit in SILENT_REALM_ACCESSES
}
SILENT_REALM_REVERSE_ACCESSES_POOL = {
    entrance_of_exit(exit): PoolEntrance(entrance_of_exit(exit), [exit])
    for exit in SILENT_REALM_ACCESSES
}

SILENT_REALMNS_COMPLETE_POOLS = [
    (SILENT_REALM_ENTRANCES_POOL, SILENT_REALM_ACCESSES_POOL),
    (SILENT_REALM_REVERSE_ACCESSES_POOL, SILENT_REALM_EXITS_POOL),
]
