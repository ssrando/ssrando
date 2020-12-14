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

import nlzss11
from sslib import AllPatcher, U8File
from sslib.utils import write_bytes_create_dirs, encodeBytes
from paths import RANDO_ROOT_PATH
from tboxSubtypes import tboxSubtypes

from logic.logic import Logic

TOTAL_STAGE_FILES = 369
TOTAL_EVENT_FILES = 6

# arc cache, main.dol, rels, objectpack
GAMEPATCH_TOTAL_STEP_COUNT = TOTAL_EVENT_FILES + TOTAL_STAGE_FILES + 4

DEFAULT_SOBJ = OrderedDict(
    params1 = 0,
    params2 = 0,
    posx = 0,
    posy = 0,
    posz = 0,
    sizex = 0,
    sizey = 0,
    sizez = 0,
    anglex = 0,
    angley = 0,
    anglez = 0,
    id = 0,
    name = "",
)

DEFAULT_OBJ = OrderedDict(
    params1 = 0,
    params2 = 0,
    posx = 0,
    posy = 0,
    posz = 0,
    anglex = 0,
    angley = 0,
    anglez = 0,
    id = 0,
    name = "",
)

DEFAULT_SCEN = OrderedDict(
    name = "",
    room = 0,
    layer = 0,
    entrance = 0,
    byte4 = 0,
    byte5 = 0,
    flag6 = 0,
    zero = 0,
    flag8 = 0
)

# cutscenes to use to set storyflags, sceneflags and itemflags
START_CUTSCENES = [
    # stage, room, eventindex
    ('F000',0,22),
    ('F000',0,23),
    ('F001r',1,2),
    ('F405',0,0),
]

START_ITEM_STORYFLAGS = {
    "Emerald Tablet": 46,
    "Ruby Tablet": 47,
    "Amber Tablet": 48,
}

# The stage name of each dungeon
DUNGEON_STAGES = {
    'Skyview': 'D100',
    'Ancient Cistern': 'D101',
    'Earth Temple': 'D200',
    'Fire Sanctuary': 'D201',
    'Lanayru Mining Facility': 'D300',
    'Sandship': 'D301',
    'Skykeep': 'D003_7'
}

# The stage for each map where there are dungeon entrances
DUNGEON_ENTRANCE_STAGES = {
    "Dungeon Entrance In Deep Woods": "F101",
    "Dungeon Entrance In Lake Floria": 'F102_1',
    "Dungeon Entrance In Eldin Volcano": "F200",
    "Dungeon Entrance In Volcano Summit": 'F201_3',
    "Dungeon Entrance In Lanayru Desert": 'F300',
    "Dungeon Entrance In Sand Sea": 'F301_1',
    "Dungeon Entrance On Skyloft": 'F000',
}

# The index of the SCEN inside of the stage
ENTRANCE_MAP_SCEN_INDEX = {
    'F101': 1,
    'F102_1': 1,
    'F200': 0,
    'F201_3': 1,
    'F300': 5,
    'F301_1': 1,
    'F000': 48
}

# The entrance into the dungeon
ENTRANCE_MAP_ENTRANCE_INDEX = {
    'F101': 0,
    'F102_1': 1,
    'F200': 0,
    'F201_3': 1,
    'F300': 0,
    'F301_1': 1,
    'F000': 4
}

# The room on the map the entrance is on where the SCEN is located
ENTRANCE_MAP_ROOM = {
    'F101': 0,
    'F102_1': 1,
    'F200': 4,
    'F201_3': 0,
    'F300': 0,
    'F301_1': 1,
    'F000': 4
}

# The room of the dungeon tto enter into
ENTRANCE_DUNGEON_ROOM = {
    'D100': 0,
    'D101': 0,
    'D200': 1,
    'D201': 0,
    'D300': 0,
    'D301': 0,
    'D003_7': 0
}

PROGRESSIVE_SWORD_STORYFLAGS = [906, 907, 908, 909, 910, 911]
PROGRESSIVE_SWORD_ITEMIDS = [10, 11, 12, 9, 13, 14]

class FlagEventTypes(IntEnum):
    SET_STORYFLAG = 0,
    UNSET_STORYFLAG = 1,
    SET_SCENEFLAG = 2,
    UNSET_SCENEFLAG = 3,
    SET_ZONEFLAG = 4,
    UNSET_ZONEFLAG = 5,
    SET_TEMPFLAG = 28,
    UNSET_TEMPFLAG = 29,

class FlagSwitchTypes(IntEnum):
    CHOICE = 0,
    STORYFLAG = 3,
    ZONEFLAG = 5,
    SCENEFLAG = 6,
    TEMPFLAG = 9,

def entrypoint_hash(name: str, entries: int) -> int:
    hash = 0
    for char in name:
        hash = (hash * 0x492 + ord(char)) & 0xFFFFFFFF
    return hash % entries

def make_switch(subtype: FlagSwitchTypes, arg: int):
    if subtype == FlagSwitchTypes.CHOICE:
        p2 = 0
        p3 = arg # number of choices
    else:
        p2 = arg
        p3 = subtype.value
    return OrderedDict(
        type = "switch",
        subType = 6,
        param1 = 0,
        param2 = p2,
        next = -1,
        param3 = p3,
        param4 = -1,
        param5 = -1,
    )

def make_give_item_event(item):
    return OrderedDict(
        type = "type3",
        subType = 0,
        param1 = 0,
        param2 = item,
        next = -1,
        param3 = 9,
        param4 = 0,
        param5 = 0,
    )

def make_flag_event(subtype: FlagEventTypes, flag):
    if subtype == FlagEventTypes.SET_STORYFLAG or subtype == FlagEventTypes.UNSET_STORYFLAG:
        st = 0
        p1 = 0
        p2 = flag
    else:
        st = 1
        p1 = flag
        p2 = 0
    return OrderedDict(
        type = "type3",
        subType = st,
        param1 = p1,
        param2 = p2,
        next = -1,
        param3 = subtype.value,
        param4 = 0,
        param5 = 0,
    )

