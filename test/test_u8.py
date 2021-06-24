from context import sslib
from test_utils import get_bzs_data, get_arc_data, ALL_STAGES, STAGEPATH
import pytest
from io import BytesIO
import nlzss11
from pathlib import Path


@pytest.mark.parametrize("stage", ALL_STAGES)
# @pytest.mark.parametrize("stage", ['F000'])
def test_roundtrip(stage):
    with open(STAGEPATH / f"{stage}" / f"{stage}_stg_l0.arc.LZ", "rb") as f:
        extracted_data = nlzss11.decompress(f.read())
    stagearc = sslib.U8File.parse_u8(BytesIO(extracted_data))
    assert extracted_data == stagearc.to_buffer()
    data = stagearc.get_file_data("dat/stage.bzs")
    parsed = sslib.parseBzs(data)
    roomcount = len(parsed.get("RMPL", []))
    for i in range(roomcount):
        roomdata = stagearc.get_file_data(f"rarc/{stage}_r{i:02}.arc")
        if not roomdata:
            continue
        roomarc = sslib.U8File.parse_u8(BytesIO(roomdata))
        assert roomdata == roomarc.to_buffer()


def test_change_content():
    with open(STAGEPATH / "F000" / "F000_stg_l0.arc.LZ", "rb") as f:
        extracted_data = nlzss11.decompress(f.read())
    stagearc = sslib.U8File.parse_u8(BytesIO(extracted_data))
    orig_bzs = stagearc.get_file_data("dat/stage.bzs")
    stagearc.set_file_data("dat/stage.bzs", b"I deleted this :)")
    new_data = stagearc.to_buffer()
    assert len(extracted_data) > len(new_data)
    stagearc = sslib.U8File.parse_u8(BytesIO(new_data))
    stagearc.set_file_data("dat/stage.bzs", orig_bzs)
    assert extracted_data == stagearc.to_buffer()


def test_add_delete():
    with open(STAGEPATH / "F000" / "F000_stg_l0.arc.LZ", "rb") as f:
        extracted_data = nlzss11.decompress(f.read())
    stagearc = sslib.U8File.parse_u8(BytesIO(extracted_data))
    stagearc.delete_file("oarc/GetGaragara.arc")
    stagearc.add_file_data("oarc/NewModel.arc", b"look at this new cool model")
    paths = list(stagearc.get_all_paths())
    stagedata = stagearc.to_buffer()
    stagearc = sslib.U8File.parse_u8(BytesIO(stagedata))
    assert stagearc.get_file_data("oarc/GetGaragara.arc") is None
    new_paths = list(stagearc.get_all_paths())
    assert len(paths) == len(new_paths)
    assert all([a == b for a, b in zip(paths, new_paths)])
