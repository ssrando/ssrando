import sys

sys.path.insert(0, "..")
from io import BytesIO
from pathlib import Path
import yaml

from sslib.dol import DOL
from sslib.rel import REL
from sslib import U8File

# Output integers as hexadecimal.
yaml.CDumper.add_representer(
    int, lambda dumper, data: yaml.ScalarNode("tag:yaml.org,2002:int", "0x%02X" % data)
)

section_names = {
    1: "text0",
    2: "data0",
    3: "data1",
    4: "data2",
    5: "data3",
    6: "uninitialized",
}

rel_arc = U8File.parse_u8(
    BytesIO((Path("../actual-extract") / "DATA" / "files" / "rels.arc").read_bytes())
)

all_rel_info = {}
free_start_offsets = {}

# it's possible to calculate that, not necessary though
free_start_offsets["main.dol"] = 0x806782C0

for relpath in rel_arc.get_all_paths():
    rel = REL()
    rel.read(BytesIO(rel_arc.get_file_data(relpath)))
    relname = relpath.split("/")[-1]
    rel_info = {}
    free_start_offset = 0
    for sec_num, section in enumerate(rel.sections):
        if sec_num >= 7 or sec_num == 0:
            assert section.offset == 0 and section.length == 0
        else:
            free_start_offset = max(section.offset + section.length, free_start_offset)
            rel_info[section_names[sec_num]] = {
                "offset": section.offset,
                "length": section.length,
            }
            # print(f'{section_names[sec_num]}: offset 0x{section.offset:04x}, length 0x{section.length:04x}')
    all_rel_info[relname] = rel_info
    free_start_offsets[relname] = free_start_offset

with open("rel_info.yaml", "w") as f:
    yaml.dump(
        all_rel_info, f, Dumper=yaml.CDumper, default_flow_style=False, sort_keys=False
    )

with open("free_space_start_offsets2.txt", "w") as f:
    yaml.dump(
        free_start_offsets,
        f,
        Dumper=yaml.CDumper,
        default_flow_style=False,
        sort_keys=False,
    )
