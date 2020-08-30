from io import BytesIO
import os
from collections import OrderedDict
from typing import List
from pathlib import Path
import random

from sslib.bzs import parseBzs, buildBzs
import nlzss11
from sslib.u8file import U8File
from sslib import parseMSB, buildMSB, Patcher, AllPatcher

EXTRACT_ROOT_PATH='actual-extract'
MODIFIED_ROOT_PATH='modified-extract'

extracts={
    ('D003_0', 0): ['oarc/GetTriForceSingle.arc'], # Triforce part
    ('D301', 0): ['oarc/GetBowA.arc'], # Bow
    ('F001r', 3):[
        'oarc/GetKobunALetter.arc',  # Cawlin's Letter
        'oarc/GetPouchA.arc'        # Adventure Pouch
    ],
    ('F002r', 1):[
        'oarc/GetPouchB.arc',  # Extra Pouch Slot
        'oarc/GetMedal.arc',        # all Medals
        'oarc/GetNetA.arc'        # Bug Net
        ],
    ('F004r', 0):[
        'oarc/GetPachinkoB.arc',  # Scatershot
        'oarc/GetBowB.arc',        # Iron Bow
        'oarc/GetBowC.arc',        # Sacred Bow
        'oarc/GetBeetleC.arc',  # Quick beetle
        'oarc/GetBeetleD.arc',        # Though Beetle
        'oarc/GetNetB.arc'        # Big Bug Net
        # a bunch more bottles and other stuff is also here
        ],
    ('F202', 1): [
      'oarc/GetPachinkoA.arc', # slingshot
      'oarc/GetHookShot.arc', # clawshots
      'oarc/GetMoleGloveB.arc', # mogma mitts
      'oarc/GetVacuum.arc', # gust bellows
      'oarc/GetWhip.arc', # whip
      'oarc/GetBombBag.arc' # bomb bag
    ],
    ('F210', 0):['oarc/GetMoleGloveA.arc'], # digging mitts
    ('S100', 2):['oarc/GetSizuku.arc'], # water dragon scale
    ('S200', 2):['oarc/GetEarring.arc'], # fireshield earrings
    ('D100', 1):['oarc/GetBeetleA.arc'], # beetle
    ('F300', 0):['oarc/GetBeetleB.arc'], # hook beetle
    ('F301_5', 0):['oarc/GetMapSea.arc'], # Sand Sea Map
    ('F402', 2):['oarc/GetHarp.arc'], # all Songs & Harp
    ('F000', 0):[
        'oarc/MoldoGut_Baby.arc', # babies rattle
        'oarc/GetSeedLife.arc' # LTS
    ],
    ('F000', 4):[
        'oarc/GetShieldWood.arc', # wooden shield
        'oarc/GetShieldHylia.arc' # hylian shield
    ],
    ('F100', 3):[ # stuff for silent realms
        'oarc/PLHarpPlay.arc',
        'oarc/SirenEntrance.arc',
        'oarc/PLSwordStick.arc'
    ],
    ('F020', 1):['oarc/GetBirdStatue.arc'], # Bird statuette
    ('F023', 0):['oarc/GetTerryCage.arc'], # Beedle's Beetle
}

def get_stagepath(stage: str, layer: int=0, rootpath: str=EXTRACT_ROOT_PATH) -> Path:
    return Path(__file__).parent / rootpath / 'DATA' / 'files' / 'Stage' / stage / f'{stage}_stg_l{layer}.arc.LZ'

def extract_objects():
    try:
        os.mkdir('oarc')
    except:
        pass
    for (file, layer), objs in extracts.items():
        with get_stagepath(file, layer).open('rb') as f:
            data=nlzss11.decompress(f.read())
            data=BytesIO(data)
            data=U8File.parse_u8(data)

            for objname in objs:
                outdata=data.get_file_data(objname)
                with open(objname,'wb') as out:
                    out.write(outdata)

