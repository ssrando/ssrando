from pathlib import Path
import random
from collections import OrderedDict, defaultdict
from pprint import pprint

import yaml
import json
from io import BytesIO
from enum import IntEnum
from typing import Optional
import re
import struct

import nlzss11
from sslib import AllPatcher, U8File
from sslib.msb import process_control_sequences
from sslib.utils import write_bytes_create_dirs, encodeBytes
from sslib.fs_helpers import write_str, write_u16, write_float
from sslib.dol import DOL
from sslib.rel import REL
from paths import RANDO_ROOT_PATH
from tboxSubtypes import tboxSubtypes
from musicrando import music_rando

from logic.logic import Logic
from logic.constants import SILENT_REALM_CHECKS

from asm.patcher import apply_dol_patch, apply_rel_patch

from util.textbox_utils import break_lines, break_and_make_multiple_textboxes

TOTAL_STAGE_FILES = 369
TOTAL_EVENT_FILES = 6

# arc cache, main.dol, rels, objectpack
GAMEPATCH_TOTAL_STEP_COUNT = TOTAL_EVENT_FILES + TOTAL_STAGE_FILES + 4

DEFAULT_SOBJ = OrderedDict(
    params1=0,
    params2=0,
    posx=0,
    posy=0,
    posz=0,
    sizex=0,
    sizey=0,
    sizez=0,
    anglex=0,
    angley=0,
    anglez=0,
    id=0,
    name="",
)

DEFAULT_OBJ = OrderedDict(
    params1=0,
    params2=0,
    posx=0,
    posy=0,
    posz=0,
    anglex=0,
    angley=0,
    anglez=0,
    id=0,
    name="",
)

DEFAULT_SCEN = OrderedDict(
    name="", room=0, layer=0, entrance=0, byte4=0, byte5=0, flag6=0, zero=0, flag8=0
)

DEFAULT_AREA = OrderedDict(
    posx=0,
    posy=0,
    posz=0,
    sizex=0,
    sizey=0,
    sizez=0,
    angle=0,
    area_link=-1,
    unk3=0,
    dummy=b"\xFF\xFF\xFF",
)

# cutscenes to use to set storyflags, sceneflags and itemflags
START_CUTSCENES = [
    # stage, room, eventindex
    ("F000", 0, 22),
    ("F000", 0, 23),
    ("F001r", 1, 2),
    ("F405", 0, 0),
]

START_ITEM_STORYFLAGS = {
    "Emerald Tablet": 46,
    "Ruby Tablet": 47,
    "Amber Tablet": 48,
}

# The stage name of each dungeon
DUNGEON_STAGES = {
    "Skyview": "D100",
    "Ancient Cistern": "D101",
    "Earth Temple": "D200",
    "Fire Sanctuary": "D201",
    "Lanayru Mining Facility": "D300",
    "Sandship": "D301",
    "Sky Keep": "D003_7",
}

# The stage for each map where there are dungeon entrances
DUNGEON_ENTRANCE_STAGES = {
    # stage, room, scen
    "Dungeon Entrance in Deep Woods": ("F101", 0, 1),
    "Dungeon Entrance in Lake Floria": ("F102_1", 0, 1),
    "Dungeon Entrance in Eldin Volcano": ("F200", 4, 0),
    "Dungeon Entrance in Volcano Summit": ("F201_3", 0, 1),
    "Dungeon Entrance in Lanayru Desert": ("F300", 0, 5),
    "Dungeon Entrance in Sand Sea": ("F301_1", 0, 1),
    "Dungeon Entrance on Skyloft": ("F000", 0, 48),
}

DUNGEON_EXITS = {
    # stage, layer, room, entrance
    "Dungeon Entrance in Deep Woods": ("F101", 0, 0, 1),
    "Dungeon Entrance in Lake Floria": ("F102_1", 0, 0, 1),
    "Dungeon Entrance in Eldin Volcano": ("F200", 0, 4, 1),
    "Dungeon Entrance in Volcano Summit": ("F201_3", 0, 0, 1),
    "Dungeon Entrance in Lanayru Desert": ("F300", 0, 0, 5),
    "Dungeon Entrance in Sand Sea": ("F301_1", 0, 0, 4),
    "Dungeon Entrance on Skyloft": ("F000", 0, 0, 53),
}

DUNGEON_FINISH_EXITS = {
    # stage, layer, room, entrance
    "Dungeon Entrance in Deep Woods": ("F101", 0, 0, 1),
    "Dungeon Entrance in Lake Floria": ("F102_1", 0, 0, 6),
    "Dungeon Entrance in Eldin Volcano": ("F200", 0, 4, 1),
    "Dungeon Entrance in Volcano Summit": ("F201_3", 0, 0, 1),
    "Dungeon Entrance in Lanayru Desert": ("F300_4", 2, 0, 2),
    "Dungeon Entrance in Sand Sea": ("F301", 0, 0, 3),
    "Dungeon Entrance on Skyloft": ("F000", 0, 0, 52),
}

DUNGEON_ENTRANCES = {
    # stage, layer, room, entrance
    "Skyview": ("D100", 0, 0, 0),
    "Earth Temple": ("D200", 0, 1, 0),
    "Lanayru Mining Facility": ("D300", 0, 0, 0),
    "Ancient Cistern": ("D101", 0, 0, 0),
    "Sandship": ("D301", 1, 0, 0),
    "Fire Sanctuary": ("D201", 0, 0, 0),
    "Sky Keep": ("D003_7", 0, 0, 4),
}

DUNGEON_FINISH_EXIT_SCEN = {
    # stage, room, index
    "Skyview": ("B100_1", 0, 1),
    "Earth Temple": ("B210", 0, 0),
    "Lanayru Mining Facility": ("F300_4", 0, 3),
    "Ancient Cistern": ("B101_1", 0, 3),
    "Sandship": ("B301", 0, 4),
    "Fire Sanctuary": ("B201_1", 0, 2),
    "Sky Keep": ("F407", 0, 1),
}

DUNGEON_EXIT_SCENS = {
    # stage, room, index
    "Skyview": [
        ("D100", 0, 0),
        ("D100", 0, 2),
        ("D100", 2, 0),
        ("D100", 5, 0),
        ("D100", 9, 0),
        ("B100_1", 0, 4),
    ],
    "Earth Temple": [("D200", 1, 0), ("D200", 1, 1), ("D200", 2, 0), ("D200", 4, 2)],
    "Lanayru Mining Facility": [
        ("D300", 0, 0),
        ("D300", 0, 1),
        ("D300", 5, 4),
        ("D300_1", 0, 0),
        ("D300_1", 0, 1),
        ("D300_1", 5, 4),
        ("B300", 0, 1),
        ("F300_5", 0, 3),  # extra bird statue
    ],
    "Ancient Cistern": [
        ("D101", 0, 2),
        ("D101", 0, 3),
        ("D101", 3, 1),
        ("D101", 4, 2),
        ("D101", 5, 0),
        # ('B101_1', 0, 1)
    ],
    "Sandship": [
        ("D301", 0, 0),
        ("D301", 0, 1),
        ("D301", 1, 2),
        ("D301", 2, 0),
        ("D301", 6, 0),
        ("D301", 9, 1),
        ("D301", 12, 0),
        ("D301", 13, 0),
        ("B301", 0, 1),
    ],
    "Fire Sanctuary": [
        ("D201", 0, 1),
        ("D201", 3, 2),
        ("D201", 10, 2),
        ("D201_1", 1, 0),
        ("D201_1", 7, 0),
        ("D201_1", 5, 3),
        ("D201_1", 6, 2),
    ],
    "Sky Keep": [
        ("D003_0", 0, 3),  # most of them not needed
        ("D003_1", 0, 2),
        ("D003_2", 0, 3),
        ("D003_3", 0, 3),
        ("D003_4", 0, 2),
        ("D003_5", 0, 2),
        ("D003_6", 0, 2),
        ("D003_7", 0, 2),
        ("D003_0", 0, 1),  # most of them not needed
        ("D003_1", 0, 1),
        ("D003_2", 0, 1),
        ("D003_3", 0, 1),
        ("D003_4", 0, 1),
        ("D003_5", 0, 1),
        ("D003_6", 0, 1),
        ("D003_7", 0, 1),
    ],
}

# fixes for entrance rando, ET, SSH and SK don't need to set storyflags at all
# for LMF it's the ToT layer change
POST_DUNGEON_STORYFLAGS = {
    "Dungeon Entrance in Deep Woods": 5,
    "Dungeon Entrance in Lake Floria": 900,
    "Dungeon Entrance in Eldin Volcano": -1,
    "Dungeon Entrance in Volcano Summit": 901,
    "Dungeon Entrance in Lanayru Desert": 914,
    "Dungeon Entrance in Sand Sea": -1,
    "Dungeon Entrance on Skyloft": -1,
}

POST_DUNGEON_CUTSCENE = {
    # (stage, room, EVNT)
    "Skyview": ("B100_1", 0, 1),
    "Earth Temple": ("B210", 0, 2),
    "Lanayru Mining Facility": ("F300_4", 0, 20),
    "Ancient Cistern": ("B101_1", 0, 1),
    "Sandship": ("B301", 0, 1),
    "Fire Sanctuary": ("B201_1", 0, 0),
    "Sky Keep": ("F000", 0, 19),
}

TRIAL_GATE_TO_TRIAL = {
    "Trial Gate on Skyloft": "Skyloft Silent Realm",
    "Trial Gate in Faron Woods": "Faron Silent Realm",
    "Trial Gate in Eldin Volcano": "Eldin Silent Realm",
    "Trial Gate in Lanayru Desert": "Lanayru Silent Realm",
}

TRIAL_STAGES = {
    "Skyloft Silent Realm": "S000",
    "Faron Silent Realm": "S100",
    "Eldin Silent Realm": "S200",
    "Lanayru Silent Realm": "S300",
}

