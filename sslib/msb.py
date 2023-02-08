from collections import OrderedDict
import struct
from typing import NewType

from .utils import unpack, toStr, toBytes

FLOWTYPES = {"type1": 1, "switch": 2, "type3": 3, "start": 4}

ParsedMsb = NewType("ParsedMsb", OrderedDict)

# both in utf-8
CONTROL_REPLACEMENTS = {
    "<r<": "\x0e\x00\x03\x02\x00",  # red
    "<rd<": "\x0e\x00\x03\x02\x01",  # also red
    "<y+<": "\x0e\x00\x03\x02\x02",  # yellow-white
    "<b<": "\x0e\x00\x03\x02\x03",  # blue
    "<g<": "\x0e\x00\x03\x02\x04",  # green
    "<y<": "\x0e\x00\x03\x02\x05",  # yellow
    "<g+<": "\x0e\x00\x03\x02\x07",  # green rupee green
    "<b+<": "\x0e\x00\x03\x02\x08",  # blue rupee blue
    "<r+<": "\x0e\x00\x03\x02\x09",  # red-white
    "<s<": "\x0e\x00\x03\x02\x0A",  # silver
    "<ye<": "\x0e\x00\x03\x02\x0B",  # gold rupee gold
    "<blk<": "\x0e\x00\x03\x02\x0C",  # rupoor
    ">>": "\x0e\x00\x03\x02\uFFFF",  # end color
    # start of option token, '-' means cancel (B) option
    "[1]": "\x0e\x01\x00\x02\uFFFF",
    "[2-]": "\x0e\x01\x01\x02\x00",
    "[2]": "\x0e\x01\x01\x02\uFFFF",
    "[3-]": "\x0e\x01\x02\x02\x00",
    "[3]": "\x0e\x01\x02\x02\uFFFF",
    "[4-]": "\x0e\x01\x03\x02\x00",
    "[4]": "\x0e\x01\x03\x02\uFFFF",
    "<numeric arg0>": "\x0e\x02\x03\x06\x00\x00\xcd",
    "<numeric arg1>": "\x0e\x02\x03\x06\x00\x01\xcd",
    "<numeric arg2>": "\x0e\x02\x03\x06\x00\x02\xcd",
    "<numeric arg3>": "\x0e\x02\x03\x06\x00\x03\xcd",
    "<numeric arg4>": "\x0e\x02\x03\x06\x00\x04\xcd",
    "<string arg0>": "\x0e\x02\x02\x04\x00\x00",
    "<string arg1>": "\x0e\x02\x02\x04\x00\x01",
    "<string arg2>": "\x0e\x02\x02\x04\x00\x02",
    "<heroname>": "\x0e\x02\x00\x00",
}


def process_control_sequences(data: str) -> str:
    for orig, replaced in CONTROL_REPLACEMENTS.items():
        data = data.replace(orig, replaced)
    return data


def parseMSB(data: bytes) -> ParsedMsb:
    parsed = OrderedDict()
    if data[:10] == b"MsgFlwBn\xFE\xFF":
        parsed["type"] = "MsgFlwBn"
        assert data[10:16] == b"\x00\x00\x00\x03\x00\x02"
    elif data[:10] == b"MsgStdBn\xFE\xFF":
        parsed["type"] = "MsgStdBn"
        assert data[10:16] == b"\x00\x00\x01\x03\x00\x03"
    else:
        raise Exception("Unsupported filetype.")
    assert struct.unpack(">i", data[0x12:0x16])[0] == len(data)
    pos = 0x20
    while pos < len(data):
        seg_header = data[pos : pos + 0x10]
        pos += 0x10
        seg_id, seg_len, zero1, zero2 = struct.unpack(">4siii", seg_header)
        assert zero1 == 0
        assert zero2 == 0
        seg_id = seg_id.decode("ascii")
        seg_data = data[pos : pos + seg_len]
        pos += seg_len
        pos += -pos % 0x10
        assert not seg_id in parsed
        if seg_id == "FLW3":
            parsed["FLW3"] = OrderedDict()
            parsed["FLW3"]["flow"] = []
            parsed["FLW3"]["branch_points"] = []
            count1, count2 = struct.unpack(">hh12x", seg_data[:0x10])
            for i in range(count1):  # for every node in FLW3
                item = unpack(
                    "type subType param1 param2 next param3 param4 param5",
                    ">bb2xhhhhhh",
                    seg_data[0x10 + 0x10 * i : 0x20 + 0x10 * i],
                )
                assert item["type"] in (1, 2, 3, 4)
                item["type"] = ["type1", "switch", "type3", "start"][item["type"] - 1]
                parsed["FLW3"]["flow"].append(item)
            for i in range(count2):  # for every branch point
                item = struct.unpack(
                    ">h",
                    seg_data[
                        0x10 + 0x10 * count1 + 2 * i : 0x12 + 0x10 * count1 + 2 * i
                    ],
                )[0]
                parsed["FLW3"]["branch_points"].append(item)
        elif seg_id == "FEN1" or seg_id == "LBL1":
            parsed[seg_id] = []
            count = struct.unpack(">i", seg_data[:4])[0]
            for i in range(count):
                count, ptr = struct.unpack(">ii", seg_data[4 + 8 * i : 0xC + 8 * i])
                entrypoint_group = []
                for _ in range(count):
                    strlen = seg_data[ptr]
                    string = seg_data[1 + ptr : 1 + ptr + strlen].decode("ascii")
                    value = struct.unpack(
                        ">i", seg_data[1 + ptr + strlen : 5 + ptr + strlen]
                    )[0]
                    entrypoint = OrderedDict()
                    entrypoint["name"] = string
                    entrypoint["value"] = value
                    entrypoint_group.append(entrypoint)
                    ptr += 5 + strlen
                parsed[seg_id].append(entrypoint_group)
        elif seg_id == "ATR1":
            parsed["ATR1"] = []
            count, dimension = struct.unpack(">ii", seg_data[:8])
            for i in range(count):
                cur_list = []
                for j in range(dimension):
                    cur_list.append(seg_data[8 + i * dimension + j])
                parsed["ATR1"].append(cur_list)
        elif seg_id == "TXT2":
            parsed["TXT2"] = []
            count = struct.unpack(">i", seg_data[:4])[0]
            indices = [
                struct.unpack(">i", seg_data[4 + 4 * i : 8 + 4 * i])[0]
                for i in range(count)
            ]
            for i in range(count):  # for every item of text
                bytestring = seg_data[
                    indices[i] : (indices[i + 1] if i + 1 < count else seg_len) - 2
                ]
                parsed["TXT2"].append(bytestring)
        else:
            raise Exception(f"Unsupported seg_id: {seg_id}.")
    return parsed