def get_names():
    with open(EXTRACT_ROOT_PATH+'/DATA/files/Stage/F000/F000_stg_l4.arc.LZ','rb') as f:
        data=nlzss11.decompress(f.read())
        data=BytesIO(data)
        data=U8File.parse_u8(data)

        # room=data.get_data('rarc/D000_r00.arc:dat/room.bzs')
        for arc in len(data.get_all_paths):
            if arc.endswith('.arc'):
                print(arc)
                # print(data._get_subarc(arc).get_all_paths_recursive())

def testpatch():
    # open the skyloft cave file
    with open(EXTRACT_ROOT_PATH+'/DATA/files/Stage/D000/D000_stg_l0.arc.LZ','rb') as f:
        # extract in memory
        data=nlzss11.decompress(f.read())
        data=BytesIO(data)
        data=U8File.parse_u8(data)

        # add hookshot and gust bellows
        with open('oarc/GetHookShot.arc','rb') as h:
            data.add_file_data('oarc/GetHookShot.arc', h.read())

        with open('oarc/GetVacuum.arc','rb') as h:
            data.add_file_data('oarc/GetVacuum.arc', h.read())
        
        # open room
        # room=parse_bzs(data.get_data('rarc/D000_r00.arc:dat/room.bzs'))
        # get objects
        # objects=room.children['LAY '].layers[0].children['OBJS'].objects
        # find chest with id 68 and replace the content with hookshot
        # for obj in objects:
        #     if obj['name']==b'TBox\x00\x00\x00\x00':
        #         if (obj['talk_behaviour']&0xF700)>>9 == 64:
        #             obj['talk_behaviour']==(obj['talk_behaviour']&0xF700)+0x14
        #             print('patched hookshot')
        # for obj in objects:
        #     if obj['name']==b'TBox\x00\x00\x00\x00':
        #         if (obj['talk_behaviour']&0xF700)>>9 == 67:
        #             obj['talk_behaviour']==(obj['talk_behaviour']&0xF700)+0x31
        #             print('patched gust bellows')
        
        # write room back
        # data.update_file('rarc/D000_r00.arc:dat/room.bzs',build_bzs(room))
        # write stage to memory
        # with open('D000_stg_l0.arc', 'wb') as o:
        #     data.writeto(o)
        return data

def testpatch2():
    with open(f'{EXTRACT_ROOT_PATH}/DATA/files/Stage/D000/D000_stg_l0.arc.LZ','rb') as f:
        extracted_data=nlzss11.decompress(f.read())
    stagearc=U8File.parse_u8(BytesIO(extracted_data))
    roomarc=U8File.parse_u8(BytesIO(stagearc.get_file_data(f'rarc/D000_r00.arc')))
    room=parseBzs(roomarc.get_file_data('dat/room.bzs'))
    objects=room['LAY ']['l0']['OBJS']
    # find chest with id 68 and replace the content with hookshot
    for obj in objects:
        if obj['name']==b'TBox\x00\x00\x00\x00':
            if (obj['unk4']&0xFE00)>>9 == 68:
                obj['posy']=obj['posy']+50
                obj['unk4']=(obj['unk4']&0xFE00)+0x14
                print('patched hookshot')
            if (obj['unk4']&0xFE00)>>9 == 67:
                obj['posy']=obj['posy']+50
                obj['unk4']=(obj['unk4']&0xFE00)+0x31
                print('patched gust bellows')
    roomarc.set_file_data('dat/room.bzs', buildBzs(room))
    stagearc.set_file_data('rarc/D000_r00.arc', roomarc.to_buffer())
    # add gust bellows and hookshot oarcs so they properly work
    with open('oarc/GetHookShot.arc','rb') as f:
        arc=f.read()
        stagearc.add_file_data('oarc/GetHookShot.arc', arc)
    with open('oarc/GetVacuum.arc','rb') as f:
        arc=f.read()
        stagearc.add_file_data('oarc/GetVacuum.arc', arc)

    with open(f'{MODIFIED_ROOT_PATH}/DATA/files/Stage/D000/D000_stg_l0.arc.LZ','wb') as f:
        f.write(nlzss11.compress(stagearc.to_buffer()))

