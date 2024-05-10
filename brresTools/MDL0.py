# https://wiki.tockdom.com/wiki/MDL0_(File_Format)
from dataclasses import dataclass
from io import BufferedIOBase
from itertools import chain
from typing import List
import numpy as np
import struct

# NB this format is pretty complex, so for now we only support some primitive
# in-place operations such as vertex or UV shuffling.
# this allows us to skip the complicated re-assembling and offset shifts
# in the future this may be extended to support more things


@dataclass
class InPlacePatch:
    offset: int
    bytes: bytes


class MDL0:
    patches: List[InPlacePatch]

    def __init__(
        self,
        dataBuffer: BufferedIOBase,
        section_offsets,
        file_size: int,
        start_offset: int,
    ):
        self.dataBuffer: BufferedIOBase = dataBuffer
        self.section_offsets = section_offsets
        self.file_size = file_size
        self.start_offset = start_offset
        self.patches = []

    @staticmethod
    def parse_MDL0(dataBuffer: BufferedIOBase, start_offset: int):
        dataBuffer.seek(start_offset + 0x04)
        file_size = struct.unpack(">I", dataBuffer.read(4))[0]

        dataBuffer.seek(start_offset + 0x08)
        version_number = struct.unpack(">I", dataBuffer.read(4))[0]
        if version_number == 8:
            num_sections = 11
        elif version_number == 11:
            num_sections = 14

        dataBuffer.seek(start_offset + 0x10)
        section_offsets = struct.unpack(
            ">" + "I" * num_sections, dataBuffer.read(4 * num_sections)
        )

        return MDL0(
            dataBuffer=dataBuffer,
            section_offsets=section_offsets,
            file_size=file_size,
            start_offset=start_offset,
        )
    
    def get_uv_entry_header(self, buffer_name: str):
        from .brres import BRRES, IndexGroupNode, SubFileNode

        index_group_offset = self.section_offsets[5] + self.start_offset
        root_node = IndexGroupNode("root")
        BRRES.parse_index_group_entries(
            data=self.dataBuffer,
            indexGroupNode=root_node,
            group_start_offset=index_group_offset,
            nonrecursive=True,
        )

        entry_offset = None
        for child in root_node.childNodes:
            if child.name == buffer_name and isinstance(child, SubFileNode):
                entry_offset = child.dataOffset
                break

        if not entry_offset:
            raise ValueError("did not find " + buffer_name)

        self.dataBuffer.seek(entry_offset)
        header = struct.unpack(">IiiiIIIBBH", self.dataBuffer.read(0x20))
        [
            _length,
            _mld0_off,
            data_offset,
            _name_offset,
            _index,
            comp_count,
            data_fmt,
            _divisor,
            _stride,
            coord_count,
        ] = header
        if comp_count != 0x01:
            raise ValueError("cannot decode non-XY UV")
        if data_fmt != 0x03:
            raise ValueError("cannot decode non-uint16 UV")

        return entry_offset, data_offset, coord_count
    
    def get_uvs(self, buffer_name: str) -> List[List[int]]:
        entry_offset, data_offset, coord_count = self.get_uv_entry_header(
            buffer_name
        )
        self.dataBuffer.seek(entry_offset + data_offset)

        coords = []
        for _ in range(coord_count):
            coord = struct.unpack(">hh", self.dataBuffer.read(0x4))
            coords.append(coord)

        return coords

    def set_uvs(self, buffer_name: str, uvs: List[List[int]]):
        entry_offset, data_offset, coord_count = self.get_uv_entry_header(
            buffer_name
        )
        if len(uvs) != coord_count:
            raise ValueError("cannot in-place patch vertices due to count mismatch")

        bytes = bytearray()
        coords_flat = list(chain.from_iterable(uvs))
        bytes.extend(struct.pack(">" + "hh" * coord_count, *coords_flat))
        self.patches.append(
            InPlacePatch(entry_offset + data_offset - self.start_offset, bytes)
        )


    def get_vertex_entry_header(self, buffer_name: str):
        from .brres import BRRES, IndexGroupNode, SubFileNode

        index_group_offset = self.section_offsets[2] + self.start_offset
        root_node = IndexGroupNode("root")
        BRRES.parse_index_group_entries(
            data=self.dataBuffer,
            indexGroupNode=root_node,
            group_start_offset=index_group_offset,
            nonrecursive=True,
        )

        entry_offset = None
        for child in root_node.childNodes:
            if child.name == buffer_name and isinstance(child, SubFileNode):
                entry_offset = child.dataOffset
                break

        if not entry_offset:
            raise ValueError("did not find " + buffer_name)

        self.dataBuffer.seek(entry_offset)
        header = struct.unpack(">IiiiIIIBBH", self.dataBuffer.read(0x20))
        [
            _length,
            _mld0_off,
            data_offset,
            _name_offset,
            _index,
            comp_count,
            data_fmt,
            _divisor,
            _stride,
            vertex_count,
        ] = header
        if comp_count != 0x01:
            raise ValueError("cannot decode non-XYZ vertices")
        if data_fmt != 0x04:
            raise ValueError("cannot decode non-float vertices")

        return entry_offset, data_offset, vertex_count

    def get_vertices(self, buffer_name: str) -> List[List[float]]:
        entry_offset, data_offset, vertex_count = self.get_vertex_entry_header(
            buffer_name
        )
        self.dataBuffer.seek(entry_offset + data_offset)

        vertices = []
        for _ in range(vertex_count):
            coords = struct.unpack(">fff", self.dataBuffer.read(0xC))
            vertices.append(coords)

        return vertices

    def set_vertices(self, buffer_name: str, vertices: List[List[float]]):
        entry_offset, data_offset, vertex_count = self.get_vertex_entry_header(
            buffer_name
        )
        if len(vertices) != vertex_count:
            raise ValueError("cannot in-place patch vertices due to count mismatch")

        bytes = bytearray()
        floats = list(chain.from_iterable(vertices))
        bytes.extend(struct.pack(">" + "fff" * vertex_count, *floats))
        self.patches.append(
            InPlacePatch(entry_offset + data_offset - self.start_offset, bytes)
        )

    def to_bytes(self):
        buf: bytearray = bytearray()

        self.dataBuffer.seek(self.start_offset)
        buf += self.dataBuffer.read(self.file_size)

        for patch in self.patches:
            buf[patch.offset : patch.offset + len(patch.bytes)] = patch.bytes

        return buf
