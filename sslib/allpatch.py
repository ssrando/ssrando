from pathlib import Path
from typing import Callable, Iterable, Dict, Optional
import re
from io import BytesIO
from collections import defaultdict

import nlzss11
from .bzs import ParsedBzs, parseBzs, buildBzs
from .msb import ParsedMsb, parseMSB, buildMSB
from .u8file import U8File

STAGE_REGEX = re.compile('(.+)_stg_l([0-9]+).arc.LZ')
EVENT_REGEX = re.compile('([0-9])-[A-Za-z]+.arc')
LANGUAGES = {'EU': 'en_GB', 'US': 'en_US'} # no idea for JP
EXTRACTS = {
    ('D003_0', 0): ['GetTriForceSingle'], # Triforce part
    ('D301', 0): ['GetBowA'], # Bow
    ('F001r', 3):[
        'GetKobunALetter',  # Cawlin's Letter
        'GetPouchA'        # Adventure Pouch
    ],
    ('F002r', 1):[
        'GetPouchB',  # Extra Pouch Slot
        'GetMedal',        # all Medals
        'GetNetA'        # Bug Net
        ],
    ('F004r', 0):[
        'GetPachinkoB',  # Scatershot
        'GetBowB',        # Iron Bow
        'GetBowC',        # Sacred Bow
        'GetBeetleC',  # Quick beetle
        'GetBeetleD',        # Though Beetle
        'GetNetB'        # Big Bug Net
        # a bunch more bottles and other stuff is also here
        ],
    ('F202', 1): [
      'GetPachinkoA', # slingshot
      'GetHookShot', # clawshots
      'GetMoleGloveB', # mogma mitts
      'GetVacuum', # gust bellows
      'GetWhip', # whip
      'GetBombBag' # bomb bag
    ],
    ('F210', 0):['GetMoleGloveA'], # digging mitts
    ('S100', 2):['GetSizuku'], # water dragon scale
    ('S200', 2):['GetEarring'], # fireshield earrings
    ('D100', 1):['GetBeetleA'], # beetle
    ('F300', 0):['GetBeetleB'], # hook beetle
    ('F301_5', 0):['GetMapSea'], # Sand Sea Map
    ('F402', 2):['GetHarp'], # all Songs & Harp
    ('F000', 0):[
        'MoldoGut_Baby', # babies rattle
        'GetSeedLife' # LTS
    ],
    ('F000', 4):[
        'GetShieldWood', # wooden shield
        'GetShieldHylia' # hylian shield
    ],
    ('F100', 3):[ # stuff for silent realms
        'PLHarpPlay',
        'SirenEntrance',
        'PLSwordStick'
    ],
    ('F020', 1):['GetBirdStatue'], # Bird statuette
    ('F023', 0):['GetTerryCage'], # Beedle's Beetle
}

