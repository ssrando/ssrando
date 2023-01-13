from collections import defaultdict
from typing import NewType, Dict, Callable

EXTENDED_ITEM_NAME = NewType("EXTENDED_ITEM_NAME", str)
EIN = EXTENDED_ITEM_NAME

sep = " - "

EVERYTHING = EIN("Everything")

NUMBER_OF_HINT_STONES = 18

MAX_HINTS_PER_STONE = 8
MAX_HINTS = MAX_HINTS_PER_STONE * NUMBER_OF_HINT_STONES

# Logic options, runtime requirements

OPEN_THUNDERHEAD_OPTION = EIN("Open Thunderhead option")
OPEN_ET_OPTION = EIN("Open ET option")
OPEN_LMF_OPTION = EIN("Open LMF option")
LMF_NODES_ON_OPTION = EIN("LMF Nodes On option")
RANDOMIZED_BEEDLE_OPTION = EIN("Randomized Beedle option")
GONDO_UPGRADES_ON_OPTION = EIN("Gondo Upgrades On option")
NO_BIT_CRASHES = EIN("No BiT crashes")
NONLETHAL_HOT_CAVE = EIN("Nonlethal Hot Cave")
UPGRADED_SKYWARD_STRIKE = EIN("Upgraded Skyward Strike option")

GOT_OPENING_REQUIREMENT = EIN("GoT Opening Requirement")
GOT_RAISING_REQUIREMENT = EIN("GoT Raising Requirement")
HORDE_DOOR_REQUIREMENT = EIN("Horde Door Requirement")

BEEDLE_STALL_ACCESS = EIN("Beedle Stall Access Token")
MEDIUM_PURCHASES = EIN("Medium Purchases Token")
EXPENSIVE_PURCHASES = EIN("Expensive Purchases Token")
MAY_GET_n_CRYSTALS = lambda n: EIN(f"May Get {n} Crystals Token")

CRYSTAL_THRESHOLDS = [5, 10, 30, 40, 50, 70, 80]

LOGIC_OPTIONS = dict.fromkeys(
    [
        OPEN_THUNDERHEAD_OPTION,
        OPEN_ET_OPTION,
        OPEN_LMF_OPTION,
        LMF_NODES_ON_OPTION,
        RANDOMIZED_BEEDLE_OPTION,
        GONDO_UPGRADES_ON_OPTION,
        NO_BIT_CRASHES,
        NONLETHAL_HOT_CAVE,
        UPGRADED_SKYWARD_STRIKE,
        GOT_OPENING_REQUIREMENT,
        GOT_RAISING_REQUIREMENT,
        HORDE_DOOR_REQUIREMENT,
        BEEDLE_STALL_ACCESS,
        MEDIUM_PURCHASES,
        EXPENSIVE_PURCHASES,
    ]
    + [MAY_GET_n_CRYSTALS(n) for n in CRYSTAL_THRESHOLDS]
)

# Locations


def with_sep_full(pre: str, loc: str) -> EXTENDED_ITEM_NAME:
    if "\\" not in loc:
        return EIN(pre + "\\" + loc)
    return EIN(loc)


make_day = lambda s: EIN(s + "_DAY")
make_night = lambda s: EIN(s + "_NIGHT")


def entrance_of_exit(exit):
    if exit.endswith(" Exit") or exit.endswith("\\Exit"):
        return exit.replace("Exit", "Entrance")
    if "Exit to " in exit:
        return exit.replace("Exit to", "Entrance from")
    raise ValueError("No pattern")


SV = "Skyview"
ET = "Earth Temple"
LMF = "Lanayru Mining Facility"
AC = "Ancient Cistern"
SSH = "Sandship"
FS = "Fire Sanctuary"
SK = "Sky Keep"

DUNGEON_COMPLETE_STORYFLAGS = {
    SV: 5,
    ET: 7,
    LMF: 935,
    AC: 900,
    SSH: 15,
    FS: 901,
}

DUNGEON_COLORS = {
    SV: "<g<",
    ET: "<r+<",
    LMF: "<y<",
    AC: "<b<",
    FS: "<r<",
    SSH: "<y+<",
    SK: "<s<",
    "Lanayru Caves": "<ye<",
}

REGULAR_DUNGEONS = [SV, ET, LMF, AC, SSH, FS]
ALL_DUNGEONS = REGULAR_DUNGEONS + [SK]

SV_ENTRANCE = "Dungeon Entrance in Deep Woods"
ET_ENTRANCE = "Dungeon Entrance in Eldin Volcano"
LMF_ENTRANCE = "Dungeon Entrance in Lanayru Desert"
AC_ENTRANCE = "Dungeon Entrance in Lake Floria"
SSH_ENTRANCE = "Dungeon Entrance in Lanayru Sand Sea"
FS_ENTRANCE = "Dungeon Entrance in Volcano Summit"
SK_ENTRANCE = "Dungeon Entrance on Skyloft"