def add_msbf_branch(msbf, switch, branchpoints):
    branch_index = len(msbf['FLW3']['branch_points'])
    msbf['FLW3']['branch_points'].extend(branchpoints)
    switch['param4'] = len(branchpoints)
    switch['param5'] = branch_index
    msbf['FLW3']['flow'].append(switch)

def make_progressive_item(msbf, base_item_start, item_text_indexes, item_ids, storyflags):
    if len(item_text_indexes) != len(storyflags) or len(item_text_indexes) != len(item_ids):
        raise Exception("item_text_indexes should be the same length as storyflags!")
    flow_idx = len(msbf['FLW3']['flow'])
    msbf['FLW3']['flow'][base_item_start]['next'] = flow_idx
    index = len(item_text_indexes) - 1 # start from the highest upgrade
    # first, check if the storyflag of the previous upgrade is set
    # if yes, set the storyflag for this upgrade, give the upgrade and jump to that upgrade's text
    # otherwise check the next upgrade storyflag. If no storyflag is set, set the lowest upgrades storyflag
    # but no need to give that item since it's that items event that is hijacked
    for index in range(len(item_text_indexes)-1, 0, -1):
        branch = make_switch(FlagSwitchTypes.STORYFLAG, storyflags[index-1])
        add_msbf_branch(msbf, branch, [flow_idx+1, flow_idx+3])
        event = make_give_item_event(item_ids[index])
        event['next'] = flow_idx + 2
        msbf['FLW3']['flow'].append(event)
        event = make_flag_event(FlagEventTypes.SET_STORYFLAG, storyflags[index])
        event['next'] = item_text_indexes[index]
        msbf['FLW3']['flow'].append(event)
        flow_idx += 3
    event = make_flag_event(FlagEventTypes.SET_STORYFLAG, storyflags[0])
    event['next'] = item_text_indexes[0]
    msbf['FLW3']['flow'].append(event)

# check highest
def highest_objid(bzs):
    max_id = 0
    for layer in bzs.get('LAY ',{}).values():
        if len(layer) == 0:
            continue
        for objtype in ['OBJS','OBJ ','SOBS','SOBJ','STAS','STAG','SNDT','DOOR']:
            if objtype in layer:
                id = layer[objtype][-1]['id'] & 0x3FF
                if id != 0x3FF: # aparently some objects have the max id?
                    max_id = max(max_id, id)
    return max_id

def mask_shift_set(value, mask, shift, new_value):
    """
    Replace new_value in value, by applying the mask after the shift
    """
    new_value = new_value & mask
    return (value & ~(mask << shift)) | (new_value << shift)

def try_patch_obj(obj, key, value):
    if obj['name'].startswith('Npc'):
        if key == 'trigstoryfid':
            obj['params1'] = mask_shift_set(obj['params1'], 0x7FF, 10, value)
        elif key == 'untrigstoryfid':
            obj['params1'] = mask_shift_set(obj['params1'], 0x7FF, 21, value)
        elif key == 'talk_behaviour':
            obj['anglez'] = value
        elif obj['name'] == 'NpcTke':
            if key == 'trigscenefid':
                obj['anglex'] = mask_shift_set(obj['anglex'], 0xFF, 0, value)
            elif key == 'untrigscenefid':
                obj['anglex'] = mask_shift_set(obj['anglex'], 0xFF, 8, value)
            else:
                print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj['name'] == 'TBox':
        if key == 'spawnscenefid':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 20, value)
        elif key == 'setscenefid':
            obj['anglex'] = mask_shift_set(obj['anglex'], 0xFF, 0, value)
        elif key == 'itemid':
            obj['anglez'] = mask_shift_set(obj['anglez'], 0x1FF, 0, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj['name'] == 'EvntTag':
        if key == 'trigscenefid':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 16, value)
        elif key == 'setscenefid':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 8, value)
        elif key == 'event':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 0, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj['name'] == 'EvfTag':
        if key == 'trigstoryfid':
            obj['params1'] = mask_shift_set(obj['params1'], 0x7FF, 19, value)
        elif key == 'setstoryfid':
            obj['params1'] = mask_shift_set(obj['params1'], 0x7FF, 8, value)
        elif key == 'event':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 0, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj['name'] == 'ScChang':
        if key == 'trigstoryfid':
            obj['anglex'] = mask_shift_set(obj['anglex'], 0x7FF, 0, value)
        elif key == 'untrigstoryfid':
            obj['anglez'] = mask_shift_set(obj['anglez'], 0x7FF, 0, value)
        elif key == 'scen_link':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 0, value)
        elif key == 'trigscenefid':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 24, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    elif obj['name'] == 'SwAreaT':
        if key == 'setstoryfid':
            obj['anglex'] = mask_shift_set(obj['anglex'], 0x7FF, 0, value)
        elif key == 'unsetstoryfid':
            obj['anglez'] = mask_shift_set(obj['anglez'], 0x7FF, 0, value)
        elif key == 'setscenefid':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 0, value)
        elif key == 'unsetscenefid':
            obj['params1'] = mask_shift_set(obj['params1'], 0xFF, 8, value)
        else:
            print(f'ERROR: unsupported key "{key}" to patch for object {obj}')
    else:
        print(f'ERROR: unsupported object to patch {obj}')

def patch_tbox_item(tbox: OrderedDict, itemid: int):
    origitemid = tbox['anglez'] & 0x1FF
    boxtype = tboxSubtypes[origitemid]
    tbox['anglez'] = mask_shift_set(tbox['anglez'], 0x1FF, 0, itemid)
    # code has been patched, to interpret this part of params1 as boxtype
    tbox['params1'] = mask_shift_set(tbox['params1'], 0x3, 4, boxtype)