class AllPatcher:

    def __init__(self, actual_extract_path: Path, modified_extract_path: Path, oarc_cache_path: Path, keep_path: bool=True, copy_unmodified: bool=True):
        """
        Creates a new instance of the AllPatcher, which patches the game files but with a single callback for each resource type
        actual_extract_path: a path pointing to the root directory of the extracted game, so that it has the subdirectories DATA and UPDATE
        modified_extract_path: a path where to write the patched files to, should be a copy of the actual extract if intended to be repacked into an iso
        keep_path: whether or not to keep the path structure of the original files, set to True if repacking the modified files into an iso and to files if using Riivolution
        copy_unmodified: If unmodified Stage and Event files should be copied, other files are never copied
        """
        self.actual_extract_path = actual_extract_path
        self.modified_extract_path = modified_extract_path
        self.oarc_cache_path = oarc_cache_path
        self.keep_path = keep_path
        self.copy_unmodified = copy_unmodified
        self.stage_oarc_add={}
        self.bzs_patch=None
        self.event_patch=None
    
    def add_stage_oarc(self, stage: str, layer: int, oarcs: Iterable[str]):
        self.stage_oarc_add[(stage, layer)] = oarcs
    
    def set_bzs_patch(self, patchfunc: Callable[[ParsedBzs, str, Optional[int]], Optional[ParsedBzs]]):
        """
        The function gets called for every bzs (so stages and rooms), it passes the parsed bzs,
        the stage name and the room id or None, if it's a stage and not a room
        if the return value of the function is not None, it will override the game files,
        otherwise nothing will change
        """
        self.bzs_patch = patchfunc
    
    def set_event_patch(self, event: str, patchfunc: Callable[[ParsedMsb], ParsedMsb]):
        """
        The function gets called for every event file (msbt, msbf)
        if the return value of the function is not None, it will override the game files,
        otherwise nothing will change
        """
        self.event_patche = patchfunc
    
    def create_oarc_cache(self):
        self.oarc_cache_path.mkdir(parents=True, exist_ok=True)
        for (stage, layer), objs in EXTRACTS.items():
            data = (self.actual_extract_path/'DATA'/'files'/'Stage'/f'{stage}'/f'{stage}_stg_l{layer}.arc.LZ').read_bytes()
            data = nlzss11.decompress(data)
            data = U8File.parse_u8(BytesIO(data))

            for objname in objs:
                outdata=data.get_file_data(f'oarc/{objname}.arc')
                (self.oarc_cache_path / f'{objname}.arc').write_bytes(outdata)
    
    def do_patch(self):
        self.modified_extract_path.mkdir(parents=True, exist_ok=True)

        # stages
        for stagepath in (self.actual_extract_path/'DATA'/'files'/'Stage').glob('*/*_stg_l*.arc.LZ'):
            match = STAGE_REGEX.match(stagepath.parts[-1])
            stage = match[1]
            layer = int(match[2])
            if self.keep_path:
                modified_stagepatch = self.modified_extract_path/'DATA'/'files'/'Stage'/f'{stage}'/f'{stage}_stg_l{layer}.arc.LZ'
            else:
                modified_stagepatch = self.modified_extract_path/f'{stage}_stg_l{layer}.arc.LZ'
            modified = False
            stagedata = nlzss11.decompress(stagepath.read_bytes())
            stageu8 = U8File.parse_u8(BytesIO(stagedata))
            # add additional arcs if needed
            for arc in self.stage_oarc_add.get((stage, layer), []):
                oarc_bytes = (self.oarc_cache_path / f'{arc}.arc').read_bytes()
                stageu8.add_file_data(f'oarc/{arc}.arc', oarc_bytes)
                modified = True
            if layer == 0:
                stagebzs = parseBzs(stageu8.get_file_data('dat/stage.bzs'))
                # patch stage
                if self.bzs_patch:
                    newstagebzs = self.bzs_patch(stagebzs,stage,None)
                    if newstagebzs is not None:
                        stageu8.set_file_data('dat/stage.bzs', buildBzs(newstagebzs))
                        modified = True
                # patch rooms
                for roomid in range(len(stagebzs.get('RMPL',[0]))):
                    roomdata = stageu8.get_file_data(f'rarc/{stage}_r{roomid:02}.arc')
                    if roomdata is None:
                        continue
                    roomarc = U8File.parse_u8(BytesIO(roomdata))
                    roombzs = parseBzs(roomarc.get_file_data('dat/room.bzs'))
                    roombzs = self.bzs_patch(roombzs, stage, roomid)
                    if roombzs is not None:
                        roomarc.set_file_data('dat/room.bzs', buildBzs(roombzs))
                        stageu8.set_file_data(f'rarc/{stage}_r{roomid:02}.arc', roomarc.to_buffer())
                        modified = True
            # repack u8 and compress it if modified
            if modified:
                stagedata = stageu8.to_buffer()
                modified_stagepatch.write_bytes(nlzss11.compress(stagedata))
                print(f'patched {stage} l{layer}')
            elif self.copy_unmodified:
                modified_stagepatch.write_bytes(stagepath.read_bytes())
                print(f'copied {stage} l{layer}')

        # events
        # eventrootpath = None
        # modified_eventrootpath = None

        # # check target language
        # for path, lang in LANGUAGES.items():
        #     if (self.actual_extract_path/'DATA'/'files'/path).exists():
        #         eventrootpath = self.actual_extract_path/'DATA'/'files'/path/'Object'/lang
        #         if self.keep_path:
        #             modified_eventrootpath = self.modified_extract_path/'DATA'/'files'/path/'Object'/lang
        #         else:
        #             modified_eventrootpath = self.modified_extract_path
        #         break
        # TODO
        # if eventrootpath == None:
        #     raise Exception('Event files not found')
        # for eventpath in eventrootpath.glob('*.arc'):
        #     filename = eventpath.parts[-1]
        #     match = EVENT_REGEX.match(filename)
        #     eventfilenum = match[1]
        #     modified_eventpath = modified_eventrootpath / filename
        #     eventarc = U8File.parse_u8(BytesIO(eventpath.read_bytes()))
        #     for file, patchfunc in self.event_patches.items():
        #         if not str(eventfilenum) == file[0]: # first letter determines which file to use
        #             continue
        #         parsedMsb = parseMSB(eventarc.get_file_data(f'{filename[:-4]}/{file}'))
        #         parsedMsb = patchfunc(parsedMsb)
        #         eventarc.set_file_data(f'{filename[:-4]}/{file}', buildMSB(parsedMsb))
        #     modified_eventpath.write_bytes(eventarc.to_buffer())
        #     print(f'patched {filename}')