def buildMSB(msb: ParsedMsb) -> bytes:
    if msb["type"] == "MsgFlwBn":
        header = b"MsgFlwBn\xFE\xFF"
        header += b"\x00\x00\x00\x03\x00\x02"
    elif msb["type"] == "MsgStdBn":
        header = b"MsgStdBn\xFE\xFF"
        header += b"\x00\x00\x01\x03\x00\x03"
    else:
        raise Exception(f'Unsupported filetype: {msb["type"]}.')
    header = bytearray(header + b"\x00" * 16)
    total_body = b""
    for seg_id, seg_data in msb.items():
        body = b""
        if seg_id == "type":
            continue
        if seg_id == "FLW3":
            body += struct.pack(
                ">hh", len(seg_data["flow"]), len(seg_data["branch_points"])
            )
            body += b"\x00" * 12
            for flow in seg_data["flow"]:
                body += struct.pack(
                    ">bbhhhhhhh",
                    FLOWTYPES[flow["type"]],
                    flow["subType"],
                    0,
                    flow["param1"],
                    flow["param2"],
                    flow["next"],
                    flow["param3"],
                    flow["param4"],
                    flow["param5"],
                )
            for branch_point in seg_data["branch_points"]:
                body += struct.pack(">h", branch_point)
        elif seg_id == "FEN1" or seg_id == "LBL1":
            data = b""
            offset = len(seg_data) * 8 + 4
            seg_body = b""
            for subseg in seg_data:
                data += struct.pack(">ii", len(subseg), offset + len(seg_body))
                for subsub in subseg:
                    seg_body += struct.pack(">b", len(subsub["name"]))
                    seg_body += subsub["name"].encode("ascii")
                    seg_body += struct.pack(">i", subsub["value"])
            data += seg_body
            body += struct.pack(">i", len(seg_data))
            body += data
        elif seg_id == "ATR1":
            dimension = None
            for atr in seg_data:
                if dimension is None:
                    dimension = len(atr)
                else:
                    assert dimension == len(atr)
            body += struct.pack(">ii", len(seg_data), dimension)
            for atr in seg_data:
                for val in atr:
                    body += struct.pack(">b", val)
        elif seg_id == "TXT2":
            body += struct.pack(">i", len(seg_data))
            offset = 4 * len(seg_data) + 4
            seg_header = b""
            seg_body = b""
            for txt in seg_data:
                seg_header += struct.pack(">i", offset + len(seg_body))
                seg_body += txt + b"\x00\x00"
            body += seg_header
            body += seg_body
        else:
            raise Exception(f"Unsupported seg_id: {seg_id}.")
        total_body += seg_id.encode("ascii")
        total_body += struct.pack(">i", len(body)) + 8 * b"\x00"
        total_body += body
        total_body += (-len(total_body) % 0x10) * b"\xAB"
    total_length = len(header) + len(total_body)
    header[0x12] = (total_length >> 24) & 0xFF
    header[0x13] = (total_length >> 16) & 0xFF
    header[0x14] = (total_length >> 8) & 0xFF
    header[0x15] = total_length & 0xFF
    return header + total_body
