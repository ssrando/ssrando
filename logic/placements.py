from typing import Any, List
from .constants import *
from .logic import Placement

# Single crystals
SINGLE_CRYSTAL_CHECKS = [
    "Upper Skyloft - Crystal in Link's Room",
    "Upper Skyloft - Crystal in Knight Academy Plant",
    "Upper Skyloft - Crystal in Zelda's Room",
    "Upper Skyloft - Crystal in Sparring Hall",
    "Central Skyloft - Crystal between Wooden Planks",
    "Central Skyloft - Crystal on West Cliff",
    "Central Skyloft - Crystal in Orielle and Parrow's House",
    "Central Skyloft - Crystal on Light Tower",
    "Skyloft Village - Crystal near Pumpkin Patch",
    "Central Skyloft - Crystal after Waterfall Cave",
    "Central Skyloft - Crystal in Loftwing Prison",
    "Central Skyloft - Crystal on Waterfall Island",
    "Sky - Crystal outside Lumpy Pumpkin",
    "Sky - Crystal inside Lumpy Pumpkin",
    "Sky - Crystal on Beedle's Ship",
]


def norm_vanilla(list: List[str]):
    def norm_keys(norm: Callable[[str], EIN], checks: Dict[EIN, Any]) -> Placement:
        list2 = map(norm, list)
        dict = {k: EIN(checks[k]["original item"]) for k in list2}
        return Placement(locations=dict, items={v: k for k, v in dict.items()})

    return norm_keys


SINGLE_CRYSTAL_PLACEMENT = norm_vanilla(SINGLE_CRYSTAL_CHECKS)


def norm_keys(dict: Dict[str, EIN]):
    def norm_keys(norm: Callable[[str], EIN]) -> Placement:
        dict2 = {norm(k): v for k, v in dict.items()}
        return Placement(locations=dict2, items={v: k for k, v in dict2.items()})

    return norm_keys


def norm_values(dict: Dict[EIN, str]):
    def norm_values(norm: Callable[[str], EIN]):
        dict2 = {k: norm(v) for k, v in dict.items()}
        return Placement(item_placement_limit=dict2)

    return norm_values


HARDCODED_PLACEMENT = norm_keys({})

BEEDLE_CHECKS = [
    "Beedle's Shop - 300 Rupee Item",
    "Beedle's Shop - 600 Rupee Item",
    "Beedle's Shop - 1200 Rupee Item",
    "Beedle's Shop - 800 Rupee Item",
    "Beedle's Shop - 1600 Rupee Item",
    "Beedle's Shop - First 100 Rupee Item",
    "Beedle's Shop - Second 100 Rupee Item",
    "Beedle's Shop - Third 100 Rupee Item",
    "Beedle's Shop - 50 Rupee Item",
    "Beedle's Shop - 1000 Rupee Item",
]
VANILLA_BEEDLE_PLACEMENT = norm_vanilla(BEEDLE_CHECKS)

SMALL_KEY_CHECKS = [
    "Skyview - Chest behind Two Eyes",
    "Skyview - Chest behind Three Eyes",
    "Lanayru Mining Facility - Big Hub - Chest",
    "Ancient Cistern - East Part - Chest",
    "Ancient Cistern - Basement Gutters - Bokoblin",
    "Sandship - Chest behind Combination Lock",
    "Sandship - Brig Prison - Robot's Reward",
    "Fire Sanctuary - First Room - Chest",
    "Fire Sanctuary - First Trapped Mogma Room - Chest",
    "Fire Sanctuary - Second Trapped Mogma Room - Chest",
    "Sky Keep - Chest after Dreadfuse",
    "Lanayru Caves - Golo's Gift",
]
VANILLA_SMALL_KEYS_PLACEMENT = norm_vanilla(SMALL_KEY_CHECKS)