EMERALD_TABLET = "Emerald Tablet"
RUBY_TABLET = "Ruby Tablet"
AMBER_TABLET = "Amber Tablet"

SKYLOFT_SILENT_REALM = "Skyloft Silent Realm"
FARON_SILENT_REALM = "Faron Silent Realm"
LANAYRU_SILENT_REALM = "Lanayru Silent Realm"
ELDIN_SILENT_REALM = "Eldin Silent Realm"

ALL_SILENT_REALMS = [
    SKYLOFT_SILENT_REALM,
    FARON_SILENT_REALM,
    LANAYRU_SILENT_REALM,
    ELDIN_SILENT_REALM,
]

# Items

ITEM_COUNTS: Dict[str, int] = defaultdict(lambda: 1)


def number(name: str, index: int) -> EXTENDED_ITEM_NAME:
    if index >= ITEM_COUNTS[name]:
        raise ValueError("Index too high")
    if ITEM_COUNTS[name] == 1:
        return EIN(name)
    return EIN(f"{name} #{index}")


def strip_item_number(item: EXTENDED_ITEM_NAME) -> str:
    if "#" not in item:
        return item
    return item[: item.index("#") - 1]


def group(name: str, count: int) -> Dict[EXTENDED_ITEM_NAME, None]:
    if name not in ITEM_COUNTS:
        ITEM_COUNTS[name] = count
    return {number(name, i): None for i in range(count)}


HINT = "Hint"
HINTS = group(HINT, MAX_HINTS)

# SAILCLOTH = EIN("Sailcloth")
BOMB_BAG = EIN("Bomb Bag")
GUST_BELLOWS = EIN("Gust Bellows")
WHIP = EIN("Whip")
CLAWSHOTS = EIN("Clawshots")
WATER_SCALE = EIN("Water Scale")
FIRESHIELD_EARRINGS = EIN("Fireshield Earrings")
SEA_CHART = EIN("Sea Chart")
EMERALD_TABLET = EIN("Emerald Tablet")
RUBY_TABLET = EIN("Ruby Tablet")
AMBER_TABLET = EIN("Amber Tablet")
STONE_OF_TRIALS = EIN("Stone of Trials")

BABY_RATTLE = EIN("Baby Rattle")
CAWLINS_LETTER = EIN("Cawlin's Letter")
HORNED_COLOSSUS_BEETLE = EIN("Horned Colossus Beetle")
GODDESS_HARP = EIN("Goddess Harp")
BALLAD_OF_THE_GODDESS = EIN("Ballad of the Goddess")
FARORES_COURAGE = EIN("Farore's Courage")
NAYRUS_WISDOM = EIN("Nayru's Wisdom")
DINS_POWER = EIN("Din's Power")
FARON_SOTH_PART = EIN("Faron Song of the Hero Part")
ELDIN_SOTH_PART = EIN("Eldin Song of the Hero Part")
LANAYRU_SOTH_PART = EIN("Lanayru Song of the Hero Part")
SONG_OF_THE_HERO = "Song of the Hero"
SPIRAL_CHARGE = EIN("Spiral Charge")
LIFE_TREE_SEEDLING = EIN("Life Tree Seedling")
LIFE_TREE_FRUIT = EIN("Life Tree Fruit")
TRIFORCE_OF_COURAGE = EIN("Triforce of Courage")
TRIFORCE_OF_WISDOM = EIN("Triforce of Wisdom")
TRIFORCE_OF_POWER = EIN("Triforce of Power")

GRATITUDE_CRYSTAL_PACK = "Gratitude Crystal Pack"
GRATITUDE_CRYSTAL = "Gratitude Crystal"
PROGRESSIVE_SWORD = "Progressive Sword"
PROGRESSIVE_MITTS = "Progressive Mitts"
PROGRESSIVE_SLINGSHOT = "Progressive Slingshot"
PROGRESSIVE_BEETLE = "Progressive Beetle"
PROGRESSIVE_BOW = "Progressive Bow"
PROGRESSIVE_BUG_NET = "Progressive Bug Net"
PROGRESSIVE_POUCH = "Progressive Pouch"
KEY_PIECE = "Key Piece"
FULL_ET_KEY = "Full ET Key"
EMPTY_BOTTLE = "Empty Bottle"
PROGRESSIVE_WALLET = "Progressive Wallet"
EXTRA_WALLET = "Extra Wallet"

