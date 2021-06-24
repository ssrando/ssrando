from context import sslib
from test_utils import get_bzs_data, get_arc_data, ALL_STAGES, STAGEPATH
import pytest
from io import BytesIO
import nlzss11
from pathlib import Path


def get_all_msb():
    all_msb = {}
    for arc in (
        Path(__file__).parent.parent / "actual-extract" / "DATA" / "files"
    ).glob("*/Object/*/*.arc"):
        with open(arc, "rb") as f:
            eventfile = sslib.U8File.parse_u8(BytesIO(f.read()))
        msb_paths = filter(
            lambda x: x.endswith(".msbf") or x.endswith(".msbt"),
            eventfile.get_all_paths(),
        )
        for msb_path in msb_paths:
            all_msb[msb_path] = eventfile.get_file_data(msb_path)
    return all_msb


def test_msb():
    for file, data in get_all_msb().items():
        print(f"testing {file}")
        assert data == bytes(sslib.buildMSB(sslib.parseMSB(data)))