TRIAL_GATE_STAGES = {
    # stage, room, scen
    "Trial Gate on Skyloft": ("F000", 0, 45),
    "Trial Gate in Faron Woods": ("F100", 0, 8),
    "Trial Gate in Eldin Volcano": ("F200", 2, 4),
    "Trial Gate in Lanayru Desert": ("F300", 0, 7),
}

TRIAL_EXITS = {
    # stage, layer, room, entrance
    "Trial Gate on Skyloft": ("F000", 0, 0, 83),
    "Trial Gate in Faron Woods": ("F100", 0, 0, 48),
    "Trial Gate in Eldin Volcano": ("F200", 0, 2, 5),
    "Trial Gate in Lanayru Desert": ("F300", 0, 0, 4),
}

TRIAL_ENTRANCES = {
    # stage, layer, room, entrance
    # all trials are layer 2
    "Skyloft Silent Realm": ("S000", 2, 0, 0),
    "Faron Silent Realm": ("S100", 2, 0, 0),
    "Eldin Silent Realm": ("S200", 2, 2, 0),
    "Lanayru Silent Realm": ("S300", 2, 0, 0),
}

TRIAL_EXIT_SCENS = {
    # stage, room, index
    "Skyloft Silent Realm": ("S000", 0, 1),
    "Faron Silent Realm": ("S100", 0, 1),
    "Eldin Silent Realm": ("S200", 2, 1),
    "Lanayru Silent Realm": ("S300", 0, 1),
}

TRIAL_EXIT_GATE_IDS = {
    # silent realm name, silent realm WarpObj ID
    "Skyloft Silent Realm": 0xFC26,
    "Faron Silent Realm": 0xFC94,
    "Eldin Silent Realm": 0xFC37,
    "Lanayru Silent Realm": 0xFC18,
}

TRIAL_COMPLETE_STORYFLAGS = {
    # trial gate, storyflag
    "Trial Gate on Skyloft": 0x39A,
    "Trial Gate in Faron Woods": 0x397,
    "Trial Gate in Eldin Volcano": 0x398,
    "Trial Gate in Lanayru Desert": 0x399,
}

BEEDLE_TEXT_PATCHES = {  # (undiscounted, discounted, normal price, discounted price)
    "Beedle - 50 Rupee Item": (25, 26, 50, 25),
    "Beedle - First 100 Rupee Item": (23, 24, 100, 50),
    "Beedle - Second 100 Rupee Item": (
        "Second 100R undiscounted Text",
        "Second 100R discounted Text",
        100,
        50,
    ),
    "Beedle - Third 100 Rupee Item": (
        "Third 100R undiscounted Text",
        "Third 100R discounted Text",
        100,
        50,
    ),
    "Beedle - 300 Rupee Item": (19, 20, 300, 150),
    "Beedle - 600 Rupee Item": (29, 30, 600, 300),
    "Beedle - 800 Rupee Item": (27, 28, 800, 400),
    "Beedle - 1000 Rupee Item": (33, 34, 1000, 500),
    "Beedle - 1200 Rupee Item": (31, 32, 1200, 600),
    "Beedle - 1600 Rupee Item": (21, 22, 1600, 800),
}

BEEDLE_BUY_SWTICH = "[1]I'll buy it![2-]No, thanks."

PROGRESSIVE_SWORD_STORYFLAGS = [906, 907, 908, 909, 910, 911]
PROGRESSIVE_SWORD_ITEMIDS = [10, 11, 12, 9, 13, 14]


class FlagEventTypes(IntEnum):
    SET_STORYFLAG = (0,)
    UNSET_STORYFLAG = (1,)
    SET_SCENEFLAG = (2,)
    UNSET_SCENEFLAG = (3,)
    SET_ZONEFLAG = (4,)
    UNSET_ZONEFLAG = (5,)
    SET_TEMPFLAG = (28,)
    UNSET_TEMPFLAG = (29,)


class FlagSwitchTypes(IntEnum):
    CHOICE = (0,)
    STORYFLAG = (3,)
    ZONEFLAG = (5,)
    SCENEFLAG = (6,)
    TEMPFLAG = (9,)


FLAGINDEX_NAMES = [
    "Skyloft",
    "Faron Woods",
    "Lake Floria",
    "Flooded Faron Woods",
    "Eldin Volcano",
    "Eldin Volcano Summit",
    "-Unused-",
    "Lanayru Desert",
    "Lanayru Sand Sea",
    "Lanayru Gorge",
    "Sealed Grounds",
    "Skyview Temple",
    "Ancient Cistern",
    "-Unused-",
    "Earth Temple",
    "Fire Sanctuary",
    "-Unused-",
    "Mining Facility",
    "Sandship",
    "-Unused-",
    "Sky Keep",
    "The Sky",
    "Faron Silent Realm",
    "Eldin Silent Realm",
    "Lanayru Silent Realm",
    "Skyloft Silent Realm",
]


def entrypoint_hash(name: str, entries: int) -> int:
    hash = 0
    for char in name:
        hash = (hash * 0x492 + ord(char)) & 0xFFFFFFFF
    return hash % entries


def make_switch(subtype: FlagSwitchTypes, arg: int):
    if subtype == FlagSwitchTypes.CHOICE:
        p2 = 0
        p3 = arg  # number of choices
    else:
        p2 = arg
        p3 = subtype.value
    return OrderedDict(
        type="switch",
        subType=6,
        param1=0,
        param2=p2,
        next=-1,
        param3=p3,
        param4=-1,
        param5=-1,
    )


def make_give_item_event(item):
    return OrderedDict(
        type="type3",
        subType=0,
        param1=0,
        param2=item,
        next=-1,
        param3=9,
        param4=0,
        param5=0,
    )


def make_flag_event(subtype: FlagEventTypes, flag):
    if (
        subtype == FlagEventTypes.SET_STORYFLAG
        or subtype == FlagEventTypes.UNSET_STORYFLAG
    ):
        st = 0
        p1 = 0
        p2 = flag
    else:
        st = 1
        p1 = flag
        p2 = 0
    return OrderedDict(
        type="type3",
        subType=st,
        param1=p1,
        param2=p2,
        next=-1,
        param3=subtype.value,
        param4=0,
        param5=0,
    )


def add_msbf_branch(msbf, switch, branchpoints):
    branch_index = len(msbf["FLW3"]["branch_points"])
    msbf["FLW3"]["branch_points"].extend(branchpoints)
    switch["param4"] = len(branchpoints)
    switch["param5"] = branch_index
    msbf["FLW3"]["flow"].append(switch)


def make_progressive_item(
    msbf, base_item_start, item_text_indexes, item_ids, storyflags
):
    if len(item_text_indexes) != len(storyflags) or len(item_text_indexes) != len(
        item_ids
    ):
        raise Exception("item_text_indexes should be the same length as storyflags!")
    flow_idx = len(msbf["FLW3"]["flow"])
    msbf["FLW3"]["flow"][base_item_start]["next"] = flow_idx
    index = len(item_text_indexes) - 1  # start from the highest upgrade
    # first, check if the storyflag of the previous upgrade is set
    # if yes, set the storyflag for this upgrade, give the upgrade and jump to that upgrade's text
    # otherwise check the next upgrade storyflag. If no storyflag is set, set the lowest upgrades storyflag
    # but no need to give that item since it's that items event that is hijacked
    for index in range(len(item_text_indexes) - 1, 0, -1):
        branch = make_switch(FlagSwitchTypes.STORYFLAG, storyflags[index - 1])
        add_msbf_branch(msbf, branch, [flow_idx + 1, flow_idx + 3])
        event = make_give_item_event(item_ids[index])
        event["next"] = flow_idx + 2
        msbf["FLW3"]["flow"].append(event)
        event = make_flag_event(FlagEventTypes.SET_STORYFLAG, storyflags[index])
        event["next"] = item_text_indexes[index]
        msbf["FLW3"]["flow"].append(event)
        flow_idx += 3
    event = make_flag_event(FlagEventTypes.SET_STORYFLAG, storyflags[0])
    event["next"] = item_text_indexes[0]
    msbf["FLW3"]["flow"].append(event)


# check highest
def highest_objid(bzs):
    max_id = 0
    for layer in bzs.get("LAY ", {}).values():
        if len(layer) == 0:
            continue
        for objtype in ["OBJS", "OBJ ", "SOBS", "SOBJ", "STAS", "STAG", "SNDT", "DOOR"]:
            if objtype in layer:
                id = layer[objtype][-1]["id"] & 0x3FF
                if id != 0x3FF:  # aparently some objects have the max id?
                    max_id = max(max_id, id)
    return max_id


def mask_shift_set(value, mask, shift, new_value):
    """
    Replace new_value in value, by applying the mask after the shift
    """
    new_value = new_value & mask
    return (value & ~(mask << shift)) | (new_value << shift)


def try_patch_obj(obj, key, value):
    if obj["name"].startswith("Npc"):
        if key == "trigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 10, value)
        elif key == "untrigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 21, value)
        elif key == "talk_behaviour":
            obj["anglez"] = value
        elif obj["name"] == "NpcTke":
            if key == "trigscenefid":
                obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 0, value)
            elif key == "untrigscenefid":
                obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 8, value)
            elif key == "subtype":
                obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
            else:
                print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj["name"] == "TBox":
        if key == "spawnscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 20, value)
        elif key == "setscenefid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0xFF, 0, value)
        elif key == "itemid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x1FF, 0, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj["name"] == "EvntTag":
        if key == "trigscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 16, value)
        elif key == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 8, value)
        elif key == "event":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj["name"] == "EvfTag":
        if key == "trigstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 19, value)
        elif key == "setstoryfid":
            obj["params1"] = mask_shift_set(obj["params1"], 0x7FF, 8, value)
        elif key == "event":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj["name"] == "ScChang":
        if key == "trigstoryfid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0x7FF, 0, value)
        elif key == "untrigstoryfid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x7FF, 0, value)
        elif key == "scen_link":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        elif key == "trigscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 24, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj["name"] == "SwAreaT":
        if key == "setstoryfid":
            obj["anglex"] = mask_shift_set(obj["anglex"], 0x7FF, 0, value)
        elif key == "unsetstoryfid":
            obj["anglez"] = mask_shift_set(obj["anglez"], 0x7FF, 0, value)
        elif key == "setscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0, value)
        elif key == "unsetscenefid":
            obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 8, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    else:
        print(f"ERROR: unsupported object to patch {obj}")