GRATITUDE_CRYSTAL_PACKS = group(GRATITUDE_CRYSTAL_PACK, 13)
GRATITUDE_CRYSTALS = group(GRATITUDE_CRYSTAL, 15)
NUMBER_SWORDS = 6
PROGRESSIVE_SWORDS = group(PROGRESSIVE_SWORD, NUMBER_SWORDS)
PROGRESSIVE_MITTS_ALL = group(PROGRESSIVE_MITTS, 2)
PROGRESSIVE_SLINGSHOTS = group(PROGRESSIVE_SLINGSHOT, 2)
PROGRESSIVE_BEETLES = group(PROGRESSIVE_BEETLE, 4)
PROGRESSIVE_BOWS = group(PROGRESSIVE_BOW, 3)
PROGRESSIVE_BUG_NETS = group(PROGRESSIVE_BUG_NET, 2)
PROGRESSIVE_POUCHES = group(PROGRESSIVE_POUCH, 5)
KEY_PIECES = group(KEY_PIECE, 5)
EMPTY_BOTTLES = group(EMPTY_BOTTLE, 5)
PROGRESSIVE_WALLETS = group(PROGRESSIVE_WALLET, 4)
EXTRA_WALLETS = group(EXTRA_WALLET, 3)

small_key = lambda d: d + " Small Key"
SMALL_KEY = {dun: small_key(dun) for dun in ALL_DUNGEONS}

boss_key = lambda d: d + " Boss Key"
BOSS_KEY = {dun: boss_key(dun) for dun in ALL_DUNGEONS}

dungeon_map = lambda d: EIN(d + " Map")
MAP = {dun: dungeon_map(dun) for dun in ALL_DUNGEONS}

SONG_OF_THE_HERO_PARTS = [FARON_SOTH_PART, ELDIN_SOTH_PART, LANAYRU_SOTH_PART]
TRIFORCES = dict.fromkeys([TRIFORCE_OF_COURAGE, TRIFORCE_OF_POWER, TRIFORCE_OF_WISDOM])

CAVES_KEY = EIN("Lanayru Caves Small Key")

SMALL_KEYS = {
    SV: group(SMALL_KEY[SV], 2),
    ET: group(SMALL_KEY[ET], 0),
    LMF: group(SMALL_KEY[LMF], 1),
    AC: group(SMALL_KEY[AC], 2),
    SSH: group(SMALL_KEY[SSH], 2),
    FS: group(SMALL_KEY[FS], 3),
    SK: group(SMALL_KEY[SK], 1),
}

BOSS_KEYS = {
    SV: group(BOSS_KEY[SV], 1),
    ET: group(BOSS_KEY[ET], 1),
    LMF: group(BOSS_KEY[LMF], 1),
    AC: group(BOSS_KEY[AC], 1),
    SSH: group(BOSS_KEY[SSH], 1),
    FS: group(BOSS_KEY[FS], 1),
    SK: group(BOSS_KEY[SK], 0),
}

WOODEN_SHIELD = EIN("Wooden Shield")
HYLIAN_SHIELD = EIN("Hylian Shield")
CURSED_MEDAL = EIN("Cursed Medal")
TREASURE_MEDAL = EIN("Treasure Medal")
POTION_MEDAL = EIN("Potion Medal")
SMALL_SEED_SATCHEL = EIN("Small Seed Satchel")
SMALL_BOMB_BAG = EIN("Small Bomb Bag")
SMALL_QUIVER = EIN("Small Quiver")
BUG_MEDAL = EIN("Bug Medal")

HEART_MEDAL = "Heart Medal"
RUPEE_MEDAL = "Rupee Medal"
HEART_PIECE = "Heart Piece"
HEART_CONTAINER = "Heart Container"
LIFE_MEDAL = "Life Medal"

HEART_MEDALS = group(HEART_MEDAL, 2)
RUPEE_MEDALS = group(RUPEE_MEDAL, 2)
HEART_PIECES = group(HEART_PIECE, 24)
HEART_CONTAINERS = group(HEART_CONTAINER, 6)
LIFE_MEDALS = group(LIFE_MEDAL, 2)

GREEN_RUPEE = "Green Rupee"
BLUE_RUPEE = "Blue Rupee"
RED_RUPEE = "Red Rupee"
SILVER_RUPEE = "Silver Rupee"
GOLD_RUPEE = "Gold Rupee"
SEMI_RARE_TREASURE = "Semi Rare Treasure"
GOLDEN_SKULL = "Golden Skull"
RARE_TREASURE = "Rare Treasure"
EVIL_CRYSTAL = "Evil Crystal"
ELDIN_ORE = "Eldin Ore"
GODDESS_PLUME = "Goddess Plume"
DUSK_RELIC = "Dusk Relic"
TUMBLEWEED = "Tumbleweed"
FIVE_BOMBS = "5 Bombs"

GREEN_RUPEES = group(GREEN_RUPEE, 3)
BLUE_RUPEES = group(BLUE_RUPEE, 11)
RED_RUPEES = group(RED_RUPEE, 42)
SILVER_RUPEES = group(SILVER_RUPEE, 22)
GOLD_RUPEES = group(GOLD_RUPEE, 11)
SEMI_RARE_TREASURES = group(SEMI_RARE_TREASURE, 10)
GOLDEN_SKULLS = group(GOLDEN_SKULL, 1)
RARE_TREASURES = group(RARE_TREASURE, 12)
EVIL_CRYSTALS = group(EVIL_CRYSTAL, 2)
ELDIN_ORES = group(ELDIN_ORE, 2)
GODDESS_PLUMES = group(GODDESS_PLUME, 1)
DUSK_RELICS = group(DUSK_RELIC, 1)
TUMBLEWEEDS = group(TUMBLEWEED, 1)
FIVE_BOMBS_GROUP = group(FIVE_BOMBS, 1)