def patch_item_item(itemobj: OrderedDict, itemid: int):
    itemobj['params1'] = mask_shift_set(itemobj['params1'], 0xFF, 0, itemid)
    # subtype 9, this acts like hearpieces and force being collected with a textbox
    itemobj['params1'] = mask_shift_set(itemobj['params1'], 0xF, 0x14, 9)

# these are not treasure chests, but instead only used for the hp in zeldas room
def patch_chest_item(chest: OrderedDict, itemid: int):
    chest['params1'] = mask_shift_set(chest['params1'], 0xFF, 8, itemid)

# code has been patched to use this part of params1 as itemid
def patch_heart_co(heart_co: OrderedDict, itemid: int):
    heart_co['params1'] = mask_shift_set(heart_co['params1'], 0xFF, 16, itemid)

# code has been patched to use this part of params1 as itemid
def patch_chandelier_item(chandel: OrderedDict, itemid: int):
    chandel['params1'] = mask_shift_set(chandel['params1'], 0xFF, 8, itemid)

def patch_soil_item(soil: OrderedDict, itemid: int):
    # match key piece soils in all ways but keep sceneflag
    soil['params1'] = (soil['params1'] & 0xFF0) | 0xFF0B1004
    # code has been patched to use the first byte of params2 as itemid, but only
    # if it would have been a key piece otherwise
    soil['params2'] = mask_shift_set(soil['params2'], 0xFF, 0x18, itemid)

def patch_trial_item(trial: OrderedDict, itemid: int):
    trial['params1'] = mask_shift_set(trial['params1'], 0xFF, 0x18, itemid)

def patch_key_bokoblin_item(boko: OrderedDict, itemid: int):
    boko['params2'] = mask_shift_set(boko['params2'], 0xFF, 0x0, itemid)



# not treasure chest, wardrobes you can open, used for zelda room HP
def rando_patch_chest(bzs: OrderedDict, itemid: int, id: str):
    id = int(id)
    chest = next(filter(lambda x: x['name'] == 'chest' and (x['params1'] & 0xFF) == id, bzs['OBJ ']))
    patch_chest_item(chest, itemid)

def rando_patch_heartco(bzs: OrderedDict, itemid: int, id: str):
    obj = next(filter(lambda x: x['name'] == 'HeartCo', bzs['OBJ '])) # there is only one heart container at a time
    patch_heart_co(obj, itemid)

def rando_patch_warpobj(bzs: OrderedDict, itemid: int, id: str):
    obj = next(filter(lambda x: x['name'] == 'WarpObj', bzs['OBJ '])) # there is only one trial exit at a time
    patch_trial_item(obj, itemid)

def rando_patch_tbox(bzs: OrderedDict, itemid: int, id: str):
    id = int(id)
    tboxs = list(filter(lambda x: x['name'] == 'TBox' and (x['anglez']>>9) == id, bzs['OBJS']))
    if len(tboxs) == 0:
        print(tboxs)
    obj = tboxs[0] # anglez >> 9 is chest id
    patch_tbox_item(obj, itemid)

def rando_patch_item(bzs: OrderedDict, itemid: int, id: str):
    id = int(id)
    obj = next(filter(lambda x: x['name'] == 'Item' and ((x['params1'] >> 10) & 0xFF) == id, bzs['OBJ '])) # (params1 >> 10) & 0xFF is sceneflag
    patch_item_item(obj, itemid)

def rando_patch_chandelier(bzs: OrderedDict, itemid: int, id: str):
    obj = next(filter(lambda x: x['name'] == 'Chandel', bzs['OBJ ']))
    patch_chandelier_item(obj, itemid)

def rando_patch_soil(bzs: OrderedDict, itemid: int, id: str):
    id = int(id)
    obj = next(filter(lambda x: x['name'] == 'Soil' and ((x['params1'] >> 4) & 0xFF) == id, bzs['OBJ '])) # (params1 >> 4) & 0xFF is sceneflag
    patch_soil_item(obj, itemid)

def rando_patch_bokoblin(bzs: OrderedDict, itemid: int, id: str):
    id = int(id, 0)
    obj = next(filter(lambda x: x['name'] == 'EBc' and x['id']== id, bzs['OBJ ']))
    patch_key_bokoblin_item(obj, itemid)

# functions, that patch the object, they take: the bzs of that layer, the item id and optionally an id, then patches the object in place
RANDO_PATCH_FUNCS = {
    'chest': rando_patch_chest,
    'HeartCo': rando_patch_heartco,
    'WarpObj': rando_patch_warpobj,
    'TBox': rando_patch_tbox,
    'Item': rando_patch_item,
    'Chandel': rando_patch_chandelier,
    'Soil': rando_patch_soil,
    'EBc': rando_patch_bokoblin,
    'Tbox': rando_patch_tbox,
}