def extract_stage_rooms(name: str) -> OrderedDict:
    with open(f'{EXTRACT_ROOT_PATH}/DATA/files/Stage/{name}/{name}_stg_l0.arc.LZ','rb') as f:
        extracted_data=nlzss11.decompress(f.read())
    stagearc=U8File.parse_u8(BytesIO(extracted_data))
    stage = parseBzs(stagearc.get_file_data('dat/stage.bzs'))
    rooms = OrderedDict()
    for i in range(len(stage['RMPL'])):
        roomarc=U8File.parse_u8(BytesIO(stagearc.get_file_data(f'rarc/{name}_r{i:02}.arc')))
        rooms[f'r{i:02}'] = parseBzs(roomarc.get_file_data('dat/room.bzs'))
    return stage, rooms
    
def upgrade_test():
    # patch stage
    with get_stagepath('D000',0).open('rb') as f:
        extracted_data=nlzss11.decompress(f.read())
    stagearc=U8File.parse_u8(BytesIO(extracted_data))
    stagedef=parseBzs(stagearc.get_file_data('dat/stage.bzs'))
    room0arc=U8File.parse_u8(BytesIO(stagearc.get_file_data('rarc/D000_r00.arc')))
    roomdef=parseBzs(room0arc.get_file_data('dat/room.bzs'))
    # get chest
    chest=next(filter(lambda x: x['name']=='TBox', roomdef['LAY ']['l0']['OBJS']))
    chest['anglez']=(chest['anglez']&~0x1FF) | 53 # Beetle
    room0arc.set_file_data('dat/room.bzs',buildBzs(roomdef))
    # add both beetle models
    with open('oarc/GetBeetleA.arc','rb') as h:
        stagearc.add_file_data('oarc/GetBeetleA.arc', h.read())
    with open('oarc/GetBeetleB.arc','rb') as h:
        stagearc.add_file_data('oarc/GetBeetleB.arc', h.read())
    stagearc.set_file_data('rarc/D000_r00.arc',room0arc.to_buffer())
    # write back
    with get_stagepath('D000',0,rootpath=MODIFIED_ROOT_PATH).open('wb') as f:
        f.write(nlzss11.compress(stagearc.to_buffer()))
    # patch get item event
    with open(Path(__file__).parent / EXTRACT_ROOT_PATH / 'DATA' / 'files' / 'EU' / 'Object' / 'en_GB' / '0-Common.arc', 'rb') as f:
        evntarc=U8File.parse_u8(BytesIO(f.read()))
    itemmsbf=parseMSB(evntarc.get_file_data('0-Common/003-ItemGet.msbf'))
    evnt=itemmsbf['FLW3']['flow'][422] # event triggered after beetle text box
    evnt['type']='type3'
    evnt['subType']=0
    evnt['param1']=0
    evnt['param3']=9
    evnt['param2']=75 # Hook Beetle
    evntarc.set_file_data('0-Common/003-ItemGet.msbf',buildMSB(itemmsbf))
    with open(Path(__file__).parent / MODIFIED_ROOT_PATH / 'DATA' / 'files' / 'EU' / 'Object' / 'en_GB' / '0-Common.arc', 'wb') as f:
        f.write(evntarc.to_buffer())

def upgrade_with_patch():
    # config for repacking as ISO
    # patcher = Patcher(
    #     actual_extract_path=Path(__file__).parent / EXTRACT_ROOT_PATH,
    #     modified_extract_path=Path(__file__).parent / MODIFIED_ROOT_PATH,
    #     oarc_cache_path=Path(__file__).parent / 'oarc',
    #     keep_path=True,
    #     copy_unmodified=False) # set to true during dev to overwrite maybe bad experiments
    # for use with riivolution
    patcher = Patcher(
        actual_extract_path=Path(__file__).parent / EXTRACT_ROOT_PATH,
        modified_extract_path=Path(__file__).parent / 'temp',
        oarc_cache_path=Path(__file__).parent / 'oarc',
        keep_path=False,
        copy_unmodified=False)
    
    def patch_D000_r0(roomdef):
        chest=next(filter(lambda x: x['name']=='TBox', roomdef['LAY ']['l0']['OBJS']))
        chest['anglez']=(chest['anglez']&~0x1FF) | 53 # Beetle
        return roomdef
    patcher.set_room_patch('D000',0,patch_D000_r0)
    def patch_item_get(itemmsbf):
        evnt=itemmsbf['FLW3']['flow'][422] # event triggered after beetle text box
        evnt['type']='type3'
        evnt['subType']=0
        evnt['param1']=0
        evnt['param3']=9
        evnt['param2']=75 # Hook Beetle
        return itemmsbf
    patcher.set_event_patch('003-ItemGet.msbf', patch_item_get)
    patcher.add_stage_oarc('D000',0,['GetBeetleA','GetBeetleB'])
    patcher.do_patch()