DUNGEON_SMALL_KEYS_RESTRICTION = norm_values(
    {
        number(SMALL_KEY[SV], 0): SV + sep + "Main",
        number(SMALL_KEY[SV], 1): SV + sep + "Main",
        number(SMALL_KEY[LMF], 0): LMF + sep + "Main",
        number(SMALL_KEY[AC], 0): AC + sep + "Main",
        number(SMALL_KEY[AC], 1): AC + sep + "Main",
        number(SMALL_KEY[SSH], 0): SSH + sep + "Main",
        number(SMALL_KEY[SSH], 1): SSH + sep + "Main",
        number(SMALL_KEY[FS], 0): FS + sep + "Main",
        number(SMALL_KEY[FS], 1): FS + sep + "Main",
        number(SMALL_KEY[FS], 2): FS + sep + "Main",
        number(SMALL_KEY[SK], 0): SK,
    }
)

CAVES_KEY_RESTRICTION = norm_values({CAVES_KEY: "Lanayru - Caves"})


BOSS_KEY_CHECKS = [
    "Skyview - Boss Key Chest",
    "Earth Temple - Boss Key Chest",
    "Lanayru Mining Facility - Boss Key Chest",
    "Ancient Cistern - Boss Key Chest",
    "Sandship - Boss Key Chest",
    "Fire Sanctuary - Boss Key Chest",
]
VANILLA_BOSS_KEYS_PLACEMENT = norm_vanilla(BOSS_KEY_CHECKS)

DUNGEON_BOSS_KEYS_RESTRICTION = norm_values(
    {
        BOSS_KEY[SV]: SV,
        BOSS_KEY[ET]: ET,
        BOSS_KEY[LMF]: LMF,
        BOSS_KEY[AC]: AC,
        BOSS_KEY[SSH]: SSH,
        BOSS_KEY[FS]: FS,
    }
)

MAP_CHECKS = [
    "Skyview - Chest on Tree Branch",
    "Earth Temple - West Room - Chest",
    "Lanayru Mining Facility - Armos Fight Room - Chest",
    "Ancient Cistern - After Whip Hooks - Chest",
    "Sandship - Chest before 4-Door Corridor",
    "Fire Sanctuary - Second Trapped Mogma Room - Reward",
    "Sky Keep - First Chest",
]
VANILLA_MAPS_PLACEMENT = norm_vanilla(MAP_CHECKS)

DUNGEON_MAPS_RESTRICTION = norm_values(
    {
        MAP[SV]: SV,
        MAP[ET]: ET,
        MAP[LMF]: LMF,
        MAP[AC]: AC,
        MAP[SSH]: SSH,
        MAP[FS]: FS,
        MAP[SK]: SK,
    }
)
DUNGEON_MAPS_RESTRICTED_RESTRICTION = norm_values(
    {
        MAP[SV]: SV + sep + "Main",
        MAP[ET]: ET + sep + "Main",
        MAP[LMF]: LMF + sep + "Main",
        MAP[AC]: AC + sep + "Main",
        MAP[SSH]: SSH + sep + "Main",
        MAP[FS]: FS + sep + "Main",
        MAP[SK]: SK + sep + "Main",
    }
)

VANILLA_TRIFORCES_PLACEMENT = norm_values(
    {
        TRIFORCE_OF_COURAGE: "Sky Keep - Triforce of Courage",
        TRIFORCE_OF_WISDOM: "Sky Keep - Triforce of Wisdom",
        TRIFORCE_OF_POWER: "Sky Keep - Triforce of Power",
    }
)

TRIFORCES_RESTRICTION = norm_values(
    {TRIFORCE_OF_COURAGE: SK, TRIFORCE_OF_WISDOM: SK, TRIFORCE_OF_POWER: SK}
)


VANILLA_RUPEES = norm_vanilla(RUPEE_CHECKS)
VANILLA_QUICK_BEETLE_RUPEES = norm_vanilla(QUICK_BEETLE_CHECKS)
