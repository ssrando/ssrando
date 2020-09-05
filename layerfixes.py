from pathlib import Path
import random
from collections import OrderedDict, defaultdict
import yaml
import json
from io import BytesIO

from sslib import AllPatcher, U8File
from sslib.utils import write_bytes_create_dirs, encodeBytes

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
    else:
        print(f'ERROR: unsupported object to patch {obj}')

def fix_layers():
    patcher = AllPatcher(
        actual_extract_path=Path(__file__).parent / 'actual-extract',
        modified_extract_path=Path(__file__).parent / 'modified-extract',
        oarc_cache_path=Path(__file__).parent / 'oarc',
        copy_unmodified=False)
    with open("patches.yaml") as f:
        patches = yaml.safe_load(f)
    
    if not patcher.oarc_cache_path.exists():
        with open("extracts.yaml") as f:
            extracts = yaml.safe_load(f)
        patcher.create_oarc_cache(extracts)

    stageoarcs = defaultdict(set)

    for stage, stagepatches in patches.items():
        if stage == 'global':
            continue
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
                    if key in obj:
                        obj[key] = val
                    else:
                        try_patch_obj(obj, key, val)
                modified = True
                print(f'modified object from {layer} in room {room} with id {objpatch["id"]:04X}')
                # print(obj)
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
                if not objtype in bzs['LAY '][f'l{destlayer}']:
                    bzs['LAY '][f'l{destlayer}'][objtype] = []
                bzs['LAY '][f'l{destlayer}'][objtype].append(obj)
                objn = bzs['LAY '][f'l{destlayer}']['OBJN']
                if not obj['name'] in objn:
                    objn.append(obj['name'])
                modified = True
                print(f'moved object from {layer} to {destlayer} in room {room} with id {objmove["id"]:04X}')
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
                print(f'removed object from {layer} in room {room} with id {objdelete["id"]:04X}')
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
            if not objtype in bzs['LAY '][f'l{layer}']:
                bzs['LAY '][f'l{layer}'][objtype] = []
            bzs['LAY '][f'l{layer}'][objtype].append(new_obj)
            modified = True
            print(f'added object {obj["name"]} to {layer} in room {room}')
            # print(obj)
        if stage == 'F405' and room == 0:
            # patch hero's tunic, sailcloth and goddess sword in opening CS
            bzs['EVNT'][0]['story_flag2'] = 36
            bzs['EVNT'][0]['item'] = 15
            modified = True
        elif stage == 'F001r' and room == 1:
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
            bzs['EVNT'][0]['item'] = 11
            modified = True
        elif stage == 'F300_5' and room == 0:
            new_obj = OrderedDict(
                params1 = 0xFF0302FF,
                params2 = 0xFF5FFFFF,
                posx = 836,
                posy = 0,
                posz = 305,
                anglex = 0xFFFF,
                angley = 0xBC30,
                anglez = 0xFFFF,
                id = (0xFD84 & ~0x3FF) | next_id,
                name = "saveObj",
            )
            next_id += 1
            if not 'OBJS' in bzs['LAY ']['l0']:
                bzs['LAY ']['l0']['OBJS'] = []
            bzs['LAY ']['l0']['OBJS'].append(new_obj)
            bzs['LAY ']['l0']['OBJN'].append('saveObj')
            assert len(bzs['SCEN']) == 3, "F300_5 room 0 should have 3 SCEN"
            new_scen = OrderedDict(
                name = "F300",
                room = 0,
                layer = 0,
                entrance = 5,
                byte4 = 2,
                byte5 = 2,
                flag6 = 0,
                zero = 0,
                flag8 = 0
            )
            bzs['SCEN'].append(new_scen)
            modified = True
        if modified:
            # print(json.dumps(bzs))
            return bzs
        else:
            return None

    patcher.set_bzs_patch(bzs_patch_func)
    patcher.do_patch()

    # patch main.dol
    orig_dol = bytearray((patcher.actual_extract_path / 'DATA' / 'sys' / 'main.dol').read_bytes())
    for dolpatch in patches['global'].get('asm',{}).get('main',[]):
        actual_code = bytes.fromhex(dolpatch['original'])
        patched_code = bytes.fromhex(dolpatch['patched'])
        assert len(actual_code) == len(patched_code), "code length has to remain the same!"
        code_pos = orig_dol.find(actual_code)
        
        assert code_pos != -1, f"code {dolpatch['original']} not found in main.dol!"
        assert orig_dol.find(actual_code, code_pos+1) == -1, f"code {dolpatch['original']} found multiple times in main.dol!"
        orig_dol[code_pos:code_pos+len(actual_code)] = patched_code
    write_bytes_create_dirs(patcher.modified_extract_path / 'DATA' / 'sys' / 'main.dol', orig_dol)

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
        for codepatch in codepatches:
            actual_code = bytes.fromhex(codepatch['original'])
            patched_code = bytes.fromhex(codepatch['patched'])
            assert len(actual_code) == len(patched_code), "code length has to remain the same!"
            code_pos = rel.find(actual_code)
            
            assert code_pos != -1, f"code {codepatch['original']} not found in {file}!"
            assert rel.find(actual_code, code_pos+1) == -1, f"code {codepatch['original']} found multiple times in {file}!"
            rel[code_pos:code_pos+len(actual_code)] = patched_code
        rel_arc.set_file_data(f'rels/{file}NP.rel',rel)
        rel_modified = True
    if rel_modified:
        rel_data = rel_arc.to_buffer()
        write_bytes_create_dirs(patcher.modified_extract_path / 'DATA' / 'files' / 'rels.arc', rel_data)

if __name__ == '__main__':
    fix_layers()