def patch_tbox_item(tbox: OrderedDict, itemid: int):
    origitemid = tbox["anglez"] & 0x1FF
    boxtype = tboxSubtypes[origitemid]
    tbox["anglez"] = mask_shift_set(tbox["anglez"], 0x1FF, 0, itemid)
    # code has been patched, to interpret this part of params1 as boxtype
    tbox["params1"] = mask_shift_set(tbox["params1"], 0x3, 4, boxtype)


def patch_item_item(itemobj: OrderedDict, itemid: int):
    itemobj["params1"] = mask_shift_set(itemobj["params1"], 0xFF, 0, itemid)
    # subtype 9, this acts like hearpieces and force being collected with a textbox
    itemobj["params1"] = mask_shift_set(itemobj["params1"], 0xF, 0x14, 9)


# these are not treasure chests, but instead only used for the hp in zeldas room
def patch_chest_item(chest: OrderedDict, itemid: int):
    chest["params1"] = mask_shift_set(chest["params1"], 0xFF, 8, itemid)


# code has been patched to use this part of params1 as itemid
def patch_heart_co(heart_co: OrderedDict, itemid: int):
    heart_co["params1"] = mask_shift_set(heart_co["params1"], 0xFF, 16, itemid)


# code has been patched to use this part of params1 as itemid
def patch_chandelier_item(chandel: OrderedDict, itemid: int):
    chandel["params1"] = mask_shift_set(chandel["params1"], 0xFF, 8, itemid)


def patch_soil_item(soil: OrderedDict, itemid: int):
    # match key piece soils in all ways but keep sceneflag
    soil["params1"] = (soil["params1"] & 0xFF0) | 0xFF0B1004
    # code has been patched to use the first byte of params2 as itemid, but only
    # if it would have been a key piece otherwise
    soil["params2"] = mask_shift_set(soil["params2"], 0xFF, 0x18, itemid)


def patch_trial_item(trial: OrderedDict, itemid: int):
    trial["params1"] = mask_shift_set(trial["params1"], 0xFF, 0x18, itemid)


def patch_trial_flags(trial: OrderedDict, storyflag: int):
    # Use last 2 bytes of params2 as the randomized trial storyflag
    trial["params2"] = mask_shift_set(trial["params2"], 0xFFFF, 0x0, storyflag)


def patch_key_bokoblin_item(boko: OrderedDict, itemid: int):
    boko["params2"] = mask_shift_set(boko["params2"], 0xFF, 0x0, itemid)


# not treasure chest, wardrobes you can open, used for zelda room HP
def rando_patch_chest(bzs: OrderedDict, itemid: int, id: str):
    id = int(id)
    chest = next(
        filter(
            lambda x: x["name"] == "chest" and (x["params1"] & 0xFF) == id, bzs["OBJ "]
        )
    )
    patch_chest_item(chest, itemid)


def rando_patch_heartco(bzs: OrderedDict, itemid: int, id: str):
    obj = next(
        filter(lambda x: x["name"] == "HeartCo", bzs["OBJ "])
    )  # there is only one heart container at a time
    patch_heart_co(obj, itemid)


def rando_patch_warpobj(
    bzs: OrderedDict, itemid: int, id: str, trial_connections: OrderedDict
):
    obj = next(
        filter(lambda x: x["name"] == "WarpObj", bzs["OBJ "])
    )  # there is only one trial exit at a time
    patch_trial_item(obj, itemid)
    for trial, trialid in TRIAL_EXIT_GATE_IDS.items():
        if obj["id"] == trialid:
            trial_gate = [tg for tg, t in trial_connections.items() if t == trial].pop()
            trial_storyflag = TRIAL_COMPLETE_STORYFLAGS[trial_gate]
    patch_trial_flags(obj, trial_storyflag)


def rando_patch_tbox(bzs: OrderedDict, itemid: int, id: str):
    id = int(id)
    tboxs = list(
        filter(lambda x: x["name"] == "TBox" and (x["anglez"] >> 9) == id, bzs["OBJS"])
    )
    if len(tboxs) == 0:
        print(tboxs)
    obj = tboxs[0]  # anglez >> 9 is chest id
    patch_tbox_item(obj, itemid)


def rando_patch_item(bzs: OrderedDict, itemid: int, id: str):
    id = int(id)
    obj = next(
        filter(
            lambda x: x["name"] == "Item" and ((x["params1"] >> 10) & 0xFF) == id,
            bzs["OBJ "],
        )
    )  # (params1 >> 10) & 0xFF is sceneflag
    patch_item_item(obj, itemid)


def rando_patch_chandelier(bzs: OrderedDict, itemid: int, id: str):
    obj = next(filter(lambda x: x["name"] == "Chandel", bzs["OBJ "]))
    patch_chandelier_item(obj, itemid)


def rando_patch_soil(bzs: OrderedDict, itemid: int, id: str):
    id = int(id)
    obj = next(
        filter(
            lambda x: x["name"] == "Soil" and ((x["params1"] >> 4) & 0xFF) == id,
            bzs["OBJ "],
        )
    )  # (params1 >> 4) & 0xFF is sceneflag
    patch_soil_item(obj, itemid)


def rando_patch_bokoblin(bzs: OrderedDict, itemid: int, id: str):
    id = int(id, 0)
    obj = next(filter(lambda x: x["name"] == "EBc" and x["id"] == id, bzs["OBJ "]))
    patch_key_bokoblin_item(obj, itemid)


def rando_patch_goddess_crest(bzs: OrderedDict, itemid: int, index: str):
    obj = next(filter(lambda x: x["name"] == "SwSB", bzs["OBJ "]))
    # we need to patch 3 item ids into this object:
    # 1 is params1 FF 00 00 00, 2 is params1 00 FF 00 00
    # 3 is params2 FF 00 00 00
    if index == "0":
        obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0x18, itemid)
    elif index == "1":
        obj["params1"] = mask_shift_set(obj["params1"], 0xFF, 0x10, itemid)
    elif index == "2":
        obj["params2"] = mask_shift_set(obj["params2"], 0xFF, 0x18, itemid)


# functions, that patch the object, they take: the bzs of that layer, the item id and optionally an id, then patches the object in place
RANDO_PATCH_FUNCS = {
    "chest": rando_patch_chest,
    "HeartCo": rando_patch_heartco,
    "WarpObj": rando_patch_warpobj,
    "TBox": rando_patch_tbox,
    "Item": rando_patch_item,
    "Chandel": rando_patch_chandelier,
    "Soil": rando_patch_soil,
    "EBc": rando_patch_bokoblin,
    "Tbox": rando_patch_tbox,
    "SwSB": rando_patch_goddess_crest,
}


def get_patches_from_location_item_list(all_checks, filled_checks):
    with (RANDO_ROOT_PATH / "items.yaml").open() as f:
        items = yaml.safe_load(f)
    by_item_name = dict((x["name"], x) for x in items)

    # (stage, room) -> (object name, layer, id?, itemid)
    stagepatchv2 = defaultdict(list)
    # (stage, layer) -> oarc
    stageoarcs = defaultdict(set)
    # # eventfile: (line, itemid)
    eventpatches = defaultdict(list)
    # shopindex: (itemid, arcname, modelname)
    shoppatches = {}

    stage_re = re.compile(
        r"stage/(?P<stage>[^/]+)/r(?P<room>[0-9]+)/l(?P<layer>[0-9]+)/(?P<objname>[a-zA-Z]+)(/(?P<objid>[^/]+))?"
    )
    event_re = re.compile(r"event/(?P<eventfile>[^/]+)/(?P<eventid>[^/]+)")
    oarc_re = re.compile(r"oarc/(?P<stage>[^/]+)/l(?P<layer>[^/]+)")
    shop_smpl_re = re.compile(r"ShpSmpl/(?P<index>[0-9]+)")

    for checkname, itemname in filled_checks.items():
        # single gratitude crystals aren't randomized
        if itemname == "Gratitude Crystal":
            continue
        check = all_checks[checkname]
        item = by_item_name[itemname]
        for path in check["Paths"]:
            stage_match = stage_re.match(path)
            event_match = event_re.match(path)
            oarc_match = oarc_re.match(path)
            shop_smpl_match = shop_smpl_re.match(path)
            if stage_match:
                stage = stage_match.group("stage")
                room = int(stage_match.group("room"))
                layer = int(stage_match.group("layer"))
                objname = stage_match.group("objname")
                objid = stage_match.group("objid")
                oarc = item["oarc"]
                if oarc:
                    if isinstance(oarc, list):
                        for o in oarc:
                            stageoarcs[(stage, layer)].add(o)
                    else:
                        stageoarcs[(stage, layer)].add(oarc)
                stagepatchv2[(stage, room)].append((objname, layer, objid, item["id"]))
            elif event_match:
                eventfile = event_match.group("eventfile")
                eventid = event_match.group("eventid")
                eventpatches[eventfile].append((eventid, item["id"]))
            elif oarc_match:
                stage = oarc_match.group("stage")
                layer = int(oarc_match.group("layer"))
                oarc = item["oarc"]
                if oarc:
                    if isinstance(oarc, list):
                        for o in oarc:
                            stageoarcs[(stage, layer)].add(o)
                    else:
                        stageoarcs[(stage, layer)].add(oarc)
            elif shop_smpl_match:
                index = int(shop_smpl_match.group("index"))
                # TODO: super fix this, add all models/arcs to items.yaml
                arcname = item.get("getarcname", None)
                modelname = item.get("getmodelname", None)
                oarc = item["oarc"]
                if oarc:
                    if isinstance(oarc, list):
                        for o in oarc:
                            stageoarcs[("F002r", 1)].add(o)
                    else:
                        stageoarcs[("F002r", 1)].add(oarc)
                if modelname is None or arcname is None:
                    raise Exception(f"no modelnames for {item}")
                shoppatches[index] = (item["id"], arcname, modelname)
            else:
                print(f"ERROR: {path} didn't match any regex!")
    return stagepatchv2, stageoarcs, eventpatches, shoppatches