RUPOOR = "Rupoor"

PROGRESS_ITEMS = (
    dict.fromkeys(
        [
            BOMB_BAG,
            GUST_BELLOWS,
            WHIP,
            CLAWSHOTS,
            WATER_SCALE,
            FIRESHIELD_EARRINGS,
            SEA_CHART,
            EMERALD_TABLET,
            RUBY_TABLET,
            AMBER_TABLET,
            STONE_OF_TRIALS,
            BABY_RATTLE,
            CAWLINS_LETTER,
            HORNED_COLOSSUS_BEETLE,
            GODDESS_HARP,
            BALLAD_OF_THE_GODDESS,
            FARORES_COURAGE,
            NAYRUS_WISDOM,
            DINS_POWER,
            FARON_SOTH_PART,
            ELDIN_SOTH_PART,
            LANAYRU_SOTH_PART,
            SPIRAL_CHARGE,
            # LIFE_TREE_SEEDLING,
            LIFE_TREE_FRUIT,
            TRIFORCE_OF_COURAGE,
            TRIFORCE_OF_WISDOM,
            TRIFORCE_OF_POWER,
            # SAILCLOTH,
        ]
    )
    | GRATITUDE_CRYSTAL_PACKS
    | GRATITUDE_CRYSTALS
    | PROGRESSIVE_SWORDS
    | PROGRESSIVE_MITTS_ALL
    | PROGRESSIVE_SLINGSHOTS
    | PROGRESSIVE_BEETLES
    | PROGRESSIVE_BOWS
    | PROGRESSIVE_BUG_NETS
    | PROGRESSIVE_POUCHES
    | KEY_PIECES
    | EMPTY_BOTTLES
    | PROGRESSIVE_WALLETS
    | EXTRA_WALLETS
)

NONPROGRESS_ITEMS = (
    dict.fromkeys(
        [
            WOODEN_SHIELD,
            HYLIAN_SHIELD,
            CURSED_MEDAL,
            TREASURE_MEDAL,
            POTION_MEDAL,
            SMALL_SEED_SATCHEL,
            SMALL_BOMB_BAG,
            SMALL_QUIVER,
            BUG_MEDAL,
        ]
    )
    | HEART_MEDALS
    | RUPEE_MEDALS
    | HEART_PIECES
    | HEART_CONTAINERS
    | LIFE_MEDALS
)

RUPEES = GREEN_RUPEES | BLUE_RUPEES | RED_RUPEES | SILVER_RUPEES | GOLD_RUPEES

TREASURES = (
    DUSK_RELICS
    | ELDIN_ORES
    | EVIL_CRYSTALS
    | GODDESS_PLUMES
    | GOLDEN_SKULLS
    | TUMBLEWEEDS
    | SEMI_RARE_TREASURES
    | RARE_TREASURES
)

CONSUMABLE_ITEMS = RUPEES | TREASURES | FIVE_BOMBS_GROUP

# Once all the items that have a fixed number per seed are used up, this list is used.
# Unlike the other lists, this one does not have items removed from it as they are placed.
# The number of each item in this list is instead its weighting relative to the other items in the list.
DUPLICABLE_ITEMS = dict.fromkeys(
    [
        BLUE_RUPEE,
        RED_RUPEE,
        SEMI_RARE_TREASURE,
        RARE_TREASURE,
    ]
)
DUPLICABLE_COUNTERPROGRESS_ITEMS = {RUPOOR: None}

# note: Lanayru Caves is technically not a dungeon, but has to be treated as such for non key sanity
ALL_SMALL_KEYS = (
    {CAVES_KEY: None}
    | SMALL_KEYS[SV]
    | SMALL_KEYS[ET]
    | SMALL_KEYS[LMF]
    | SMALL_KEYS[AC]
    | SMALL_KEYS[SSH]
    | SMALL_KEYS[FS]
    | SMALL_KEYS[SK]
)
ALL_BOSS_KEYS = (
    BOSS_KEYS[SV]
    | BOSS_KEYS[ET]
    | BOSS_KEYS[LMF]
    | BOSS_KEYS[AC]
    | BOSS_KEYS[SSH]
    | BOSS_KEYS[FS]
    | BOSS_KEYS[SK]
)
ALL_MAPS = dict.fromkeys(MAP.values())

INVENTORY_ITEMS = (
    PROGRESS_ITEMS
    | NONPROGRESS_ITEMS
    | CONSUMABLE_ITEMS
    | ALL_SMALL_KEYS
    | ALL_BOSS_KEYS
    | ALL_MAPS
)

