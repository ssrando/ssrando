from pathlib import Path
import random
from collections import OrderedDict, defaultdict
import yaml
import json

from sslib import AllPatcher
from sslib.utils import write_bytes_create_dirs

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

def fix_layers():
    patcher = AllPatcher(
        actual_extract_path=Path(__file__).parent / 'actual-extract',
        modified_extract_path=Path(__file__).parent / 'modified-extract',
        oarc_cache_path=Path(__file__).parent / 'oarc',
        copy_unmodified=False)
    with open("extracts.yaml") as f:
        extracts = yaml.safe_load(f)
    with open("patches.yaml") as f:
        patches = yaml.safe_load(f)
    
    # patcher.create_oarc_cache(extracts)

    stageoarcs = defaultdict(set)

    for stage, stagepatches in patches.items():
        for patch in stagepatches:
            if patch['type'] == 'oarcadd':
                stageoarcs[(stage, patch['destlayer'])].add(patch['oarc'])
    
    for (stage, layer), oarcs in stageoarcs.items():
        patcher.add_stage_oarc(stage, layer, oarcs)

    def bzs_patch_func(bzs, stage, room):
        stagepatches = patches.get(stage, [])
        modified = False
        if room == None:
            layer_patches = list(filter(lambda x: x['type']=='layeroverride', stagepatches))
            if len(layer_patches) > 1:
                print(f"warning, multiple layer overrides for stage {stage}!")
            elif len(layer_patches) == 1:
                layer_override = [OrderedDict(story_flag=x['story_flag'], night=x['night'], layer=x['layer']) for x in layer_patches[0]['override']]
                bzs['LYSE'] = layer_override
                modified = True
        next_id = highest_objid(bzs) + 1
        for objmove in filter(lambda x: x['type']=='objmove' and x.get('room',None)==room, stagepatches):
            id = objmove['id']
            layer = objmove['layer']
            destlayer = objmove['destlayer']
            objtype = objmove['objtype'].ljust(4) # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
            objs = [x for x in bzs['LAY '][f'l{layer}'][objtype] if x['id'] == id]
            if len(objs) != 1:
                print(f'Error finding object: {json.dumps(objmove)}')
            else:
                obj = objs[0]
                bzs['LAY '][f'l{layer}'][objtype].remove(obj)
                obj['id'] = (obj['id'] & ~0x3FF) | next_id
                next_id += 1
                bzs['LAY '][f'l{destlayer}'][objtype].append(obj)
                objn = bzs['LAY '][f'l{destlayer}']['OBJN']
                if not obj['name'] in objn:
                    objn.append(obj['name'])
                modified = True
                print(f'moved object from {layer} to {destlayer} in room {room} with id {objmove["id"]}')
                # print(obj)
        for objdelete in filter(lambda x: x['type']=='objdelete' and x.get('room',None)==room, stagepatches):
            id = objdelete['id']
            layer = objdelete['layer']
            objtype = objdelete['objtype'].ljust(4) # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
            objs = [x for x in bzs['LAY '][f'l{layer}'][objtype] if x['id'] == id]
            if len(objs) != 1:
                print(f'Error finding object: {json.dumps(objdelete)}')
            else:
                obj = objs[0]
                bzs['LAY '][f'l{layer}'][objtype].remove(obj)
                modified = True
                print(f'removed object from {layer} in room {room} with id {objdelete["id"]}')
                # print(obj)
        for objpatch in filter(lambda x: x['type']=='objpatch' and x.get('room',None)==room, stagepatches):
            id = objpatch['id']
            layer = objpatch['layer']
            objtype = objpatch['objtype'].ljust(4) # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
            objs = [x for x in bzs['LAY '][f'l{layer}'][objtype] if x['id'] == id]
            if len(objs) != 1:
                print(f'Error finding object: {json.dumps(objpatch)}')
            else:
                obj = objs[0]
                for key, val in objpatch['patch'].items():
                    obj[key] = val
                modified = True
                print(f'modified object from {layer} in room {room} with id {objpatch["id"]}')
                # print(obj)
        for objadd in filter(lambda x: x['type']=='objadd' and x.get('room',None)==room, stagepatches):
            layer = objadd['layer']
            objtype = objadd['objtype'].ljust(4) # OBJ has an whitespace but thats was too error prone for the yaml, so just pad it here
            obj = objadd['object']
            if objtype in ['SOBS','SOBJ','STAS','STAG','SNDT']:
                new_obj = OrderedDict(
                    params1 = obj['params1'],
                    params2 = obj['params2'],
                    posx = obj['posx'],
                    posy = obj['posy'],
                    posz = obj['posz'],
                    sizex = obj['sizex'],
                    sizey = obj['sizey'],
                    sizez = obj['sizez'],
                    anglex = obj['anglex'],
                    angley = obj['angley'],
                    anglez = obj['anglez'],
                    id = (obj['id'] & ~0x3FF) | next_id,
                    name = obj['name'],
                )
            elif objtype in ['OBJS','OBJ ','DOOR']:
                new_obj = OrderedDict(
                    params1 = obj['params1'],
                    params2 = obj['params2'],
                    posx = obj['posx'],
                    posy = obj['posy'],
                    posz = obj['posz'],
                    anglex = obj['anglex'],
                    angley = obj['angley'],
                    anglez = obj['anglez'],
                    id = (obj['id'] & ~0x3FF) | next_id,
                    name = obj['name'],
                )
            else:
                print(f'Error: unknown objtype: {objtype}')
                continue
            next_id += 1
            bzs['LAY '][f'l{layer}'][objtype].append(new_obj)
            modified = True
            print(f'added object {obj["name"]} to {layer} in room {room}')
            # print(obj)
        if modified:
            # print(json.dumps(bzs))
            return bzs
        else:
            return None

    patcher.set_bzs_patch(bzs_patch_func)
    patcher.do_patch()

if __name__ == '__main__':
    fix_layers()