def get_entry_from_bzs(
    bzs: OrderedDict, objdef: dict, remove: bool = False
) -> Optional[OrderedDict]:
    id = objdef.get("id", None)
    index = objdef.get("index", None)
    layer = objdef.get("layer", None)
    objtype = objdef["objtype"].ljust(
        4
    )  # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
    if layer is None:
        objlist = bzs[objtype]
    else:
        objlist = bzs["LAY "][f"l{layer}"][objtype]
    if not id is None:
        objs = [x for x in objlist if x["id"] == id]
        if len(objs) != 1:
            print(f"Error finding object: {json.dumps(objdef)}")
            return None
        obj = objs[0]
        if remove:
            objlist.remove(obj)
    elif not index is None:
        if index >= len(objlist):
            print(f"Error lisError list index out of range: {json.dumps(objdef)}")
            return None
        if remove:
            obj = objlist.pop(index)
        else:
            obj = objlist[index]
    else:
        print(f"ERROR: neither id nor index given for object {json.dumps(objdef)}")
        return None
    return obj


class GamePatcher:
    def __init__(self, rando, placement_file):
        self.rando = rando
        self.placement_file = placement_file
        self.patcher = AllPatcher(
            actual_extract_path=rando.actual_extract_path,
            modified_extract_path=rando.modified_extract_path,
            oarc_cache_path=rando.oarc_cache_path,
            copy_unmodified=False,
        )
        self.text_labels = {}

    def do_all_gamepatches(self):
        self.load_base_patches()
        self.add_entrance_rando_patches()
        self.add_trial_rando_patches()
        if self.placement_file.options["shop-mode"] != "Vanilla":
            self.shopsanity_patches()
        self.do_build_arc_cache()
        self.add_startitem_patches()
        self.add_required_dungeon_patches()
        if (self.placement_file.options["song-hints"]) != "None":
            self.add_trial_hint_patches()
        if self.placement_file.options["impa-sot-hint"]:
            self.add_impa_hint()
        self.add_stone_hint_patches()
        self.handle_oarc_add_remove()
        self.add_rando_hash()
        self.add_keysanity()

        self.patcher.set_bzs_patch(self.bzs_patch_func)
        self.patcher.set_event_patch(self.flow_patch)
        self.patcher.set_event_text_patch(self.text_patch)
        self.patcher.progress_callback = self.rando.progress_callback
        self.patcher.do_patch()

        self.do_dol_patch()
        self.do_rel_patch()
        self.do_patch_object_pack()
        self.do_patch_title_screen_logo()

        music_rando(self)

    def filter_option_requirement(self, entry):
        return not (
            isinstance(entry, dict)
            and "onlyif" in entry
            and not Logic.check_static_option_req(
                entry["onlyif"], self.placement_file.options
            )
        )

    def add_patch_to_stage(self, stage, stagepatch):
        if stage not in self.patches:
            self.patches[stage] = []
        self.patches[stage].append(stagepatch)

    # also used for text
    def add_patch_to_event(self, eventfile, eventpatch):
        if eventfile not in self.eventpatches:
            self.eventpatches[eventfile] = []
        self.eventpatches[eventfile].append(eventpatch)

    def load_base_patches(self):
        with (RANDO_ROOT_PATH / "patches.yaml").open() as f:
            self.patches = yaml.safe_load(f)
        with (RANDO_ROOT_PATH / "eventpatches.yaml").open() as f:
            self.eventpatches = yaml.safe_load(f)

        filtered_storyflags = []
        for storyflag in self.patches["global"]["startstoryflags"]:
            # conditionals are an object
            if not isinstance(storyflag, int):
                if self.filter_option_requirement(storyflag):
                    storyflag = storyflag["storyflag"]
                else:
                    continue
            filtered_storyflags.append(storyflag)
        self.startstoryflags = filtered_storyflags

        self.startitemflags = self.patches["global"]["startitems"]

        # patches from randomizing items
        (
            self.rando_stagepatches,
            self.stageoarcs,
            self.rando_eventpatches,
            self.shoppatches,
        ) = get_patches_from_location_item_list(
            self.rando.item_locations, self.placement_file.item_locations
        )

        # assembly patches
        self.all_asm_patches = defaultdict(OrderedDict)
        self.add_asm_patch("custom_funcs")
        self.add_asm_patch("ss_necessary")
        self.add_asm_patch("keysanity")
        if self.placement_file.options["shop-mode"] != "Vanilla":
            self.add_asm_patch("shopsanity")
        self.add_asm_patch("gossip_stone_hints")
        if self.placement_file.options["fix-bit-crashes"]:
            self.add_asm_patch("fix_bit_crashes")
        if self.placement_file.options["tunic-swap"]:
            self.add_asm_patch("tunic_swap")

        # GoT patch depends on required sword
        # cmpwi r0, (insert sword)
        GOT_SWORD_MODES = {
            "Goddess Sword": 1,
            "Goddess Longsword": 2,
            "Goddess Whitesword": 3,
            "Master Sword": 4,
            "True Master Sword": 5,
        }
        self.all_asm_patches["d_a_obj_time_door_beforeNP.rel"][0xD48] = {
            "Data": [
                0x2C,
                0x00,
                0x00,
                GOT_SWORD_MODES[self.placement_file.options["got-sword-requirement"]],
            ]
        }

        # for asm, custom symbols
        with (RANDO_ROOT_PATH / "asm" / "custom_symbols.txt").open("r") as f:
            self.custom_symbols = yaml.safe_load(f)
        self.main_custom_symbols = self.custom_symbols.get("main.dol", {})
        with (RANDO_ROOT_PATH / "asm" / "original_symbols.txt").open("r") as f:
            self.original_symbols = yaml.safe_load(f)
        self.main_original_symbols = self.original_symbols.get("main.dol", {})

        # for asm, free space start offset
        with (RANDO_ROOT_PATH / "asm" / "free_space_start_offsets.txt").open("r") as f:
            self.free_space_start_offsets = yaml.safe_load(f)

    def add_asm_patch(self, name):
        with (RANDO_ROOT_PATH / "asm" / "patch_diffs" / f"{name}_diff.txt").open(
            "r"
        ) as f:
            asm_patch_file_data = yaml.safe_load(f)
        for exec_file, patches in asm_patch_file_data.items():
            self.all_asm_patches[exec_file].update(patches)

    def add_entrance_rando_patches(self):
        for entrance, dungeon in self.placement_file.entrance_connections.items():
            entrance_stage, entrance_room, entrance_scen = DUNGEON_ENTRANCE_STAGES[
                entrance
            ]
            dungeon_stage, layer, room, entrance_index = DUNGEON_ENTRANCES[dungeon]
            # patch dungeon entrance
            self.add_patch_to_stage(
                entrance_stage,
                {
                    "name": f"Dungeon entrance patch - {entrance} to {dungeon}",
                    "type": "objpatch",
                    "index": entrance_scen,
                    "room": entrance_room,
                    "objtype": "SCEN",
                    "object": {
                        "name": dungeon_stage,
                        "layer": layer,
                        "room": room,
                        "entrance": entrance_index,
                    },
                },
            )

            # handle the extra loading zone to the dungeon in Sand Sea from Ancient Harbor
            # yes I know there was probably a better way to do this but it's a one off special case
            if entrance == "Dungeon Entrance in Sand Sea":
                self.add_patch_to_stage(
                    "F301",
                    {
                        "name": f"Dungeon entrance patch - Ancient Harbor to {dungeon}",
                        "type": "objpatch",
                        "index": 0,
                        "room": 0,
                        "objtype": "SCEN",
                        "object": {
                            "name": dungeon_stage,
                            "layer": layer,
                            "room": room,
                            "entrance": entrance_index,
                        },
                    },
                )
                self.add_patch_to_stage(
                    "F301",
                    {
                        "name": f"Dungeon entrance patch - Ancient Harbor to {dungeon}",
                        "type": "objpatch",
                        "index": 4,
                        "room": 0,
                        "objtype": "SCEN",
                        "object": {
                            "name": dungeon_stage,
                            "layer": layer,
                            "room": room,
                            "entrance": entrance_index,
                        },
                    },
                )

            # most dungeons only have a single exit, exception being LMF, which is handled seperately
            exit_stage, exit_layer, exit_room, exit_entrance = DUNGEON_EXITS[entrance]
            # the exit out of the back of LMF is special, because it's the only dungeon finish that can be
            # taken multiple times. The first time it should show a save prompt and subsequent times
            # it should not and they don't need to be touched if the LMF entrance is vanilla
            # the first time exit is taken care of by the DUNGEON_FINISH_EXIT_SCEN stuff
            # patch the secondary exit if it's not vanilla
            if (
                dungeon == "Lanayru Mining Facility"
                and not entrance == "Dungeon Entrance in Lanayru Desert"
            ):
                self.add_patch_to_stage(
                    "F300_5",
                    {
                        "name": f"Dungeon exit patch - second LMF finish to {entrance}",
                        "type": "objpatch",
                        "index": 1,
                        "room": 0,
                        "objtype": "SCEN",
                        "object": {
                            "name": exit_stage,
                            "layer": exit_layer,
                            "room": exit_room,
                            "entrance": exit_entrance,
                        },
                    },
                )
            # patch all the exits for the dungeon
            for scen_stage, scen_room, scen_index in DUNGEON_EXIT_SCENS[dungeon]:
                self.add_patch_to_stage(
                    scen_stage,
                    {
                        "name": f"Dungeon exit patch - {dungeon} to {entrance}",
                        "type": "objpatch",
                        "index": scen_index,
                        "room": scen_room,
                        "objtype": "SCEN",
                        "object": {
                            "name": exit_stage,
                            "layer": exit_layer,
                            "room": exit_room,
                            "entrance": exit_entrance,
                        },
                    },
                )

            scen_stage, scen_room, scen_index = DUNGEON_FINISH_EXIT_SCEN[dungeon]
            exit_stage, exit_layer, exit_room, exit_entrance = DUNGEON_FINISH_EXITS[
                entrance
            ]
            self.add_patch_to_stage(
                scen_stage,
                {
                    "name": f"Dungeon finish exit patch - {dungeon} to {entrance}",
                    "type": "objpatch",
                    "index": scen_index,
                    "room": scen_room,
                    "objtype": "SCEN",
                    "object": {
                        "name": exit_stage,
                        "layer": exit_layer,
                        "room": exit_room,
                        "entrance": exit_entrance,
                        "flag8": 1,  # save prompt
                    },
                },
            )

            # fix post dungeon storyflags
            inner_stage, inner_room, inner_evnt = POST_DUNGEON_CUTSCENE[dungeon]
            storyflag = POST_DUNGEON_STORYFLAGS[entrance]
            self.add_patch_to_stage(
                inner_stage,
                {
                    "name": f"Post Dungeon Storyflag fix: {entrance} - {dungeon}",
                    "type": "objpatch",
                    "index": inner_evnt,
                    "room": inner_room,
                    "objtype": "EVNT",
                    "object": {"story_flag1": storyflag},
                },
            )

    def add_trial_rando_patches(self):
        for trial_gate, trial in self.placement_file.trial_connections.items():
            trial_gate_stage, trial_gate_room, trial_gate_scen = TRIAL_GATE_STAGES[
                trial_gate
            ]
            trial_stage, layer, room, trial_gate_index = TRIAL_ENTRANCES[trial]
            # patch dungeon entrance
            self.add_patch_to_stage(
                trial_gate_stage,
                {
                    "name": f"Trial gate patch - {trial_gate} to {trial}",
                    "type": "objpatch",
                    "index": trial_gate_scen,
                    "room": trial_gate_room,
                    "objtype": "SCEN",
                    "object": {
                        "name": trial_stage,
                        "layer": layer,
                        "room": room,
                        "entrance": trial_gate_index,
                    },
                },
            )

            scen_stage, scen_room, scen_index = TRIAL_EXIT_SCENS[trial]
            exit_stage, exit_layer, exit_room, exit_entrance = TRIAL_EXITS[trial_gate]
            self.add_patch_to_stage(
                scen_stage,
                {
                    "name": f"Trial exit patch - {trial} to {trial_gate}",
                    "type": "objpatch",
                    "index": scen_index,
                    "room": scen_room,
                    "objtype": "SCEN",
                    "object": {
                        "name": exit_stage,
                        "layer": exit_layer,
                        "room": exit_room,
                        "entrance": exit_entrance,
                    },
                },
            )

    def shopsanity_patches(self):
        with (Path(__file__).parent / "beedle_texts.yaml").open("r") as f:
            beedle_texts = yaml.safe_load(f)
        # print(beedle_texts)
        for location in BEEDLE_TEXT_PATCHES:
            normal, discounted, normal_price, discount_price = BEEDLE_TEXT_PATCHES[
                location
            ]
            sold_item = self.placement_file.item_locations[location]
            normal_text = (
                break_lines(
                    f"That there is a <y<{sold_item}>>. "
                    f"I'm selling it for only <r<{normal_price}>> rupees! "
                    f"Want to buy it?\n"
                )
                + f"\n{BEEDLE_BUY_SWTICH}"
            )
            discount_text = (
                break_lines(
                    f"That there is a <y<{sold_item}>>. "
                    f"Just this once it's half off! "
                    f"It can be yours for just <r<{discount_price}>> rupees! "
                    f"Want to buy it?"
                )
                + f"\n{BEEDLE_BUY_SWTICH}"
            )
            if location in beedle_texts:
                if sold_item in beedle_texts[location]:
                    # item has custom text for Beedle's shop
                    normal_text = f'{beedle_texts[location][sold_item]["normal"]}{BEEDLE_BUY_SWTICH}'
                    discount_text = f'{beedle_texts[location][sold_item]["discount"]}{BEEDLE_BUY_SWTICH}'

            if isinstance(normal, int):  # string index is new text
                self.eventpatches["105-Terry"].append(
                    {
                        "name": f"{location} Text",
                        "type": "textpatch",
                        "index": normal,
                        "text": normal_text,
                    }
                )
            else:
                self.eventpatches["105-Terry"].append(
                    {"name": normal, "type": "textadd", "text": normal_text}
                )
            if isinstance(discounted, int):
                self.eventpatches["105-Terry"].append(
                    {
                        "name": f"{location} Discount Text",
                        "type": "textpatch",
                        "index": discounted,
                        "text": discount_text,
                    }
                )
            else:
                self.eventpatches["105-Terry"].append(
                    {"name": discounted, "type": "textadd", "text": discount_text}
                )

    def do_build_arc_cache(self):
        self.rando.progress_callback("building arc cache...")

        with (RANDO_ROOT_PATH / "extracts.yaml").open() as f:
            extracts = yaml.safe_load(f)
        self.patcher.create_oarc_cache(extracts)

    def add_startitem_patches(self):
        # Add sword story/itemflags if required
        start_sword_count = self.placement_file.starting_items.count(
            "Progressive Sword"
        )
        for i in range(start_sword_count):
            self.startstoryflags.append(PROGRESSIVE_SWORD_STORYFLAGS[i])
        if start_sword_count > 0:
            self.startitemflags.append(PROGRESSIVE_SWORD_ITEMIDS[start_sword_count - 1])

        # if 'Sailcloth' in self.placement_file.starting_items:
        #     self.startstoryflags.append(32)
        #     self.startitemflags.append(15)

        if "Progressive Pouch" in self.placement_file.starting_items:
            self.startstoryflags.append(30)  # storyflag for pouch
            self.startstoryflags.append(931)  # rando storyflag for progressive pouch 1
            self.startitemflags.append(112)  # itemflag for pouch

        # Add storyflags for tablets
        for item in self.placement_file.starting_items:
            if item in START_ITEM_STORYFLAGS:
                self.startstoryflags.append(START_ITEM_STORYFLAGS[item])

    def add_required_dungeon_patches(self):
        # Add required dungeon patches to eventpatches
        DUNGEON_TO_EVENTFILE = {
            "Skyview": "201-ForestD1",
            "Earth Temple": "301-MountainD1",
            "Lanayru Mining Facility": "400-Desert",
            "Ancient Cistern": "202-ForestD2",
            "Sandship": "401-DesertD2",
            "Fire Sanctuary": "304-MountainD2",
        }

        REQUIRED_DUNGEON_STORYFLAGS = [902, 903, 926, 927, 928, 929]

        for i, dungeon in enumerate(self.placement_file.required_dungeons):
            dungeon_events = self.eventpatches[DUNGEON_TO_EVENTFILE[dungeon]]
            required_dungeon_storyflag_event = next(
                filter(
                    lambda x: x["name"] == "rando required dungeon storyflag",
                    dungeon_events,
                )
            )
            required_dungeon_storyflag_event["flow"][
                "param2"
            ] = REQUIRED_DUNGEON_STORYFLAGS[
                i
            ]  # param2 is storyflag of event

        required_dungeon_count = len(self.placement_file.required_dungeons)
        # set flags for unrequired dungeons beforehand
        for required_dungeon_storyflag in REQUIRED_DUNGEON_STORYFLAGS[
            required_dungeon_count:
        ]:
            self.startstoryflags.append(required_dungeon_storyflag)

        # patch required dungeon text in
        if required_dungeon_count == 0:
            required_dungeons_text = "No Dungeons"
        elif required_dungeon_count == 6:
            required_dungeons_text = "All Dungeons"
        elif required_dungeon_count < 4:
            required_dungeons_text = "Required Dungeons:\n" + (
                "\n".join(self.placement_file.required_dungeons)
            )
        else:
            required_dungeons_text = "Required: " + ", ".join(
                self.placement_file.required_dungeons
            )

            # try to fit the text in as few lines as possible, breaking up at spaces if necessary
            cur_line = ""
            combined = ""

            for part in required_dungeons_text.split(" "):
                if len(cur_line + part) > 27:  # limit of one line
                    combined += cur_line + "\n"
                    cur_line = part + " "
                else:
                    cur_line += part + " "
            combined += cur_line
            required_dungeons_text = combined.strip()

        self.eventpatches["107-Kanban"].append(
            {
                "name": "Knight Academy Billboard text",
                "type": "textpatch",
                "index": 18,
                "text": required_dungeons_text,
            }
        )

    def add_trial_hint_patches(self):
        def find_event(filename, name):
            return next(
                (
                    patch
                    for patch in self.eventpatches[filename]
                    if patch["name"] == name
                ),
                None,
            )

        # Trial Hints
        trial_checks = {
            # (getting it text patch, line, inventory text line, hintname)
            "Skyloft Silent Realm - Stone of Trials": (
                "Full SotH text",
                659,
                "The song that leads you to the final trial.",
                "Song of the Hero - Trial Hint",
            ),
            "Faron Silent Realm - Water Scale": (
                "Farore's Courage Text",
                653,
                "This song opens the trial located in Faron\nWoods.",
                "Farore's Courage - Trial Hint",
            ),
            "Lanayru Silent Realm - Clawshots": (
                "Nayru's Wisdom Text",
                654,
                "This song opens the trial located in\nLanayru Desert.",
                "Nayru's Wisdom - Trial Hint",
            ),
            "Eldin Silent Realm - Fireshield Earrings": (
                "Din's Power Text",
                655,
                "This song opens the trial located on\nEldin Volcano.",
                "Din's Power - Trial Hint",
            ),
        }
        for trial_check_name, (
            obtain_text_name,
            inventory_text_idx,
            inventory_text,
            hintname,
        ) in trial_checks.items():
            useful_text = self.placement_file.trial_hints[hintname]
            item_get_patch = find_event("003-ItemGet", obtain_text_name)
            item_get_patch["text"] += " " + useful_text
            item_get_patch["text"] = break_lines(item_get_patch["text"], 44)
            self.eventpatches["003-ItemGet"].append(
                {
                    "name": "Harp Text",
                    "type": "textpatch",
                    "index": inventory_text_idx,
                    "text": break_lines(inventory_text + " " + useful_text, 44),
                }
            )

    def add_impa_hint(self):
        sot_region = "Stone of Trials not placed monkaS"
        for location in self.placement_file.item_locations.keys():
            item = self.placement_file.item_locations[location]
            if item == "Stone of Trials":
                sot_region = Logic.split_location_name_by_zone(location)[0]
        self.eventpatches["502-CenterFieldBack"].append(
            {
                "name": "Past Impa SoT Hint",
                "type": "textpatch",
                "index": 6,
                "text": break_lines(
                    f"Do not fear for <b<Zelda>>. I will watch over her here. Go now to "
                    f"<b<{sot_region}>>. The <r<item you need to fulfill your destiny>> is there."
                ),
            }
        )

    def add_stone_hint_patches(self):
        for hintname, hintdef in self.rando.stonehint_definitions.items():
            self.add_patch_to_event(
                hintdef["textfile"],
                {
                    "name": f"Hint {hintname}",
                    "type": "textpatch",
                    "index": hintdef["textindex"],
                    "text": break_and_make_multiple_textboxes(
                        self.placement_file.gossip_stone_hints[hintname]
                    ),
                },
            )

    def handle_oarc_add_remove(self):
        remove_stageoarcs = defaultdict(set)

        for stage, stagepatches in self.patches.items():
            if stage == "global":
                continue
            for patch in stagepatches:
                if patch["type"] == "oarcadd":
                    self.stageoarcs[(stage, patch["destlayer"])].add(patch["oarc"])
                elif patch["type"] == "oarcdelete":
                    remove_stageoarcs[(stage, patch["layer"])].add(patch["oarc"])

        for (stage, layer), oarcs in self.stageoarcs.items():
            self.patcher.add_stage_oarc(stage, layer, oarcs)
        for (stage, layer), oarcs in remove_stageoarcs.items():
            self.patcher.delete_stage_oarc(stage, layer, oarcs)

    def add_rando_hash(self):
        if not "002-System" in self.eventpatches:
            self.eventpatches["002-System"] = []

        self.eventpatches["002-System"].append(
            {
                "name": "Rando hash on file select",
                "type": "textpatch",
                "index": 73,
                "text": self.placement_file.hash_str,
            }
        )

        self.eventpatches["002-System"].append(
            {
                "name": "Rando hash on new file",
                "type": "textpatch",
                "index": 75,
                "text": self.placement_file.hash_str,
            }
        )

    def add_keysanity(self):
        DUNGEON_COLORS = {
            "Skyview": "<g<",
            "Earth Temple": "<r+<",
            "Lanayru Mining Facility": "<y<",
            "Ancient Cistern": "<b<",
            "Fire Sanctuary": "<r<",
            "Sandship": "<y+<",
            "Sky Keep": "<s<",
            "Lanayru Caves": "<ye<",
        }
        KEYS_DUNGEONS = [
            # ('Skyview', 200), # already has a textbox
            ("Lanayru Mining Facility", 201),
            ("Ancient Cistern", 202),
            ("Fire Sanctuary", 203),
            ("Sandship", 204),
            ("Sky Keep", 205),
            ("Lanayru Caves", 206),
        ]
        self.eventpatches["003-ItemGet"].append(
            {
                "name": f"Skyview Key Text",  # for some reason there is an entry for item 200 (It's just an empty textbox though)
                "type": "textpatch",
                "index": 251,
                "text": f"You got a <g<Skyview>> Small Key!",
            }
        )
        for dungeon, itemid in KEYS_DUNGEONS:
            dungeon_and_color = DUNGEON_COLORS[dungeon] + dungeon + ">>"
            self.eventpatches["003-ItemGet"].append(
                {
                    "name": f"{dungeon} Key Text",
                    "type": "textadd",
                    "unk1": 5,
                    "unk2": 1,
                    "text": f"You got a {dungeon_and_color} Small Key!"
                    if dungeon != "Lanayru Mining Facility"
                    else f"You got a {dungeon_and_color} Small\nKey!",
                }
            )
            self.eventpatches["003-ItemGet"].append(
                {
                    "name": f"Show {dungeon} Key Text",
                    "type": "flowadd",
                    "flow": {
                        "type": "type1",
                        "next": -1,
                        "param3": 3,
                        "param4": f"{dungeon} Key Text",
                    },
                }
            )
            self.eventpatches["003-ItemGet"].append(
                {
                    "name": f"{dungeon} Key Entry",
                    "type": "entryadd",
                    "entry": {
                        "name": f"003_{itemid}",
                        "value": f"Show {dungeon} Key Text",
                    },
                }
            )
        MAPS_DUNGEONS = [
            ("Skyview", 207),
            ("Earth Temple", 208),
            ("Lanayru Mining Facility", 209),
            ("Ancient Cistern", 210),
            ("Fire Sanctuary", 211),
            ("Sandship", 212),
            ("Sky Keep", 213),
        ]
        for dungeon, itemid in MAPS_DUNGEONS:
            dungeon_and_color = DUNGEON_COLORS[dungeon] + dungeon + ">>"
            self.eventpatches["003-ItemGet"].append(
                {
                    "name": f"{dungeon} Map Text",
                    "type": "textadd",
                    "unk1": 5,
                    "unk2": 1,
                    "text": f"You got the {dungeon_and_color} Map!",
                }
            )
            self.eventpatches["003-ItemGet"].append(
                {
                    "name": f"Show {dungeon} Map Text",
                    "type": "flowadd",
                    "flow": {
                        "type": "type1",
                        "next": -1,
                        "param3": 3,
                        "param4": f"{dungeon} Map Text",
                    },
                }
            )
            self.eventpatches["003-ItemGet"].append(
                {
                    "name": f"{dungeon} Map Entry",
                    "type": "entryadd",
                    "entry": {
                        "name": f"003_{itemid}",
                        "value": f"Show {dungeon} Map Text",
                    },
                }
            )

    def bzs_patch_func(self, bzs, stage, room):
        stagepatches = self.patches.get(stage, [])
        stagepatches = list(filter(self.filter_option_requirement, stagepatches))
        modified = False
        if room == None:
            layer_patches = list(
                filter(lambda x: x["type"] == "layeroverride", stagepatches)
            )
            if len(layer_patches) > 1:
                print(f"ERROR: multiple layer overrides for stage {stage}!")
            elif len(layer_patches) == 1:
                layer_override = [
                    OrderedDict(
                        story_flag=x["story_flag"], night=x["night"], layer=x["layer"]
                    )
                    for x in layer_patches[0]["override"]
                ]
                bzs["LYSE"] = layer_override
                modified = True
        next_id = highest_objid(bzs) + 1
        for objadd in filter(
            lambda x: x["type"] == "objadd" and x.get("room", None) == room,
            stagepatches,
        ):
            layer = objadd.get("layer", None)
            objtype = objadd["objtype"].ljust(
                4
            )  # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
            obj = objadd["object"]
            if objtype in ["SOBS", "SOBJ", "STAS", "STAG", "SNDT"]:
                new_obj = DEFAULT_SOBJ.copy()
            elif objtype in ["OBJS", "OBJ ", "DOOR"]:
                new_obj = DEFAULT_OBJ.copy()
            elif objtype == "SCEN":
                new_obj = DEFAULT_SCEN.copy()
            elif objtype == "AREA":
                new_obj = DEFAULT_AREA.copy()
            else:
                print(f"Error: unknown objtype: {objtype}")
                continue
            if "index" in obj:
                # check index, just to verify index based lists don't have a mistake in them
                if layer is None:
                    objlist = bzs.get(objtype, [])
                else:
                    objlist = bzs["LAY "][f"l{layer}"].get(objtype, [])
                if len(objlist) != obj["index"]:
                    print(f"ERROR: wrong index adding object: {json.dumps(objadd)}")
                    continue
            for key, val in obj.items():
                if key in new_obj:
                    new_obj[key] = val
                else:
                    try_patch_obj(new_obj, key, val)
            if "id" in new_obj:
                new_obj["id"] = (new_obj["id"] & ~0x3FF) | next_id
                next_id += 1
            if layer is None:
                if not objtype in bzs:
                    bzs[objtype] = []
                objlist = bzs[objtype]
            else:
                if not objtype in bzs["LAY "][f"l{layer}"]:
                    bzs["LAY "][f"l{layer}"][objtype] = []
                objlist = bzs["LAY "][f"l{layer}"][objtype]
            # add object name to objn if it's some kind of actor
            if objtype in [
                "SOBS",
                "SOBJ",
                "STAS",
                "STAG",
                "SNDT",
                "OBJS",
                "OBJ ",
                "DOOR",
            ]:
                # TODO: this only works if the layer is set
                if not "OBJN" in bzs["LAY "][f"l{layer}"]:
                    bzs["LAY "][f"l{layer}"]["OBJN"] = []
                objn = bzs["LAY "][f"l{layer}"]["OBJN"]
                if not obj["name"] in objn:
                    objn.append(obj["name"])
            objlist.append(new_obj)
            modified = True
            # print(obj)
        for objpatch in filter(
            lambda x: x["type"] == "objpatch" and x.get("room", None) == room,
            stagepatches,
        ):
            obj = get_entry_from_bzs(bzs, objpatch)
            if not obj is None:
                for key, val in objpatch["object"].items():
                    if key in obj:
                        obj[key] = val
                    else:
                        try_patch_obj(obj, key, val)
                modified = True
                # print(f'modified object from {layer} in room {room} with id {objpatch["id"]:04X}')
                # print(obj)
        for objmove in filter(
            lambda x: x["type"] == "objmove" and x.get("room", None) == room,
            stagepatches,
        ):
            obj = get_entry_from_bzs(bzs, objmove, remove=True)
            destlayer = objmove["destlayer"]
            if not obj is None:
                layer = objmove["layer"]
                objtype = objmove["objtype"].ljust(4)
                obj["id"] = (obj["id"] & ~0x3FF) | next_id
                next_id += 1
                if not objtype in bzs["LAY "][f"l{destlayer}"]:
                    bzs["LAY "][f"l{destlayer}"][objtype] = []
                bzs["LAY "][f"l{destlayer}"][objtype].append(obj)
                objn = bzs["LAY "][f"l{destlayer}"]["OBJN"]
                if not obj["name"] in objn:
                    objn.append(obj["name"])
                modified = True
                # print(f'moved object from {layer} to {destlayer} in room {room} with id {objmove["id"]:04X}')
                # print(obj)
        for objdelete in filter(
            lambda x: x["type"] == "objdelete" and x.get("room", None) == room,
            stagepatches,
        ):
            obj = get_entry_from_bzs(bzs, objdelete, remove=True)
            if not obj is None:
                modified = True
                # print(f'removed object from {layer} in room {room} with id {objdelete["id"]:04X}')
                # print(obj)
        for command in filter(
            lambda x: x["type"] == "objnadd" and x.get("room", None) == room,
            stagepatches,
        ):
            layer = command.get("layer", None)
            name_to_add = command["objn"]
            if layer is None:
                if not "OBJN" in bzs:
                    bzs["OBJN"] = []
                objlist = bzs["OBJN"]
            else:
                if not "OBJN" in bzs["LAY "][f"l{layer}"]:
                    bzs["LAY "][f"l{layer}"]["OBJN"] = []
                objlist = bzs["LAY "][f"l{layer}"]["OBJN"]
            objlist.append(name_to_add)

        # patch randomized items on stages
        for objname, layer, objid, itemid in self.rando_stagepatches.get(
            (stage, room), []
        ):
            modified = True
            if objname == "WarpObj":
                RANDO_PATCH_FUNCS[objname](
                    bzs["LAY "][f"l{layer}"],
                    itemid,
                    objid,
                    self.placement_file.trial_connections,
                )
            else:
                RANDO_PATCH_FUNCS[objname](bzs["LAY "][f"l{layer}"], itemid, objid)

        if modified:
            # print(json.dumps(bzs))
            return bzs
        else:
            return None

    def flow_patch(self, msbf, filename):
        modified = False
        flowpatches = self.eventpatches.get(filename, [])
        flowpatches = list(filter(self.filter_option_requirement, flowpatches))

        # dictionary to map flow labels to ids for new flows
        label_to_index = OrderedDict()
        next_index = len(msbf["FLW3"]["flow"])
        # fist, fill in all the flow name to index mappings
        for command in filter(
            lambda x: x["type"] in ["flowadd", "switchadd"], flowpatches
        ):
            label_to_index[command["name"]] = next_index
            next_index += 1
        for command in filter(lambda x: x["type"] == "flowpatch", flowpatches):
            flowobj = msbf["FLW3"]["flow"][command["index"]]
            for key, val in command.get("flow", {}).items():
                # special case: next points to a label
                if key == "next" and not isinstance(val, int):
                    index = label_to_index.get(val, None)
                    if index is None:
                        print(
                            f'ERROR: label {val} not found in patch: {command["flow"]}'
                        )
                        continue
                    val = index
                # special case: text points to a label, textindex is param4
                if key == "param4" and not isinstance(val, int):
                    index = self.text_labels.get(val, None)
                    if index is None:
                        print(
                            f'ERROR: text label {val} not found in patch: {command["flow"]}'
                        )
                        continue
                    val = index
                flowobj[key] = val
            if flowobj["type"] == "switch":
                # patch cases if given
                cases = command.get("cases", None)
                if cases:
                    assert len(cases) == flowobj["param4"]  # param4 is number of cases
                    branch_start = flowobj["param5"]
                    for i, case in enumerate(cases):
                        if not isinstance(case, int):
                            case = label_to_index.get(case, None)
                            assert (
                                not case is None
                            ), f'ERROR: text label {val} not found in patch: {command["flow"]}'
                        msbf["FLW3"]["branch_points"][branch_start + i] = case
                        # print(f'set {branch_start+i} to {case}')
                    # print(flowobj)
            # print(f'patched flow {command["index"]}, {filename}')
            modified = True
        for command in filter(
            lambda x: x["type"] in ["flowadd", "switchadd"], flowpatches
        ):
            assert (
                len(msbf["FLW3"]["flow"]) == label_to_index[command["name"]]
            ), f'index has to be the next value in the flow, expected {len(msbf["FLW3"]["flow"])} got {label_to_index[command["name"]]}'
            flowobj = OrderedDict(
                type="type1",
                subType=-1,
                param1=0,
                param2=0,
                next=-1,
                param3=0,
                param4=0,
                param5=0,
            )
            for key, val in command["flow"].items():
                # special case: next points to a label
                if key == "next" and not isinstance(val, int):
                    index = label_to_index.get(val, None)
                    if index is None:
                        print(
                            f'ERROR: label {val} not found in new flow: {command["flow"]}'
                        )
                        continue
                    val = index
                # special case: text points to a label, textindex is param4
                if key == "param4" and not isinstance(val, int):
                    index = self.text_labels.get(val, None)
                    if index is None:
                        print(
                            f'ERROR: text label {val} not found in new flow: {command["flow"]}'
                        )
                        continue
                    val = index
                flowobj[key] = val
            if command["type"] == "flowadd":
                msbf["FLW3"]["flow"].append(flowobj)
                # print(f'added flow {command["name"]}, {filename}')
            else:
                flowobj["type"] = "switch"
                cases = command["cases"]
                for i, _ in enumerate(cases):
                    value = cases[i]
                    if not isinstance(value, int):
                        index = label_to_index.get(value, None)
                        if index is None:
                            print(
                                f"ERROR: label {value} not found in switch: {command}"
                            )
                            continue
                        cases[i] = index
                add_msbf_branch(msbf, flowobj, cases)
                # print(f'added switch {command["name"]}, {filename}')
            modified = True
        for command in filter(lambda x: x["type"] == "entryadd", flowpatches):
            value = command["entry"]["value"]
            if not isinstance(value, int):
                index = label_to_index.get(value, None)
                if index is None:
                    print(
                        f'ERROR: label {value} not found in new entry: {command["entry"]}'
                    )
                    continue
                value = index
            new_entry = OrderedDict(
                name=command["entry"]["name"],
                value=value,
            )
            bucket = entrypoint_hash(command["entry"]["name"], len(msbf["FEN1"]))
            msbf["FEN1"][bucket].append(new_entry)
            # print(f'added flow entry {command["entry"]["name"]}, {filename}')
            modified = True
        if filename == "003-ItemGet":
            # make progressive mitts
            make_progressive_item(msbf, 93, [35, 231], [56, 99], [904, 905])
            # make progressive swords
            # TODO trainings and goddess sword both set storyflags on their own, could reuse those
            make_progressive_item(
                msbf,
                136,
                [77, 608, 75, 78, 74, 73],
                PROGRESSIVE_SWORD_ITEMIDS,
                PROGRESSIVE_SWORD_STORYFLAGS,
            )
            # make progressive beetle
            make_progressive_item(msbf, 96, [38, 178], [53, 75], [912, 913])
            # make progressive pouch
            make_progressive_item(msbf, 258, [254, 253], [112, 113], [931, 932])
            # make progressive wallets
            make_progressive_item(
                msbf,
                250,
                [246, 245, 244, 255],
                [108, 109, 110, 111],
                [915, 916, 917, 918],
            )
            modified = True

        # patch randomized items
        for evntline, itemid in self.rando_eventpatches.get(filename, []):
            try:
                # can either be a label or a number
                evntline = int(evntline)
            except ValueError:
                index = label_to_index.get(evntline, None)
                if index is None:
                    print(f"ERROR: label {evntline} not found!")
                    continue
                evntline = index
                # print(f'dynamic label: {evntline}')
            modified = True
            msbf["FLW3"]["flow"][evntline]["param2"] = itemid
            msbf["FLW3"]["flow"][evntline]["param3"] = 9  # give item command

        if modified:
            return msbf
        else:
            return None

    def text_patch(self, msbt, filename):
        # for bucket, lbl_list in enumerate(msbt['LBL1']):
        #     for lbl in lbl_list:
        #         hash_b = entrypoint_hash(lbl['name'], len(msbt['LBL1']))
        #         print(f'smile: {bucket} {hash_b}')
        assert len(msbt["TXT2"]) == len(msbt["ATR1"])
        modified = False
        textpatches = self.eventpatches.get(filename, [])
        textpatches = list(filter(self.filter_option_requirement, textpatches))
        for command in filter(lambda x: x["type"] == "textpatch", textpatches):
            msbt["TXT2"][command["index"]] = process_control_sequences(
                command["text"]
            ).encode("utf-16be")
            # print(f'patched text {command["index"]}, {filename}')
            modified = True
        for command in filter(lambda x: x["type"] == "textadd", textpatches):
            index = len(msbt["TXT2"])
            self.text_labels[command["name"]] = index
            msbt["TXT2"].append(
                process_control_sequences(command["text"]).encode("utf-16be")
            )
            msbt["ATR1"].append(
                {"unk1": command.get("unk1", 1), "unk2": command.get("unk2", 0)}
            )
            # the game doesn't care about the name, but it has to exist and be unique
            # only unique within a file but whatever
            entry_name = "%s:%d" % (filename[-3:], index)
            new_entry = OrderedDict(
                name=entry_name,
                value=index,
            )
            bucket = entrypoint_hash(entry_name, len(msbt["LBL1"]))
            msbt["LBL1"][bucket].append(new_entry)
            # print(f'added text {index}, {filename}')
            modified = True
        if modified:
            return msbt
        else:
            return None

    def do_dol_patch(self):
        self.rando.progress_callback("patching main.dol...")
        # patch main.dol
        dol_bytes = BytesIO(
            (
                self.patcher.actual_extract_path / "DATA" / "sys" / "main.dol"
            ).read_bytes()
        )
        dol = DOL()
        dol.read(dol_bytes)
        apply_dol_patch(self, dol, self.all_asm_patches["main.dol"])
        # do startflags, each entry is a u16, different flag types are terminated by 0xFFFF
        # first storyflags, then itemflags, then sceneflags (first byte area, second byte flag)
        start_flags_write = BytesIO()
        for flag in self.startstoryflags:
            start_flags_write.write(struct.pack(">H", flag))
        start_flags_write.write(bytes.fromhex("FFFF"))
        # itemflags
        for flag in self.startitemflags:
            start_flags_write.write(struct.pack(">H", flag))
        start_flags_write.write(bytes.fromhex("FFFF"))
        # sceneflags
        for flagregion, flags in (
            self.patches["global"].get("startsceneflags", {}).items()
        ):
            flagregionid = FLAGINDEX_NAMES.index(flagregion)
            for flag in flags:
                if not isinstance(flag, int):  # it's a dict with onlyif and flag
                    if not Logic.check_static_option_req(
                        flag["onlyif"], self.placement_file.options
                    ):
                        # flag should not be set according to options
                        continue
                    flag = flag["flag"]
                start_flags_write.write(struct.pack(">BB", flagregionid, flag))
        start_flags_write.write(bytes.fromhex("FFFF"))
        startflag_byte_count = len(start_flags_write.getbuffer())
        if startflag_byte_count > 512:
            raise Exception(
                f"not enough space to fit in all of the startflags, need {startflag_byte_count}, but only 512 bytes available"
            )
        # print(f"total startflag byte count: {startflag_byte_count}")
        dol.write_data_bytes(0x804EE1B8, start_flags_write.getbuffer())
        dol.save_changes()
        write_bytes_create_dirs(
            self.patcher.modified_extract_path / "DATA" / "sys" / "main.dol",
            dol_bytes.getbuffer(),
        )

    def do_rel_patch(self):
        self.rando.progress_callback("patching rels...")
        rel_arc = U8File.parse_u8(
            BytesIO(
                (
                    self.patcher.actual_extract_path / "DATA" / "files" / "rels.arc"
                ).read_bytes()
            )
        )
        rel_modified = False
        for file, codepatches in self.all_asm_patches.items():
            if file == "main.dol":  # main.dol
                continue
            rel_data = BytesIO(rel_arc.get_file_data(f"rels/{file}"))
            if rel_data is None:
                print(f"ERROR: rel {file} not found!")
                continue
            rel = REL()
            rel.read(rel_data)
            apply_rel_patch(self, rel, file, codepatches)
            if (
                file == "d_a_shop_sampleNP.rel"
                and self.placement_file.options["shop-mode"] != "Vanilla"
            ):
                self.do_shoptable_rel_patch(rel)
            rel.save_changes()
            rel_arc.set_file_data(f"rels/{file}", rel_data.getbuffer())
            rel_modified = True
        if rel_modified:
            rel_data = rel_arc.to_buffer()
            write_bytes_create_dirs(
                self.patcher.modified_extract_path / "DATA" / "files" / "rels.arc",
                rel_data,
            )

    def do_shoptable_rel_patch(self, rel):
        # shopsanity patches
        # 24, 17, 18 is patched extra wallet chain
        # patches the next value in the shop item chain
        shop_item_next_patches = {
            24: 17,
            17: 18,
        }
        shop_price_patches = {
            17: 100,
            18: 100,
        }
        shop_entrypoint_patches = {
            17: 10539,
            18: 10540,
        }
        shop_present_scale_patches = {
            17: 1.2,
            18: 1.2,
        }
        shop_target_height_patches = {
            17: 100,
            18: 100,
        }
        sold_out_storyflag_patches = {
            24: 937,
            17: 938,
            18: 939,
            25: 940,  # bug net
            27: 941,  # bug medal
        }
        SHOP_LIST_OFFSET = 0x6D8C
        ENTRY_SIZE = 0x54
        for shopindex, (itemid, arcname, modelname) in self.shoppatches.items():
            (
                data_bytes,
                shop_list_offset,
            ) = rel.convert_rel_offset_to_section_data_and_relative_offset(
                SHOP_LIST_OFFSET
            )
            current_shop_entry_offset = shop_list_offset + ENTRY_SIZE * shopindex
            present_scale = shop_present_scale_patches.get(shopindex, None)
            if not present_scale is None:
                write_float(data_bytes, current_shop_entry_offset + 0x0, present_scale)
            target_height = shop_target_height_patches.get(shopindex, None)
            if not target_height is None:
                write_float(data_bytes, current_shop_entry_offset + 0x8, target_height)
            # item id
            write_u16(data_bytes, current_shop_entry_offset + 0xC, itemid)

            shop_price = shop_price_patches.get(shopindex, None)
            if not shop_price is None:
                write_u16(data_bytes, current_shop_entry_offset + 0xE, shop_price)

            shop_entrypoint = shop_entrypoint_patches.get(shopindex, None)
            if not shop_entrypoint is None:
                write_u16(data_bytes, current_shop_entry_offset + 0x10, shop_entrypoint)

            shop_item_next = shop_item_next_patches.get(shopindex, None)
            if not shop_item_next is None:
                write_u16(data_bytes, current_shop_entry_offset + 0x12, shop_item_next)

            write_str(data_bytes, current_shop_entry_offset + 0x16, arcname, 30)
            write_str(data_bytes, current_shop_entry_offset + 0x34, modelname, 30)
            sold_out_storyflag = sold_out_storyflag_patches.get(shopindex, None)
            if not sold_out_storyflag is None:
                # normally not part of the struct, but the last 2 bytes of the modelname aren't used, so use them for storyflags
                write_u16(
                    data_bytes, current_shop_entry_offset + 0x52, sold_out_storyflag
                )

    def do_patch_object_pack(self):
        self.rando.progress_callback("patching ObjectPack...")
        # patch object pack
        objpack_data = nlzss11.decompress(
            (
                self.patcher.actual_extract_path
                / "DATA"
                / "files"
                / "Object"
                / "ObjectPack.arc.LZ"
            ).read_bytes()
        )
        object_arc = U8File.parse_u8(BytesIO(objpack_data))
        objpack_modified = False
        for oarc in self.patches["global"].get("objpackoarcadd", []):
            oarc_data = (self.patcher.oarc_cache_path / f"{oarc}.arc").read_bytes()
            object_arc.add_file_data(f"oarc/{oarc}.arc", oarc_data)
            objpack_modified = True
        # arc replacements
        ARC_REPLACEMENTS_PATH = self.rando.exe_root_path / "arc-replacements"
        ARC_REPLACEMENTS_PATH.mkdir(exist_ok=True)
        for file in ARC_REPLACEMENTS_PATH.glob("*.arc"):
            arcname = file.parts[-1]  # includes the .arc extension
            filename = f"oarc/{arcname}"
            file_in_arc = object_arc.get_file(filename)
            if file_in_arc is not None:
                arcdata = file.read_bytes()
                file_in_arc.set_data(arcdata)
            objpack_modified = True
        if objpack_modified:
            objpack_data = object_arc.to_buffer()
            write_bytes_create_dirs(
                self.patcher.modified_extract_path
                / "DATA"
                / "files"
                / "Object"
                / "ObjectPack.arc.LZ",
                nlzss11.compress(objpack_data),
            )

    def do_patch_title_screen_logo(self):
        # patch title screen logo
        actual_data = (
            self.rando.actual_extract_path
            / "DATA"
            / "files"
            / "US"
            / "Layout"
            / "Title2D.arc"
        ).read_bytes()
        actual_arc = U8File.parse_u8(BytesIO(actual_data))
        logodata = (self.rando.rando_root_path / "assets" / "logo.tpl").read_bytes()
        actual_arc.set_file_data("timg/tr_wiiKing2Logo_00.tpl", logodata)
        (
            self.rando.modified_extract_path
            / "DATA"
            / "files"
            / "US"
            / "Layout"
            / "Title2D.arc"
        ).write_bytes(actual_arc.to_buffer())