def bingo_patch():
    # open all light pillars as part of the zelda event before the save prompt
    # make eldin layer 1 by default, move trial to layer 0, move lava draining to layer 0
    # make eldin caves layer 1 only
    # 
    # config for repacking as ISO
    patcher = Patcher(
        actual_extract_path=Path(__file__).parent / EXTRACT_ROOT_PATH,
        modified_extract_path=Path(__file__).parent / MODIFIED_ROOT_PATH,
        oarc_cache_path=Path(__file__).parent / 'oarc',
        keep_path=True,
        copy_unmodified=False) # set to true during dev to overwrite maybe bad experiments
    # for use with riivolution
    # patcher = Patcher(
    #     actual_extract_path=Path(__file__).parent / EXTRACT_ROOT_PATH,
    #     modified_extract_path=Path(__file__).parent / 'temp',
    #     oarc_cache_path=Path(__file__).parent / 'oarc',
    #     keep_path=False,
    #     copy_unmodified=False)

    # skyloft: move trial to layer 0
    def patch_F000_r0(roomdef):
        trial=next(filter(lambda x: x['name']=='WarpObj', roomdef['LAY ']['l4']['OBJ ']))
        # trial_butterflies=next(filter(lambda x: x['name']=='InsctTg', roomdef['LAY ']['l4']['STAG']))
        # trial['posy'] += 100
        # fix object ID of trial
        trial['id']=0x02F2
        # trial_butterflies['id']=0xFEF3
        roomdef['LAY ']['l4']['OBJ '].remove(trial)
        roomdef['LAY ']['l0']['OBJ '].append(trial)
        # roomdef['LAY ']['l4']['STAG'].remove(trial_butterflies)
        # roomdef['LAY ']['l0']['STAG'].append(trial_butterflies)
        roomdef['LAY ']['l0']['ARCN'].append('SirenEntrance')
        roomdef['LAY ']['l0']['ARCN'].append('PLSwordStick')
        roomdef['LAY ']['l0']['ARCN'].append('PLHarpPlay')
        roomdef['LAY ']['l0']['OBJN'].append('WarpObj')
    patcher.set_room_patch('F000', 0, patch_F000_r0)
    patcher.add_stage_oarc('F000', 0, ('SirenEntrance','PLSwordStick','PLHarpPlay'))
    # faron: force layer 1 always, add trial to layer 0
    def patch_F100(stagedef):
        stagedef['LYSE'] = [OrderedDict((('story_flag', -1), ('night', 0), ('layer', 1)))]
        return stagedef
    patcher.set_stage_patch('F100', patch_F100)
    def patch_F100_r0(roomdef):
        trial=next(filter(lambda x: x['name']=='WarpObj', roomdef['LAY ']['l3']['OBJ ']))
        trial_butterflies=next(filter(lambda x: x['name']=='InsctTg', roomdef['LAY ']['l3']['STAG']))
        # trial['posy'] += 100
        # fix object ID of trial
        trial['id']=0x02F2
        trial_butterflies['id']=0xFEF3
        roomdef['LAY ']['l3']['OBJ '].remove(trial)
        roomdef['LAY ']['l0']['OBJ '].append(trial)
        roomdef['LAY ']['l3']['STAG'].remove(trial_butterflies)
        roomdef['LAY ']['l0']['STAG'].append(trial_butterflies)
        roomdef['LAY ']['l0']['ARCN'].append('SirenEntrance')
        roomdef['LAY ']['l0']['ARCN'].append('PLSwordStick')
        roomdef['LAY ']['l0']['ARCN'].append('PLHarpPlay')
        roomdef['LAY ']['l0']['OBJN'].append('WarpObj')
    patcher.set_room_patch('F100', 0, patch_F100_r0)
    patcher.add_stage_oarc('F100', 0, ('SirenEntrance','PLSwordStick','PLHarpPlay'))

    # deep woods: remove layer 3+ 
    def patch_F101(stagedef):
        stagedef['LYSE']=[layer for layer in stagedef['LYSE'] if layer['layer'] < 3]
    patcher.set_stage_patch('F101',patch_F101)