ALL_ITEM_NAMES = INVENTORY_ITEMS | DUPLICABLE_ITEMS | DUPLICABLE_COUNTERPROGRESS_ITEMS
RAW_ITEM_NAMES = dict.fromkeys(strip_item_number(EIN(k)) for k in ALL_ITEM_NAMES)

TABLETS = [EMERALD_TABLET, RUBY_TABLET, AMBER_TABLET]

SWORD_COUNT = {
    "Swordless": 0,
    "Practice Sword": 1,
    "Goddess Sword": 2,
    "Goddess Longsword": 3,
    "Goddess White Sword": 4,
    "Master Sword": 5,
    "True Master Sword": 6,
}


str_main_exit = "Main Exit"
DUNGEON_MAIN_EXITS = {
    SV: SV + sep + str_main_exit,
    ET: ET + sep + str_main_exit,
    LMF: LMF + sep + str_main_exit,
    AC: AC + sep + str_main_exit,
    SSH: SSH + sep + str_main_exit,
    FS: FS + sep + str_main_exit,
    SK: SK + sep + "First Room - Bottom Exit",
}

DUNGEON_FINAL_CHECK = {
    SV: SV + sep + RUBY_TABLET,
    ET: ET + sep + AMBER_TABLET,
    LMF: LMF + sep + GODDESS_HARP,
    AC: AC + sep + "Farore's Flame",
    SSH: SSH + sep + "Nayru's Flame",
    FS: FS + sep + "Din's Flame",
}

dungeon_heart_containers = lambda d: d + sep + HEART_CONTAINER
DUNGEON_HEART_CONTAINERS = {
    dun: dungeon_heart_containers(dun) for dun in REGULAR_DUNGEONS
}

GHIRAHIM_I = "Ghirahim 1"
SCALDERA = "Scaldera"
MOLDARACH = "Moldarach"
KOLOKTOS = "Koloktos"
TENTALUS = "Tentalus"
GHIRAHIM_II = "Ghirahim 2"
DEMISE = "Defeat Demise"

GOALS = [GHIRAHIM_I, SCALDERA, MOLDARACH, KOLOKTOS, TENTALUS, GHIRAHIM_II]
ALL_GOALS = GOALS + [DEMISE]

DUNGEON_GOALS = {
    SV: GHIRAHIM_I,
    ET: SCALDERA,
    LMF: MOLDARACH,
    AC: KOLOKTOS,
    SSH: TENTALUS,
    FS: GHIRAHIM_II,
}

GOAL_CHECKS = {
    GHIRAHIM_I: DUNGEON_HEART_CONTAINERS[SV],
    SCALDERA: DUNGEON_HEART_CONTAINERS[ET],
    MOLDARACH: DUNGEON_HEART_CONTAINERS[LMF],
    KOLOKTOS: DUNGEON_HEART_CONTAINERS[AC],
    TENTALUS: DUNGEON_HEART_CONTAINERS[SSH],
    GHIRAHIM_II: DUNGEON_HEART_CONTAINERS[FS],
    DEMISE: DEMISE,
}


START = "Start"
START_ITEM = EIN("Start Item")
UNPLACED_ITEM = EIN("Unplaced Item")
SONG_IMPA_CHECK = "Sealed Grounds - Song from Impa"
COMPLETE_TRIFORCE = "Complete Triforce"

trick: Callable[[str], str] = lambda s: s + " Trick"

CISTERN_CLIP = EIN(trick("Ancient Cistern - Cistern Clip"))

UPPER_SKYLOFT = "Upper Skyloft"
CENTRAL_SKYLOFT = "Central Skyloft"
SKYLOFT_VILLAGE = "Skyloft Village"
BATREAUX = "Batreaux's House"
BEEDLE = "Beedle's Shop"

SKY = "Sky"
THUNDERHEAD = "Thunderhead"

SEALED_GROUNDS = "Sealed Grounds"
FARON_WOODS = "Faron Woods"
LAKE_FLORIA = "Lake Floria"
FLOODED_FARON_WOODS = "Flooded Faron Woods"

ELDIN_VOLCANO = "Eldin Volcano"
MOGMA_TURF = "Mogma Turf"
VOLCANO_SUMMIT = "Volcano Summit"
BOKOBLIN_BASE = "Bokoblin Base"

LANAYRU_MINE = "Lanayru Mine"
LANAYRU_DESERT = "Lanayru Desert"
LANAYRU_CAVES = "Lanayru Caves"
LANAYRU_GORGE = "Lanayru Gorge"
LANAYRU_SAND_SEA = "Lanayru Sand Sea"

