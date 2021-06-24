import nlzss11
from io import BytesIO
from sslib import U8File
import glob
from pathlib import Path

bzscache = {}

STAGEPATH = Path(__file__).parent / ".." / "actual-extract" / "DATA" / "files" / "Stage"
ALL_STAGES = list(map(lambda x: Path(x).parts[-1], STAGEPATH.glob("*")))


def get_bzs_data(stage, room=None):
    if (stage, room) in bzscache:
        return bzscache[(stage, room)]
    with open(STAGEPATH / f"/{stage}/{stage}_stg_l0.arc.LZ", "rb") as f:
        extracted_data = nlzss11.decompress(f.read())
    stagearc = U8File.parse_u8(BytesIO(extracted_data))
    if room == None:
        stage = stagearc.get_file_data("dat/stage.bzs")
        bzscache[(stage, room)] = stage
        return stage
    else:
        roomarc = U8File.parse_u8(
            BytesIO(stagearc.get_file_data(f"rarc/{stage}_r{room:02}.arc"))
        )
        roomparsed = roomarc.get_file_data("dat/room.bzs")
        bzscache[(stage, room)] = roomparsed
        return roomparsed


def get_arc_data(stage, layer=0):
    # caching arcs might be a bad idea since they can be like 6MB...
    with open(STAGEPATH / f"{stage}/{stage}_stg_l{layer}.arc.LZ", "rb") as f:
        return nlzss11.decompress(f.read())
