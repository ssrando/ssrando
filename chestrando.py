from pathlib import Path
import random

from sslib import AllPatcher
from sslib.utils import write_bytes_create_dirs

def chestrando():

    # PPC machine code for: (some context missing, uVar5 is the itemid)
    # bVar1 = chestSizeForItem[uVar5];
    # param_1->chest_size = bVar1;
    # if (bVar1 == 3) {
    #   setItem(param_1,0x1ff - uVar5);
    # }
    actual_code = bytes.fromhex("38 7f 0e 08 7c 03 20 ae 98 1c 12 09 28 00 00 03 40 82 00 14 20 04 01 ff 7f 83 e3 78 54 04 04 3e")
    # PPC machine code for: (some context missing)
    # param_1->chest_size = (param_1->params >> 4) & 3;
    # // unconditional jump to skip now unneeded block
    patched_code = bytes.fromhex("80 1c 00 04 54 00 e7 be 98 1c 12 09 28 00 00 03 48 00 00 14 20 04 01 ff 7f 83 e3 78 54 04 04 3e")
    patcher = AllPatcher(
        actual_extract_path=Path(__file__).parent / 'actual-extract',
        modified_extract_path=Path(__file__).parent / 'modified-extract',
        oarc_cache_path=Path(__file__).parent / 'oarc',
        copy_unmodified=False)
    def patch_tbox(tbox):
        if (tbox['params1'] >> 28) == 0:
            return
        itemid = tbox['anglez'] & 0x1FF
        if itemid > 0x100:
            #goddess chest
            itemid = 0x1FF - itemid
            tbox['anglez'] = (tbox['anglez'] & ~0x1FF) | itemid
            # patch chest subtype param (constant for goddess chest is 3)
            subtype = 3
        else:
            subtype = random.randint(0,2)
            # subtype = 1
        tbox['params1'] = (tbox['params1'] & ~0x30) | (subtype << 4)

    def random_chests(bzsdata, stage, room):
        for o in bzsdata.get('OBJS',[]):
            if o['name'] == 'TBox':
                patch_tbox(o)
        for x in bzsdata['LAY '].values():
            for o in x.get('OBJS',[]):
                if o['name'] == 'TBox':
                    patch_tbox(o)
        return bzsdata
    patcher.set_bzs_patch(random_chests)
    patcher.do_patch()
    # patch dol
    orig_dol = bytearray((patcher.actual_extract_path / 'DATA' / 'sys' / 'main.dol').read_bytes())
    code_pos = orig_dol.find(actual_code)
    assert code_pos != -1
    assert orig_dol.find(actual_code, code_pos+1) == -1
    orig_dol[code_pos:code_pos+len(actual_code)] = patched_code
    write_bytes_create_dirs(patcher.modified_extract_path / 'DATA' / 'sys' / 'main.dol', orig_dol)

if __name__ == '__main__':
    chestrando()