ALL_HINT_REGIONS = dict.fromkeys(
    [
        UPPER_SKYLOFT,
        CENTRAL_SKYLOFT,
        SKYLOFT_VILLAGE,
        BATREAUX,
        BEEDLE,
        SKY,
        THUNDERHEAD,
        SEALED_GROUNDS,
        FARON_WOODS,
        FLOODED_FARON_WOODS,
        LAKE_FLORIA,
        ELDIN_VOLCANO,
        MOGMA_TURF,
        VOLCANO_SUMMIT,
        BOKOBLIN_BASE,
        LANAYRU_MINE,
        LANAYRU_DESERT,
        LANAYRU_CAVES,
        LANAYRU_GORGE,
        LANAYRU_SAND_SEA,
        SV,
        ET,
        LMF,
        AC,
        SSH,
        FS,
        SK,
        SKYLOFT_SILENT_REALM,
        FARON_SILENT_REALM,
        LANAYRU_SILENT_REALM,
        ELDIN_SILENT_REALM,
    ]
)

DUNGEONFLAG_INDICES = {
    SV: 11,
    ET: 14,
    LMF: 17,
    AC: 12,
    SSH: 18,
    FS: 15,
    SK: 20,
    LANAYRU_CAVES: 9,
}

# Retro-compatibility

SV_ENTRANCE = "Dungeon Entrance in Deep Woods"
ET_ENTRANCE = "Dungeon Entrance in Eldin Volcano"
LMF_ENTRANCE = "Dungeon Entrance in Lanayru Desert"
AC_ENTRANCE = "Dungeon Entrance in Lake Floria"
SSH_ENTRANCE = "Dungeon Entrance in Lanayru Sand Sea"
FS_ENTRANCE = "Dungeon Entrance in Volcano Summit"
SK_ENTRANCE = "Dungeon Entrance on Skyloft"

DUNGEON_OVERWORLD_ENTRANCES = {
    SV: SV_ENTRANCE,
    ET: ET_ENTRANCE,
    LMF: LMF_ENTRANCE,
    AC: AC_ENTRANCE,
    SSH: SSH_ENTRANCE,
    FS: FS_ENTRANCE,
    SK: SK_ENTRANCE,
}

DUNGEON_ENTRANCE_EXITS: dict[str, list[str]] = {
    SV_ENTRANCE: ["Deep Woods - Exit to Skyview Temple"],
    ET_ENTRANCE: ["Eldin Volcano - Exit to Earth Temple"],
    LMF_ENTRANCE: ["Lanayru Desert - Exit to Lanayru Mining Facility"],
    AC_ENTRANCE: ["Floria Waterfall - Exit to Ancient Cistern"],
    SSH_ENTRANCE: [
        "Lanayru Sand Sea - Sandship Dock Exit",
        "Lanayru Sand Sea Docks - Exit to Sandship",
    ],
    FS_ENTRANCE: ["Outside Fire Sanctuary - Exit to Fire Sanctuary"],
    SK_ENTRANCE: ["Skyloft - Exit to Sky Keep"],
}

LMF_SECOND_EXIT = LMF + sep + "Great Hall" + sep + "Exit to Temple of Time"

SKYLOFT_TRIAL_GATE = "Trial Gate on Skyloft"
FARON_TRIAL_GATE = "Trial Gate in Faron Woods"
LANAYRU_TRIAL_GATE = "Trial Gate in Lanayru Desert"
ELDIN_TRIAL_GATE = "Trial Gate in Eldin Volcano"

SILENT_REALM_GATES = {
    SKYLOFT_SILENT_REALM: SKYLOFT_TRIAL_GATE,
    FARON_SILENT_REALM: FARON_TRIAL_GATE,
    LANAYRU_SILENT_REALM: LANAYRU_TRIAL_GATE,
    ELDIN_SILENT_REALM: ELDIN_TRIAL_GATE,
}

SONG_OF_THE_HERO_TRIAL_HINT = EIN("Song of the Hero - Trial Hint")
FARORES_COURAGE_TRIAL_HINT = EIN("Farore's Courage - Trial Hint")
NAYRUS_WISDOM_TRIAL_HINT = EIN("Nayru's Wisdom - Trial Hint")
DINS_POWER_TRIAL_HINT = EIN("Din's Power - Trial Hint")


SONG_HINTS = {
    SONG_OF_THE_HERO_TRIAL_HINT: SKYLOFT_TRIAL_GATE,
    FARORES_COURAGE_TRIAL_HINT: FARON_TRIAL_GATE,
    NAYRUS_WISDOM_TRIAL_HINT: LANAYRU_TRIAL_GATE,
    DINS_POWER_TRIAL_HINT: ELDIN_TRIAL_GATE,
}

TRIAL_GATE_EXITS: dict[str, str] = {
    SKYLOFT_TRIAL_GATE: "Skyloft - Trial Gate Exit",
    FARON_TRIAL_GATE: "Faron Woods - Trial Gate Exit",
    ELDIN_TRIAL_GATE: "Eldin Volcano - Trial Gate Exit",
    LANAYRU_TRIAL_GATE: "Lanayru Desert - Trial Gate Exit",
}

SILENT_REALM_EXITS: dict[str, str] = {
    SKYLOFT_SILENT_REALM: "Skyloft Silent Realm - Exit",
    FARON_SILENT_REALM: "Faron Silent Realm - Exit",
    ELDIN_SILENT_REALM: "Eldin Silent Realm - Exit",
    LANAYRU_SILENT_REALM: "Lanayru Silent Realm - Exit",
}