def get_patches_from_location_item_list(all_checks, filled_checks):
    with (RANDO_ROOT_PATH / 'items.yaml').open() as f:
        items = yaml.safe_load(f)
    by_item_name=dict((x['name'],x) for x in items)

    # make sure dungeon items exist
    DUNGEONS = ['SW', 'ET', 'LMF', 'AC', 'SS', 'FS', 'SK', 'LanayruCaves'] # caves has a key, no spaces because the randomizer splits by spaces
    for dungeon in DUNGEONS:
        by_item_name[f'{dungeon} Small Key'] = by_item_name['Small Key']
        by_item_name[f'{dungeon} Map'] = by_item_name['Map']
    # (stage, room) -> (object name, layer, id?, itemid)
    stagepatchv2 = defaultdict(list)
    # (stage, layer) -> oarc
    stageoarcs = defaultdict(set)
    # # eventfile: (line, itemid)
    eventpatches = defaultdict(list)

    stage_re = re.compile(r'stage/(?P<stage>[^/]+)/r(?P<room>[0-9]+)/l(?P<layer>[0-9]+)/(?P<objname>[a-zA-Z]+)(/(?P<objid>[^/]+))?')
    event_re = re.compile(r'event/(?P<eventfile>[^/]+)/(?P<eventid>[^/]+)')
    oarc_re = re.compile(r'oarc/(?P<stage>[^/]+)/l(?P<layer>[^/]+)')

    for checkname, itemname in filled_checks.items():
        # single gratitude crystals aren't randomized
        if itemname == 'Gratitude Crystal':
            continue
        check = all_checks[checkname]
        item = by_item_name[itemname]
        for path in check['Paths']:
            stage_match = stage_re.match(path)
            event_match = event_re.match(path)
            oarc_match = oarc_re.match(path)
            if stage_match:
                stage = stage_match.group('stage')
                room = int(stage_match.group('room'))
                layer = int(stage_match.group('layer'))
                objname = stage_match.group('objname')
                objid = stage_match.group('objid')
                oarc = item['oarc']
                if oarc:
                    if isinstance(oarc, list):
                        for o in oarc:
                            stageoarcs[(stage, layer)].add(o)
                    else:
                        stageoarcs[(stage, layer)].add(oarc)
                stagepatchv2[(stage, room)].append((objname, layer, objid, item['id']))
            elif event_match:
                eventfile = event_match.group('eventfile')
                eventid = event_match.group('eventid')
                eventpatches[eventfile].append((eventid, item['id']))
            elif oarc_match:
                stage = oarc_match.group('stage')
                layer = int(oarc_match.group('layer'))
                oarc = item['oarc']
                if oarc:
                    if isinstance(oarc, list):
                        for o in oarc:
                            stageoarcs[(stage, layer)].add(o)
                    else:
                        stageoarcs[(stage, layer)].add(oarc)
            else:
                print(f'ERROR: {path} didn\'t match any regex!')
    return stagepatchv2, stageoarcs, eventpatches

def get_entry_from_bzs(bzs: OrderedDict, objdef: dict, remove: bool=False) -> Optional[OrderedDict]:
    id = objdef.get('id',None)
    index = objdef.get('index',None)
    layer = objdef.get('layer', None)
    objtype = objdef['objtype'].ljust(4) # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
    if layer is None:
        objlist = bzs[objtype]
    else:
        objlist = bzs['LAY '][f'l{layer}'][objtype]
    if not id is None:
        objs = [x for x in objlist if x['id'] == id]
        if len(objs) != 1:
            print(f'Error finding object: {json.dumps(objdef)}')
            return None
        obj = objs[0]
        if remove:
            objlist.remove(obj)
    elif not index is None:
        if index >= len(objlist):
            print(f'Error lisError list index out of range: {json.dumps(objdef)}')
            return None
        if remove:
            obj = objlist.pop(index)
        else:
            obj = objlist[index]
    else:
        print(f'ERROR: neither id nor index given for object {json.dumps(objdef)}')
        return None
    return obj

