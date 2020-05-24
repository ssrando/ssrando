from io import BytesIO
import os
from collections import OrderedDict
from typing import List

from bzs import parseBzs, buildBzs
import nlzss11
from u8file import U8File

EXTRACT_ROOT_PATH='../../ss-extract/actual-extract'
MODIFIED_ROOT_PATH='../../ss-extract/modified-extract'

extracts={
    'F202/F202_stg_l1.arc.LZ': [
      'oarc/GetPachinkoA.arc', # slingshot
      'oarc/GetHookShot.arc', # clawshots
      'oarc/GetMoleGloveB.arc', # mogma mitts
      'oarc/GetVacuum.arc', # gust bellows
      'oarc/GetWhip.arc', # whip
      'oarc/GetBombBag.arc', # bomb bag
    ],
    'F210/F210_stg_l0.arc.LZ':['oarc/GetMoleGloveA.arc'], # digging mitts
    'S100/S100_stg_l2.arc.LZ':['oarc/GetSizuku.arc'], # water dragon scale
    'S200/S200_stg_l2.arc.LZ':['oarc/GetEarring.arc'], # fireshield earrings
    'D100/D100_stg_l1.arc.LZ':['oarc/GetBeetleA.arc'], # beetle
    'F300/F300_stg_l0.arc.LZ':['oarc/GetBeetleB.arc'], # hook beetle
    'F000/F000_stg_l0.arc.LZ':['oarc/MoldoGut_Baby.arc'], # babies rattle?
    'F000/F000_stg_l4.arc.LZ':[
        'oarc/GetShieldWood.arc', # wooden shield
        'oarc/GetShieldHylia.arc' # hylian shield
    ],
    'F100/F100_stg_l3.arc.LZ':[ # stuff for silent realms
        'oarc/PLHarpPlay.arc',
        'oarc/SirenEntrance.arc',
        'oarc/PLSwordStick.arc'
    ]
}

def extract_objects():
    try:
        os.mkdir('oarc')
    except:
        pass
    for file, objs in extracts.items():
        with open(EXTRACT_ROOT_PATH+'/DATA/files/Stage/'+file,'rb') as f:
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
    

def patch_faron():
    with open(EXTRACT_ROOT_PATH+'/DATA/files/Stage/F100/F100_stg_l0.arc.LZ','rb') as f:
        extracted_data=nlzss11.decompress(f.read())
    stagearc=U8File.parse_u8(BytesIO(extracted_data))
    # patch layers, force layer 1
    stagedef=parseBzs(stagearc.get_file_data('dat/stage.bzs'))
    stagedef['LYSE'] = [OrderedDict((('story_flag', -1), ('night', 0), ('layer', 1)))]

    stagearc.set_file_data('dat/stage.bzs', buildBzs(stagedef))

    room0arc=U8File.parse_u8(BytesIO(stagearc.get_file_data('rarc/F100_r00.arc')))
    roomdef=parseBzs(room0arc.get_file_data('dat/room.bzs'))
    # grab the trial from layer 3 and put in on layer 0
    trial=next(filter(lambda x: x['name']==b'WarpObj\x00', roomdef['LAY ']['l3']['OBJ ']))
    trial_butterflies=next(filter(lambda x: x['name']==b'InsctTg\x00', roomdef['LAY ']['l3']['STAG']))
    # trial['posy'] += 100
    # fix object ID of trial
    trial['unk5']=0x02F2
    trial_butterflies['unk5']=0xFEF3
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
    with open('patch.arc','wb') as f:
        f.write(stagedat.getbuffer())
    with open(MODIFIED_ROOT_PATH+'/DATA/files/Stage/F100/F100_stg_l0.arc.LZ','wb') as f:
        f.write(nlzss11.compress(stagedat.getbuffer()))
    
# extract_objects()
testpatch2()
# patch_faron()
# stage, rooms = extract_stage_rooms('F100')
# assert stage == parseBzs(buildBzs(stage))
# for room in rooms.values():
#     built = buildBzs(room)
#     assert type(built) == bytes
#     assert room == parseBzs(built)