SILENT_REALM_CHECKS: dict[str, str] = {
    SKYLOFT_SILENT_REALM: "Skyloft Silent Realm - Stone of Trials",
    FARON_SILENT_REALM: "Faron Silent Realm - Water Scale",
    ELDIN_SILENT_REALM: "Eldin Silent Realm - Fireshield Earrings",
    LANAYRU_SILENT_REALM: "Lanayru Silent Realm - Clawshots",
}

SILENT_REALM_CHECKS_REV = lambda norm: {
    norm(v): k for k, v in SILENT_REALM_CHECKS.items()
}


RUPEE_CHECKS = [
    "Skyloft - Central Skyloft - Rupee Waterfall Cave Crawlspace",
    "Great Tree - Rupee on Great Tree North Branch",
    "Great Tree - Rupee on Great Tree West Branch",
    "Faron Woods - Rupee on Platform near Floria Door",
    "Faron Woods - Rupee on Hollow Tree Root",
    "Faron Woods - Rupee on Hollow Tree Branch",
    "Lake Floria - Rupee under Central Boulder",
    "Lake Floria - Right Rupee behind Northwest Boulder",
    "Lake Floria - Left Rupee behind Northwest Boulder",
    "Lake Floria - Rupee behind Southwest Boulder",
    "Floria Waterfall - Rupee on High Ledge outside Ancient Cistern Entrance",
    "Eldin Volcano - Rupee on Ledge before First Room",
    "Eldin Volcano - Rupee behind Bombable Wall in First Room",
    "Eldin Volcano - Rupee in Crawlspace in First Room",
    "Eldin Volcano - Southeast Rupee above Mogma Turf Entrance",
    "Eldin Volcano - North Rupee above Mogma Turf Entrance",
    "Eldin Volcano - Left Rupee behind Bombable Wall on First Slope",
    "Eldin Volcano - Right Rupee behind Bombable Wall on First Slope",
    "Ancient Harbour - Rupee on First Pillar",
    "Ancient Harbour - Left Rupee on Entrance Crown",
    "Ancient Harbour - Right Rupee on Entrance Crown",
    "Pirate Stronghold - Rupee on West Sea Pillar",
    "Pirate Stronghold - Rupee on East Sea Pillar",
    "Pirate Stronghold - Rupee on Bird Statue Pillar or Nose",
    "Skyview - Second Hub - Rupee in Southeast Tunnel",
    "Skyview - Second Hub - Rupee in Southwest Tunnel",
    "Skyview - Second Hub - Rupee in East Tunnel",
    "Skyview - Rupee on Spring Pillar",
    "Earth Temple - Rupee above Drawbridge",
    "Earth Temple - Rupee in Lava Tunnel",
    "Ancient Cistern - Rupee in East Part in Main Tunnel",
    "Ancient Cistern - Rupee in East Part in Cubby",
    "Ancient Cistern - First Rupee in East Part in Short Tunnel",
    "Ancient Cistern - Second Rupee in East Part in Short Tunnel",
    "Ancient Cistern - Third Rupee in East Part in Short Tunnel",
    # "Ancient Cistern - Rupee under Lilypad",
    "Ancient Cistern - Rupee in East Hand",
    "Ancient Cistern - Rupee in West Hand",
    "Sky Keep - Rupee in Fire Sanctuary Room in Alcove",
]

QUICK_BEETLE_CHECKS = [
    "Ancient Harbour - Left Rupee on Entrance Crown",
    "Ancient Harbour - Right Rupee on Entrance Crown",
    "Pirate Stronghold - Rupee on West Sea Pillar",
    "Pirate Stronghold - Rupee on East Sea Pillar",
]

GONDO_ITEMS = {
    number(PROGRESSIVE_BEETLE, 2),
    number(PROGRESSIVE_BEETLE, 3),
    number(PROGRESSIVE_SLINGSHOT, 1),
    number(PROGRESSIVE_BOW, 1),
    number(PROGRESSIVE_BOW, 2),
    number(PROGRESSIVE_BUG_NET, 1),
}