def do_gamepatches(rando):
    patcher = AllPatcher(
        actual_extract_path=rando.actual_extract_path,
        modified_extract_path=rando.modified_extract_path,
        oarc_cache_path=rando.oarc_cache_path,
        copy_unmodified=False)
    with (RANDO_ROOT_PATH / "patches.yaml").open() as f:
        patches = yaml.safe_load(f)
    with (RANDO_ROOT_PATH / "eventpatches.yaml").open() as f:
        eventpatches = yaml.safe_load(f)
    pprint(patches)

    for entrance, dungeon in rando.entrance_connections.items():
        entrance_stage = DUNGEON_ENTRANCE_STAGES[entrance]
        dungeon_stage = DUNGEON_STAGES[dungeon]
        patches.get(entrance_stage).append({
            'name': 'Dungeon entrance patch - ' + entrance + " to " + dungeon,
            'type': 'objpatch',
            'index': ENTRANCE_MAP_SCEN_INDEX[entrance_stage],
            'room': ENTRANCE_MAP_ROOM[entrance_stage],
            'objtype': 'SCEN',
            'object': {
                'name': dungeon_stage,
                'entrance': ENTRANCE_MAP_ENTRANCE_INDEX[entrance_stage],
                'room': ENTRANCE_DUNGEON_ROOM[dungeon_stage]
            }
        })

    rando.progress_callback('building arc cache...')

    with (RANDO_ROOT_PATH / "extracts.yaml").open() as f:
        extracts = yaml.safe_load(f)
    patcher.create_oarc_cache(extracts)

    def filter_option_requirement(entry):
        return not (isinstance(entry, dict) and 'onlyif' in entry \
            and not rando.logic.check_logical_expression_string_req(entry['onlyif']))

    filtered_storyflags = []
    for storyflag in patches['global']['startstoryflags']:
        # conditionals are an object
        if not isinstance(storyflag, int):
            if filter_option_requirement(storyflag):
                storyflag = storyflag['storyflag']
            else:
                continue
        filtered_storyflags.append(storyflag)

    # filter startstoryflags
    patches['global']['startstoryflags'] = filtered_storyflags

    # Add sword story/itemflags if required
    start_sword_count = rando.starting_items.count('Progressive Sword')
    for i in range(start_sword_count):
        patches['global']['startstoryflags'].append(PROGRESSIVE_SWORD_STORYFLAGS[i])
    if start_sword_count > 0:
        patches['global']['startitems'].append(PROGRESSIVE_SWORD_ITEMIDS[start_sword_count-1])

    # if 'Sailcloth' in rando.starting_items:
    #     patches['global']['startstoryflags'].append(32)
    #     patches['global']['startitems'].append(15)


    rando_stagepatches, stageoarcs, rando_eventpatches = get_patches_from_location_item_list(rando.logic.item_locations, rando.logic.done_item_locations)

    # Add required dungeon patches to eventpatches
    DUNGEON_TO_EVENTFILE = {
        'Skyview': '201-ForestD1',
        'Earth Temple': '301-MountainD1',
        'Lanayru Mining Facility': '400-Desert',
        'Ancient Cistern': '202-ForestD2',
        'Sandship': '401-DesertD2',
        'Fire Sanctuary': '304-MountainD2',
    }

    REQUIRED_DUNGEON_STORYFLAGS = [902, 903, 926, 927, 928, 929]

    for i, dungeon in enumerate(rando.required_dungeons):
        dungeon_events = eventpatches[DUNGEON_TO_EVENTFILE[dungeon]]
        required_dungeon_storyflag_event = next(filter(lambda x: x['name'] == 'rando required dungeon storyflag', dungeon_events))
        required_dungeon_storyflag_event['flow']['param2'] = REQUIRED_DUNGEON_STORYFLAGS[i] # param2 is storyflag of event

    required_dungeon_count = len(rando.required_dungeons)
    # set flags for unrequired dungeons beforehand
    for required_dungeon_storyflag in REQUIRED_DUNGEON_STORYFLAGS[required_dungeon_count:]:
        patches['global']['startstoryflags'].append(required_dungeon_storyflag)

    # patch required dungeon text in
    if required_dungeon_count == 0:
        required_dungeons_text = 'No Dungeons'
    elif required_dungeon_count == 6:
        required_dungeons_text = 'All Dungeons'
    elif required_dungeon_count < 4:
        required_dungeons_text = 'Required Dungeons:\n'+('\n'.join(rando.required_dungeons))
    else:
        required_dungeons_text = 'Required: ' + ', '.join(rando.required_dungeons)

        # try to fit the text in as few lines as possible, breaking up at spaces if necessary
        cur_line = ''
        combined = ''

        for part in required_dungeons_text.split(' '):
            if len(cur_line + part) > 27: # limit of one line
                combined += cur_line + '\n'
                cur_line = part + ' '
            else:
                cur_line += part + ' '
        combined += cur_line
        required_dungeons_text = combined.strip()

    eventpatches['107-Kanban'].append({
        "name": "Knight Academy Billboard text",
        "type": "textpatch",
        "index": 18,
        "text": required_dungeons_text,
    })

    # Add storyflags for startitems (only tablets for now)
    for item in rando.starting_items:
        if item in START_ITEM_STORYFLAGS:
            patches['global']['startstoryflags'].append(START_ITEM_STORYFLAGS[item])


    # add startflags to eventpatches
    startstoryflags = patches['global'].get('startstoryflags',None)
    startsceneflags = patches['global'].get('startsceneflags',None)
    startitems = patches['global'].get('startitems',None)
    def pop_or_default(lst, default=-1):
        if len(lst) == 0:
            return default
        else:
            return lst.pop(0)
    for cs_stage, cs_room, cs_index in START_CUTSCENES:
        if not cs_stage in patches:
            patches[cs_stage] = []
        if cs_stage.startswith('F0'):
            # make sure to only set sceneflags on skyloft
            patches[cs_stage].append({
                'name': 'Startflags',
                'type': 'objpatch',
                'room': cs_room,
                'index': cs_index,
                'objtype': 'EVNT',
                'object': {
                    'item': pop_or_default(startitems),
                    'story_flag1': pop_or_default(startstoryflags),
                    'story_flag2': pop_or_default(startstoryflags),
                    'sceneflag1': pop_or_default(startsceneflags),
                    'sceneflag2': pop_or_default(startsceneflags),
                },
            })
        else:
            patches[cs_stage].append({
                'name': 'Startflags',
                'type': 'objpatch',
                'room': cs_room,
                'index': cs_index,
                'objtype': 'EVNT',
                'object': {
                    'item': pop_or_default(startitems),
                    'story_flag1': pop_or_default(startstoryflags),
                    'story_flag2': pop_or_default(startstoryflags),
                },
            })
    # for now, we can only set scene and storyflags here, so make sure all items were handled in the event
    assert len(startitems) == 0, "Not all items were handled in events!"

    while startsceneflags or startstoryflags:
        patches['F001r'].append({
            'name': 'Startflags',
            'type':'objadd',
            'room': 1, # Link's room
            'layer': 0,
            'objtype': 'STAG',
            'object': {
                "params1": 0xFFFFFF00 | (pop_or_default(startsceneflags) & 0xFF),
                "params2": 0xFF5FFFFF,
                "posx": 761,
                "posy": -22,
                "posz": -2260,
                "sizex": 1000,
                "sizey": 1000,
                "sizez": 1000,
                "anglex": pop_or_default(startstoryflags) & 0xFFFF,
                "angley": 0,
                "anglez": 65535,
                "name": "SwAreaT",
            }
        })

    remove_stageoarcs = defaultdict(set)

    for stage, stagepatches in patches.items():
        if stage == 'global':
            continue
        for patch in stagepatches:
            if patch['type'] == 'oarcadd':
                stageoarcs[(stage, patch['destlayer'])].add(patch['oarc'])
            elif patch['type'] == 'oarcdelete':
                remove_stageoarcs[(stage, patch['layer'])].add(patch['oarc'])

    # stageoarcs[('D000',0)].add('GetSwordA')

    for (stage, layer), oarcs in stageoarcs.items():
        patcher.add_stage_oarc(stage, layer, oarcs)
    for (stage, layer), oarcs in remove_stageoarcs.items():
        patcher.delete_stage_oarc(stage, layer, oarcs)

    if not '002-System' in eventpatches:
        eventpatches['002-System'] = []
    
    eventpatches['002-System'].append({
        "name": "Rando hash on file select",
        "type": "textpatch",
        "index": 73,
        "text": rando.randomizer_hash,
    })

    eventpatches['002-System'].append({
        "name": "Rando hash on new file",
        "type": "textpatch",
        "index": 75,
        "text": rando.randomizer_hash,
    })

    def bzs_patch_func(bzs, stage, room):
        stagepatches = patches.get(stage, [])
        stagepatches = list(filter(filter_option_requirement, stagepatches))
        modified = False
        if room == None:
            layer_patches = list(filter(lambda x: x['type']=='layeroverride', stagepatches))
            if len(layer_patches) > 1:
                print(f"ERROR: multiple layer overrides for stage {stage}!")
            elif len(layer_patches) == 1:
                layer_override = [OrderedDict(story_flag=x['story_flag'], night=x['night'], layer=x['layer']) for x in layer_patches[0]['override']]
                bzs['LYSE'] = layer_override
                modified = True
        next_id = highest_objid(bzs) + 1
        for objpatch in filter(lambda x: x['type']=='objpatch' and x.get('room',None)==room, stagepatches):
            obj = get_entry_from_bzs(bzs, objpatch)
            if not obj is None:
                for key, val in objpatch['object'].items():
                    if key in obj:
                        obj[key] = val
                    else:
                        try_patch_obj(obj, key, val)
                modified = True
                # print(f'modified object from {layer} in room {room} with id {objpatch["id"]:04X}')
                # print(obj)
        for objmove in filter(lambda x: x['type']=='objmove' and x.get('room',None)==room, stagepatches):
            obj = get_entry_from_bzs(bzs, objmove, remove=True)
            destlayer = objmove['destlayer']
            if not obj is None:
                layer = objmove['layer']
                objtype = objmove['objtype'].ljust(4)
                obj['id'] = (obj['id'] & ~0x3FF) | next_id
                next_id += 1
                if not objtype in bzs['LAY '][f'l{destlayer}']:
                    bzs['LAY '][f'l{destlayer}'][objtype] = []
                bzs['LAY '][f'l{destlayer}'][objtype].append(obj)
                objn = bzs['LAY '][f'l{destlayer}']['OBJN']
                if not obj['name'] in objn:
                    objn.append(obj['name'])
                modified = True
                # print(f'moved object from {layer} to {destlayer} in room {room} with id {objmove["id"]:04X}')
                # print(obj)
        for objdelete in filter(lambda x: x['type']=='objdelete' and x.get('room',None)==room, stagepatches):
            obj = get_entry_from_bzs(bzs, objdelete, remove=True)
            if not obj is None:
                modified = True
                # print(f'removed object from {layer} in room {room} with id {objdelete["id"]:04X}')
                # print(obj)
        for command in filter(lambda x: x['type']=='objnadd' and x.get('room',None)==room, stagepatches):
            layer = command.get('layer', None)
            name_to_add = command['objn']
            if layer is None:
                if not 'OBJN' in bzs:
                    bzs['OBJN'] = []
                objlist = bzs['OBJN']
            else:
                if not 'OBJN' in bzs['LAY '][f'l{layer}']:
                    bzs['LAY '][f'l{layer}']['OBJN'] = []
                objlist = bzs['LAY '][f'l{layer}']['OBJN']
            objlist.append(name_to_add)
        for objadd in filter(lambda x: x['type']=='objadd' and x.get('room',None)==room, stagepatches):
            layer = objadd.get('layer', None)
            objtype = objadd['objtype'].ljust(4) # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
            obj = objadd['object']
            if objtype in ['SOBS','SOBJ','STAS','STAG','SNDT']:
                new_obj = DEFAULT_SOBJ.copy()
            elif objtype in ['OBJS','OBJ ','DOOR']:
                new_obj = DEFAULT_OBJ.copy()
            elif objtype == 'SCEN':
                new_obj = DEFAULT_SCEN.copy()
            else:
                print(f'Error: unknown objtype: {objtype}')
                continue
            if 'index' in obj:
                # check index, just to verify index based lists don't have a mistake in them
                if layer is None:
                    objlist = bzs.get(objtype, [])
                else:
                    objlist = bzs['LAY '][f'l{layer}'].get(objtype, [])
                if len(objlist) != obj['index']:
                    print(f'ERROR: wrong index adding object: {json.dumps(objadd)}')
                    continue
            for key, val in obj.items():
                new_obj[key] = val
            if 'id' in new_obj:
                new_obj['id'] = (new_obj['id'] & ~0x3FF) | next_id
                next_id += 1
            if layer is None:
                if not objtype in bzs:
                    bzs[objtype] = []
                objlist = bzs[objtype]
            else:
                if not objtype in bzs['LAY '][f'l{layer}']:
                    bzs['LAY '][f'l{layer}'][objtype] = []
                objlist = bzs['LAY '][f'l{layer}'][objtype]
            # add object name to objn if it's some kind of actor
            if objtype in ['SOBS','SOBJ','STAS','STAG','SNDT','OBJS','OBJ ','DOOR']:
                # TODO: this only works if the layer is set
                objn = bzs['LAY '][f'l{layer}']['OBJN']
                if not obj['name'] in objn:
                    objn.append(obj['name'])
            objlist.append(new_obj)
            modified = True
            # print(obj)

        # patch randomized items on stages
        for objname, layer, objid, itemid in rando_stagepatches.get((stage, room),[]):
            modified = True
            try:
                RANDO_PATCH_FUNCS[objname](bzs['LAY '][f'l{layer}'], itemid, objid)
            except:
                print(f'ERROR: {stage}, {room}, {layer}, {objname}, {objid}')

        if stage == 'F001r' and room == 1:
            # put all storyflags in links room at the start
            if not 'STAG' in bzs['LAY ']['l0']:
                bzs['LAY ']['l0']['STAG'] = []
            for storyflag in patches['global'].get('startstoryflags',[]):
                new_obj = OrderedDict(
                    params1 = 0xFFFFFFFF,
                    params2 = 0xFF5FFFFF,
                    posx = 761,
                    posy = -22,
                    posz = -2260,
                    sizex = 1000,
                    sizey = 1000,
                    sizez = 1000,
                    anglex = storyflag,
                    angley = 0,
                    anglez = 65535,
                    id = (0xFD84 & ~0x3FF) | next_id,
                    name = "SwAreaT",
                )
                bzs['LAY ']['l0']['STAG'].append(new_obj)
                next_id += 1
            modified = True
        if modified:
            # print(json.dumps(bzs))
            return bzs
        else:
            return None

    patcher.set_bzs_patch(bzs_patch_func)

    text_labels = {}

    def flow_patch(msbf, filename):
        modified = False
        flowpatches = eventpatches.get(filename, [])
        flowpatches = list(filter(filter_option_requirement, flowpatches))

        # dictionary to map flow labels to ids for new flows
        label_to_index = OrderedDict()
        next_index = len(msbf['FLW3']['flow'])
        # fist, fill in all the flow name to index mappings
        for command in filter(lambda x: x['type'] in ['flowadd', 'switchadd'], flowpatches):
            label_to_index[command['name']] = next_index
            next_index += 1
        for command in filter(lambda x: x['type'] == 'flowpatch', flowpatches):
            flowobj = msbf['FLW3']['flow'][command['index']]
            for key, val in command['flow'].items():
                # special case: next points to a label
                if key == 'next' and not isinstance(val, int):
                    index = label_to_index.get(val, None)
                    if index is None:
                        print(f'ERROR: label {val} not found in patch: {command["flow"]}')
                        continue
                    val = index
                # special case: text points to a label, textindex is param4
                if key == 'param4' and not isinstance(val, int):
                    index = text_labels.get(val, None)
                    if index is None:
                        print(f'ERROR: text label {val} not found in patch: {command["flow"]}')
                        continue
                    val = index
                flowobj[key] = val
            # print(f'patched flow {command["index"]}, {filename}')
            modified = True
        for command in filter(lambda x: x['type'] in ['flowadd', 'switchadd'], flowpatches):
            assert len(msbf['FLW3']['flow']) == label_to_index[command['name']], f'index has to be the next value in the flow, expected {len(msbf["FLW3"]["flow"])} got {label_to_index[command["name"]]}'
            flowobj = OrderedDict(
                type='type1',
                subType=-1,
                param1=0,
                param2=0,
                next=-1,
                param3=0,
                param4=0,
                param5=0,
            )
            for key, val in command['flow'].items():
                # special case: next points to a label
                if key == 'next' and not isinstance(val, int):
                    index = label_to_index.get(val, None)
                    if index is None:
                        print(f'ERROR: label {val} not found in new flow: {command["flow"]}')
                        continue
                    val = index
                # special case: text points to a label, textindex is param4
                if key == 'param4' and not isinstance(val, int):
                    index = text_labels.get(val, None)
                    if index is None:
                        print(f'ERROR: text label {val} not found in new flow: {command["flow"]}')
                        continue
                    val = index
                flowobj[key] = val
            if command['type'] == 'flowadd':
                msbf['FLW3']['flow'].append(flowobj)
                # print(f'added flow {command["name"]}, {filename}')
            else:
                flowobj['type']='switch'
                cases = command['cases']
                for i, _ in enumerate(cases):
                    value = cases[i]
                    if not isinstance(value, int):
                        index = label_to_index.get(value, None)
                        if index is None:
                            print(f'ERROR: label {value} not found in switch: {command}')
                            continue
                        cases[i] = index
                add_msbf_branch(msbf, flowobj, cases)
                # print(f'added switch {command["name"]}, {filename}')
            modified = True
        for command in filter(lambda x: x['type'] == 'entryadd', flowpatches):
            value = command['entry']['value']
            if not isinstance(value, int):
                index = label_to_index.get(value, None)
                if index is None:
                    print(f'ERROR: label {value} not found in new entry: {command["entry"]}')
                    continue
                value = index
            new_entry = OrderedDict(
                name = command['entry']['name'],
                value = value,
            )
            bucket = entrypoint_hash(command["entry"]["name"], len(msbf['FEN1']))
            msbf['FEN1'][bucket].append(new_entry)
            # print(f'added flow entry {command["entry"]["name"]}, {filename}')
            modified = True
        if filename == '003-ItemGet':
            # make progressive mitts
            make_progressive_item(msbf, 93, [35, 231], [56, 99], [904, 905])
            # make progressive swords
            # TODO trainings and goddess sword both set storyflags on their own, could reuse those
            make_progressive_item(msbf, 136, [77, 608, 75, 78, 74, 73], PROGRESSIVE_SWORD_ITEMIDS, PROGRESSIVE_SWORD_STORYFLAGS)
            # make progressive beetle
            make_progressive_item(msbf, 96, [38, 178], [53, 75], [912, 913])
            # make progressive pouch
            make_progressive_item(msbf, 258, [254, 253], [112, 113], [931, 932])
            # make progressive wallets
            make_progressive_item(msbf, 250, [246, 245, 244, 255], [108, 109, 110, 111], [915, 916, 917, 918])
            modified = True

        # patch randomized items
        for evntline, itemid in rando_eventpatches.get(filename, []):
            try:
                # can either be a label or a number
                evntline = int(evntline)
            except ValueError:
                index = label_to_index.get(evntline, None)
                if index is None:
                    print(f'ERROR: label {evntline} not found!')
                    continue
                evntline = index
                # print(f'dynamic label: {evntline}')
            modified = True
            msbf['FLW3']['flow'][evntline]['param2'] = itemid
            msbf['FLW3']['flow'][evntline]['param3'] = 9 # give item command

        if modified:
            return msbf
        else:
            return None
    def text_patch(msbt, filename):
        # for bucket, lbl_list in enumerate(msbt['LBL1']):
        #     for lbl in lbl_list:
        #         hash_b = entrypoint_hash(lbl['name'], len(msbt['LBL1']))
        #         print(f'smile: {bucket} {hash_b}')
        assert len(msbt['TXT2']) == len(msbt['ATR1'])
        modified = False
        textpatches = eventpatches.get(filename, [])
        textpatches = list(filter(filter_option_requirement, textpatches))
        for command in filter(lambda x: x['type'] == 'textpatch', textpatches):
            msbt['TXT2'][command['index']] = command['text'].encode('utf-16be')
            # print(f'patched text {command["index"]}, {filename}')
            modified = True
        for command in filter(lambda x: x['type'] == 'textadd', textpatches):
            index = len(msbt['TXT2'])
            text_labels[command['name']] = index
            msbt['TXT2'].append(command['text'].encode('utf-16be'))
            msbt['ATR1'].append({'unk1':command.get('unk1',1), 'unk2':command.get('unk2',0)})
            # the game doesn't care about the name, but it has to exist and be unique
            # only unique within a file but whatever
            entry_name="%s:%d" % (filename[-3:], index)
            new_entry = OrderedDict(
                name = entry_name,
                value = index,
            )
            bucket = entrypoint_hash(entry_name, len(msbt['LBL1']))
            msbt['LBL1'][bucket].append(new_entry)
            # print(f'added text {index}, {filename}')
            modified = True
        if modified:
            return msbt
        else:
            return None
    patcher.set_event_patch(flow_patch)
    patcher.set_event_text_patch(text_patch)
    patcher.progress_callback = rando.progress_callback
    patcher.do_patch()

    rando.progress_callback('patching main.dol...')

    # patch main.dol
    orig_dol = bytearray((patcher.actual_extract_path / 'DATA' / 'sys' / 'main.dol').read_bytes())
    for dolpatch in filter(filter_option_requirement, patches['global'].get('asm',{}).get('main',[])):
        actual_code = bytes.fromhex(dolpatch['original'])
        patched_code = bytes.fromhex(dolpatch['patched'])
        assert len(actual_code) == len(patched_code), "code length has to remain the same!"
        code_pos = orig_dol.find(actual_code)

        assert code_pos != -1, f"code {dolpatch['original']} not found in main.dol!"
        assert orig_dol.find(actual_code, code_pos+1) == -1, f"code {dolpatch['original']} found multiple times in main.dol!"
        orig_dol[code_pos:code_pos+len(actual_code)] = patched_code
    write_bytes_create_dirs(patcher.modified_extract_path / 'DATA' / 'sys' / 'main.dol', orig_dol)

    rando.progress_callback('patching rels...')

    rel_arc = U8File.parse_u8(BytesIO((patcher.actual_extract_path / 'DATA' / 'files' / 'rels.arc').read_bytes()))
    rel_modified = False
    for file, codepatches in patches['global'].get('asm',{}).items():
        if file == 'main': # main.dol
            continue
        rel = rel_arc.get_file_data(f'rels/{file}NP.rel')
        if rel is None:
            print(f'ERROR: rel {file} not found!')
            continue
        rel = bytearray(rel)
        for codepatch in filter(filter_option_requirement, codepatches):
            actual_code = bytes.fromhex(codepatch['original'])
            patched_code = bytes.fromhex(codepatch['patched'])
            assert len(actual_code) == len(patched_code), "code length has to remain the same!"
            code_pos = rel.find(actual_code)

            assert code_pos != -1, f"code {codepatch['original']} not found in {file}!"
            if codepatch.get('multiple',False):
                while code_pos != -1:
                    rel[code_pos:code_pos+len(actual_code)] = patched_code
                    code_pos = rel.find(actual_code, code_pos+1)
            else:
                assert rel.find(actual_code, code_pos+1) == -1, f"code {codepatch['original']} found multiple times in {file}!"
                rel[code_pos:code_pos+len(actual_code)] = patched_code
        rel_arc.set_file_data(f'rels/{file}NP.rel',rel)
        rel_modified = True
    if rel_modified:
        rel_data = rel_arc.to_buffer()
        write_bytes_create_dirs(patcher.modified_extract_path / 'DATA' / 'files' / 'rels.arc', rel_data)

    rando.progress_callback('patching ObjectPack...')
    # patch object pack
    objpack_data = nlzss11.decompress((patcher.actual_extract_path / 'DATA' / 'files' / 'Object' / 'ObjectPack.arc.LZ').read_bytes())
    object_arc = U8File.parse_u8(BytesIO(objpack_data))
    objpack_modified = False
    for oarc in patches['global'].get('objpackoarcadd',[]):
        oarc_data = (patcher.oarc_cache_path / f'{oarc}.arc').read_bytes()
        object_arc.add_file_data(f'oarc/{oarc}.arc', oarc_data)
        objpack_modified = True
    if objpack_modified:
        objpack_data = object_arc.to_buffer()
        write_bytes_create_dirs(patcher.modified_extract_path / 'DATA' / 'files' / 'Object' / 'ObjectPack.arc.LZ', nlzss11.compress(objpack_data))

    # patch title screen logo
    actual_data = (rando.actual_extract_path / 'DATA' / 'files' / 'US' / 'Layout' / 'Title2D.arc').read_bytes()
    actual_arc = U8File.parse_u8(BytesIO(actual_data))
    logodata = (rando.rando_root_path / 'assets' / 'logo.tpl').read_bytes()
    actual_arc.set_file_data('timg/tr_wiiKing2Logo_00.tpl', logodata)
    (rando.modified_extract_path / 'DATA' / 'files' / 'US' / 'Layout' / 'Title2D.arc').write_bytes(actual_arc.to_buffer())