def fill_skyloft():
    # config for repacking as ISO
    patcher = Patcher(
        actual_extract_path=Path(__file__).parent / EXTRACT_ROOT_PATH,
        modified_extract_path=Path(__file__).parent / MODIFIED_ROOT_PATH,
        oarc_cache_path=Path(__file__).parent / 'oarc',
        keep_path=True,
        copy_unmodified=False) # set to true during dev to overwrite maybe bad experiments
    # for use with riivolution
    # patcher = Patcher(
    #     actual_extract_path=Path(__file__).parent / EXTRACT_ROOT_PATH,
    #     modified_extract_path=Path(__file__).parent / 'temp',
    #     oarc_cache_path=Path(__file__).parent / 'oarc',
    #     keep_path=False,
    #     copy_unmodified=False)
    
    def patch_F000_r0(roomdef):
        roomdef['LAY ']['l0']['ARCN'].append('BLastBoss')
        roomdef['LAY ']['l0']['ARCN'].append('PLLastBoss')
        roomdef['LAY ']['l0']['OBJN'].append('BLasBos')
        roomdef['LAY ']['l0']['OBJ '].append(
            {
                "params1": bytes.fromhex('FFFFFFC0'),
                "params2": bytes.fromhex('FFFFFFFF'),
                "posx": -4698.884765625,
                "posy": 1237.6900634765625,
                "posz": -6364.4482421875,
                "anglex": 0,
                "angley": 0,
                "anglez": 0,
                "id": 0xFDC5,
                "name": "BLasBos"
            })
        # save_obj=next(filter(lambda x: x['name']=='saveObj', roomdef['LAY ']['l0']['OBJS']))
        # 0x1C3
        # for i in range(400):
        #     cloned = save_obj.copy()
        #     cloned['id'] = 0xFC00 | (0x1C5 + i)
        #     cloned['posy'] += (i + 1) * 200
        #     roomdef['LAY ']['l0']['OBJS'].append(cloned)
        return roomdef
    patcher.set_room_patch('F000',0,patch_F000_r0)
    patcher.add_stage_oarc('F000',0,['BLastBoss','PLLastBoss'])
    patcher.do_patch()

