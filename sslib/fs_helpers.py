import struct
from io import BytesIO

PADDING_BYTES = b"This is padding data to alignme"


class InvalidOffsetError(Exception):
    pass


def data_len(data):
    data_length = data.seek(0, 2)
    return data_length


def make_copy_data(data):
    copy_data = read_all_bytes(data)
    return BytesIO(copy_data)


def read_all_bytes(data):
    data.seek(0)
    return data.read()


def read_bytes(data, offset, length):
    data.seek(offset)
    return data.read(length)


def write_bytes(data, offset, raw_bytes):
    data.seek(offset)
    data.write(raw_bytes)


def read_and_unpack_bytes(data, offset, length, format_string):
    data.seek(offset)
    requested_data = data.read(length)
    unpacked_data = struct.unpack(format_string, requested_data)
    return unpacked_data


def write_and_pack_bytes(data, offset, new_values, format_string):
    packed_data = struct.pack(format_string, *new_values)
    data.seek(offset)
    data.write(packed_data)


def read_str(data, offset, length):
    data_length = data.seek(0, 2)
    if offset + length > data_length:
        raise InvalidOffsetError(
            "Offset 0x%X, length 0x%X is past the end of the data (length 0x%X)."
            % (offset, length, data_length)
        )
    data.seek(offset)
    string = data.read(length).decode("shift_jis")
    string = string.rstrip("\0")  # Remove trailing null bytes
    return string


def try_read_str(data, offset, length):
    try:
        return read_str(data, offset, length)
    except UnicodeDecodeError:
        return None
    except InvalidOffsetError:
        return None


def read_str_until_null_character(data, offset):
    data_length = data.seek(0, 2)
    if offset > data_length:
        raise InvalidOffsetError(
            "Offset 0x%X is past the end of the data (length 0x%X)."
            % (offset, data_length)
        )

    temp_offset = offset
    str_length = 0
    while temp_offset < data_length:
        data.seek(temp_offset)
        char = data.read(1)
        if char == b"\0":
            break
        else:
            str_length += 1
        temp_offset += 1

    data.seek(offset)
    str = data.read(str_length).decode("shift_jis")

    return str


def write_str(data, offset, new_string, max_length):
    # Writes a fixed-length string.
    # Although it is fixed-length, it still must have a null character terminating it, so the real max length is one less than the passed max_length argument.

    str_len = len(new_string)
    if str_len >= max_length:
        raise Exception(
            'String "%s" is too long (max length including null byte: 0x%X).'
            % (new_string, max_length)
        )

    padding_length = max_length - str_len
    null_padding = b"\x00" * padding_length
    new_value = new_string.encode("shift_jis") + null_padding

    data.seek(offset)
    data.write(new_value)


def write_magic_str(data, offset, new_string, max_length):
    # Writes a fixed-length string that does not have to end with a null byte.
    # This is for magic file format identifiers.

    str_len = len(new_string)
    if str_len > max_length:
        raise Exception(
            "String %s is too long (max length 0x%X)." % (new_string, max_length)
        )

    padding_length = max_length - str_len
    null_padding = b"\x00" * padding_length
    new_value = new_string.encode("shift_jis") + null_padding

    data.seek(offset)
    data.write(new_value)


def write_str_with_null_byte(data, offset, new_string):
    # Writes a non-fixed length string.

    str_len = len(new_string)
    write_str(data, offset, new_string, str_len + 1)


def read_u8(data, offset):
    if not offset is None:
        data.seek(offset)
    return struct.unpack(">B", data.read(1))[0]


def read_u16(data, offset):
    if not offset is None:
        data.seek(offset)
    return struct.unpack(">H", data.read(2))[0]


def read_u24(data, offset):
    if not offset is None:
        data.seek(offset)
    d = struct.unpack(">BH", data.read(3))
    return (d[0] << 16) | d[1]


def read_u32(data, offset):
    if not offset is None:
        data.seek(offset)
    return struct.unpack(">I", data.read(4))[0]


def read_float(data, offset):
    if not offset is None:
        data.seek(offset)
    return struct.unpack(">f", data.read(4))[0]


def read_s8(data, offset):
    if not offset is None:
        data.seek(offset)
    return struct.unpack(">b", data.read(1))[0]


def read_s16(data, offset):
    if not offset is None:
        data.seek(offset)
    return struct.unpack(">h", data.read(2))[0]


def read_s32(data, offset):
    if not offset is None:
        data.seek(offset)
    return struct.unpack(">i", data.read(4))[0]


def write_u8(data, offset, new_value):
    new_value = struct.pack(">B", new_value)
    if not offset is None:
        data.seek(offset)
    data.write(new_value)


def write_u16(data, offset, new_value):
    new_value = struct.pack(">H", new_value)
    if not offset is None:
        data.seek(offset)
    data.write(new_value)


def write_u24(data, offset, value):
    if not offset is None:
        data.seek(offset)
    high = value >> 16
    low = value & 0xFFFF
    data.write(struct.pack(">BH", high, low))


def write_u32(data, offset, new_value):
    new_value = struct.pack(">I", new_value)
    if not offset is None:
        data.seek(offset)
    data.write(new_value)


def write_float(data, offset, new_value):
    new_value = struct.pack(">f", new_value)
    if not offset is None:
        data.seek(offset)
    data.write(new_value)


def write_s8(data, offset, new_value):
    new_value = struct.pack(">b", new_value)
    if not offset is None:
        data.seek(offset)
    data.write(new_value)


def write_s16(data, offset, new_value):
    new_value = struct.pack(">h", new_value)
    if not offset is None:
        data.seek(offset)
    data.write(new_value)


def write_s32(data, offset, new_value):
    new_value = struct.pack(">i", new_value)
    if not offset is None:
        data.seek(offset)
    data.write(new_value)


def align_data_to_nearest(data, size, padding_bytes=PADDING_BYTES):
    current_end = data_len(data)
    next_offset = current_end + (size - current_end % size) % size
    padding_needed = next_offset - current_end
    data.seek(current_end)
    padding = padding_bytes * (padding_needed // len(padding_bytes))
    padding += padding_bytes[: padding_needed % len(padding_bytes)]
    data.write(padding)


def pad_offset_to_nearest(offset, size):
    next_offset = offset + (size - offset % size) % size
    return next_offset
