from context import sslib
from util import get_bzs_data, get_arc_data, ALL_STAGES
import pytest
from io import BytesIO
import nlzss11

@pytest.mark.parametrize("stage", ALL_STAGES)
# @pytest.mark.parametrize("stage", ['F000'])
def test_roundtrip(stage):
    with open(f'../actual-extract/DATA/files/Stage/{stage}/{stage}_stg_l0.arc.LZ','rb') as f:
        extracted_data = nlzss11.decompress(f.read())
    stagearc = sslib.U8File.parse_u8(BytesIO(extracted_data))
    assert bytes(extracted_data) == bytes(stagearc.to_buffer())
    data = stagearc.get_file_data('dat/stage.bzs')
    parsed = sslib.parseBzs(data)
    roomcount = len(parsed.get('RMPL',[]))
    for i in range(roomcount):
        roomdata = stagearc.get_file_data(f'rarc/{stage}_r{i:02}.arc')
        if not roomdata:
            continue
        roomarc = sslib.U8File.parse_u8(BytesIO(roomdata))
        assert bytes(roomdata) == bytes(roomarc.to_buffer())

def test_change_content():
    with open(f'../actual-extract/DATA/files/Stage/F000/F000_stg_l0.arc.LZ','rb') as f:
        extracted_data = nlzss11.decompress(f.read())
    stagearc = sslib.U8File.parse_u8(BytesIO(extracted_data))
    orig_bzs = stagearc.get_file_data('dat/stage.bzs')
    stagearc.set_file_data('dat/stage.bzs',b'I deleted this :)')
    new_data = stagearc.to_buffer()
    assert len(extracted_data) > len(new_data)
    stagearc = sslib.U8File.parse_u8(BytesIO(new_data))
    stagearc.set_file_data('dat/stage.bzs',orig_bzs)
    assert extracted_data == stagearc.to_buffer()