def patch_faron():
    with get_stagepath('F100',0).open('rb') as f:
        extracted_data=nlzss11.decompress(f.read())
    stagearc=U8File.parse_u8(BytesIO(extracted_data))
    # patch layers, force layer 1
    stagedef=parseBzs(stagearc.get_file_data('dat/stage.bzs'))
    stagedef['LYSE'] = [OrderedDict((('story_flag', -1), ('night', 0), ('layer', 1)))]

    stagearc.set_file_data('dat/stage.bzs', buildBzs(stagedef))

    room0arc=U8File.parse_u8(BytesIO(stagearc.get_file_data('rarc/F100_r00.arc')))
    roomdef=parseBzs(room0arc.get_file_data('dat/room.bzs'))
    # grab the trial from layer 3 and put in on layer 0
    trial=next(filter(lambda x: x['name']=='WarpObj', roomdef['LAY ']['l3']['OBJ ']))
    trial_butterflies=next(filter(lambda x: x['name']=='InsctTg', roomdef['LAY ']['l3']['STAG']))
    # trial['posy'] += 100
    # fix object ID of trial
    trial['id']=0x02F2
    trial_butterflies['id']=0xFEF3
    roomdef['LAY ']['l3']['OBJ '].remove(trial)
    roomdef['LAY ']['l0']['OBJ '].append(trial)
    roomdef['LAY ']['l3']['STAG'].remove(trial_butterflies)
    roomdef['LAY ']['l0']['STAG'].append(trial_butterflies)
    roomdef['LAY ']['l0']['ARCN'].append('SirenEntrance')
    roomdef['LAY ']['l0']['ARCN'].append('PLSwordStick')
    roomdef['LAY ']['l0']['OBJN'].append('WarpObj')

    room0arc.set_file_data('dat/room.bzs', buildBzs(roomdef))

    roomdat=BytesIO()
    room0arc.writeto(roomdat)
    stagearc.set_file_data('rarc/F100_r00.arc', roomdat.getbuffer())

    # add the trial arc(s)
    with open('oarc/SirenEntrance.arc','rb') as f:
        arc=f.read()
        stagearc.add_file_data('oarc/SirenEntrance.arc', arc)
    with open('oarc/PLHarpPlay.arc','rb') as f:
        arc=f.read()
        stagearc.add_file_data('oarc/PLHarpPlay.arc', arc)
    with open('oarc/PLSwordStick.arc','rb') as f:
        arc=f.read()
        stagearc.add_file_data('oarc/PLSwordStick.arc', arc)
    
    stagedat=BytesIO()
    stagearc.writeto(stagedat)
    with get_stagepath('F100',0, rootpath=MODIFIED_ROOT_PATH).open('wb') as f:
        f.write(nlzss11.compress(stagedat.getbuffer()))

def demise():
    patcher = Patcher(
        actual_extract_path=Path(__file__).parent / EXTRACT_ROOT_PATH,
        modified_extract_path=Path(__file__).parent / 'temp',
        oarc_cache_path=Path(__file__).parent / 'oarc',
        keep_path=False,
        copy_unmodified=False)
    def patch_B400_r0(roomdef):
        orig_last_boss = next(filter(lambda x: x['name']=='BLasBos', roomdef['LAY ']['l1']['OBJ ']))
        las_bos = orig_last_boss.copy()
        las_bos['id'] = 0xFC06
        las_bos['posx'] += 1000
        roomdef['LAY ']['l1']['OBJ '].append(las_bos)
        las_bos = orig_last_boss.copy()
        las_bos['id'] = 0xFC07
        las_bos['posx'] -= 1000
        roomdef['LAY ']['l1']['OBJ '].append(las_bos)
        return roomdef
    patcher.set_room_patch('B400', 0, patch_B400_r0)
    patcher.do_patch()


def extract_obj_pack():
    data = (Path(__file__).parent / EXTRACT_ROOT_PATH / 'DATA' / 'files' / 'Object' / 'ObjectPack.arc.LZ').read_bytes()
    data = U8File.parse_u8(BytesIO(nlzss11.decompress(data)))
    oarc_cache_path = Path(__file__).parent / 'oarc'
    for oarc in filter(lambda x: x.endswith('.arc'), data.get_all_paths()):
        oarc_data = data.get_file_data(oarc)
        (oarc_cache_path / oarc.split('/')[-1]).write_bytes(oarc_data)

def as_yaml():
    import yaml
    extraccs = list(map(lambda k: {"stage":k[0][0], "layer":k[0][1], "oarcs": k[1]}, extracts.items()))
    print(yaml.safe_dump(extraccs))
as_yaml()
# extract_objects()
# testpatch2()
# patch_faron()
# stage, rooms = extract_stage_rooms('F100')
# assert stage == parseBzs(buildBzs(stage))
# for room in rooms.values():
#     built = buildBzs(room)
#     assert type(built) == bytes
#     assert room == parseBzs(built)
# extract_objects()
# patch_faron()
# upgrade_test()
# upgrade_with_patch()
# extract_obj_pack()
# fill_skyloft()
# demise()