ITEM_FLAGS = {
    PROGRESSIVE_BOW: [19, 90, 91],
    PROGRESSIVE_BEETLE: [53, 75, 76, 77],
    PROGRESSIVE_BUG_NET: [71, 140],
    PROGRESSIVE_SLINGSHOT: [52, 105],
    PROGRESSIVE_MITTS: [56, 99],
    PROGRESSIVE_POUCH: [112, 113, 113, 113, 113],
    PROGRESSIVE_WALLET: [108, 109, 110, 111],
    PROGRESSIVE_SWORD: [10, 11, 12, 9, 13, 14],
    EMERALD_TABLET: 177,
    RUBY_TABLET: 178,
    AMBER_TABLET: 179,
    BOMB_BAG: 92,
    CLAWSHOTS: 20,
    WHIP: 137,
    GUST_BELLOWS: 49,
    WATER_SCALE: 68,
    FIRESHIELD_EARRINGS: 138,
    GODDESS_HARP: 16,
    BALLAD_OF_THE_GODDESS: 186,
    FARORES_COURAGE: 187,
    NAYRUS_WISDOM: 188,
    DINS_POWER: 189,
    FARON_SOTH_PART: 190,
    ELDIN_SOTH_PART: 191,
    LANAYRU_SOTH_PART: 192,
    SONG_OF_THE_HERO: 193,
    LIFE_TREE_FRUIT: 198,
    LIFE_TREE_SEEDLING: 197,
    STONE_OF_TRIALS: 180,
    CAWLINS_LETTER: 158,
    HORNED_COLOSSUS_BEETLE: 159,
    BABY_RATTLE: 160,
    SEA_CHART: 98,
    TRIFORCE_OF_COURAGE: 95,
    TRIFORCE_OF_POWER: 96,
    TRIFORCE_OF_WISDOM: 97,
    SPIRAL_CHARGE: 21,
    # SAILCLOTH: 15
}


# lists are used for progressive items,
# tuples for setting multiple flags for one item
ITEM_STORY_FLAGS = {
    EMERALD_TABLET: 46,
    RUBY_TABLET: 47,
    AMBER_TABLET: 48,
    HORNED_COLOSSUS_BEETLE: 476,
    CAWLINS_LETTER: 547,
    SPIRAL_CHARGE: 364,
    SEA_CHART: 271,
    WATER_SCALE: 206,  # Completed Faron Trial
    FIRESHIELD_EARRINGS: 207,  # Completed Eldin Trial
    CLAWSHOTS: 208,  # Completed Lanayru Trial
    STONE_OF_TRIALS: (210, 209),  # Obtained SoT, Completed Hylia's Trial
    GODDESS_HARP: (9, 140),  # Harp, Watched Groose CS
    BALLAD_OF_THE_GODDESS: 194,
    TRIFORCE_OF_COURAGE: 729,
    TRIFORCE_OF_POWER: 728,
    TRIFORCE_OF_WISDOM: 730,
    COMPLETE_TRIFORCE: 645,
    FULL_ET_KEY: 120,
    PROGRESSIVE_SWORD: [
        906,
        907,
        908,
        909,
        910,
        911,
    ],  # Practice, Goddess, Long, White, MS, TMS
    PROGRESSIVE_MITTS: [904, 905],  # Digging Mitts, Mogma Mitts
    PROGRESSIVE_BEETLE: [912, 913, 942, 943],  # Beetle, Heetle, Queetle, Teetle
    PROGRESSIVE_WALLET: [915, 916, 917, 918],  # Medium, Big, Giant, Tycoon
    PROGRESSIVE_BOW: [944, 945, 946],  # Bow, Iron, Sacred
    PROGRESSIVE_SLINGSHOT: [947, 948],  # Slingshot, Scatershot
    PROGRESSIVE_BUG_NET: [949, 950],  # Bug Net, Big Bug Net
    PROGRESSIVE_POUCH: [931, 932, 932, 932, 932]  # Adventure Pouch, Pouch Expansion * 4
    # SAILCLOTH: 32
}

ITEM_COUNT_FLAGS = {
    EXTRA_WALLET: 508,
    PROGRESSIVE_POUCH: 490,
    GRATITUDE_CRYSTAL_PACK: 502,
    KEY_PIECE: 505,
    HEART_PIECE: 489,  # 2 bytes, 487 MSB, 489 LSB
}

START_AMMO_COUNTS = {
    PROGRESSIVE_BOW: (498, 20),
    BOMB_BAG: (499, 10),
    PROGRESSIVE_SLINGSHOT: (493, 20),
}

RANDOM_STARTING_ITEMS = [
    PROGRESSIVE_BOW,
    PROGRESSIVE_BEETLE,
    PROGRESSIVE_SLINGSHOT,
    PROGRESSIVE_MITTS,
    PROGRESSIVE_POUCH,
    BOMB_BAG,
    CLAWSHOTS,
    WHIP,
    GUST_BELLOWS,
    WATER_SCALE,
    FIRESHIELD_EARRINGS,
    GODDESS_HARP,
    SPIRAL_CHARGE,
    # SAILCLOTH
]

ALLOWED_STARTING_ITEMS = (
    ITEM_FLAGS
    | PROGRESSIVE_SWORDS
    | PROGRESSIVE_POUCHES
    | PROGRESSIVE_MITTS_ALL
    | PROGRESSIVE_SLINGSHOTS
    | PROGRESSIVE_BEETLES
    | PROGRESSIVE_BOWS
    | PROGRESSIVE_BUG_NETS
    | PROGRESSIVE_WALLETS
    | HEART_CONTAINERS
    | HEART_PIECES
    | KEY_PIECES
    | ALL_SMALL_KEYS
    | ALL_BOSS_KEYS
    | ALL_MAPS
)
