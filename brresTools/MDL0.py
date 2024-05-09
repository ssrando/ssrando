# https://wiki.tockdom.com/wiki/MDL0_(File_Format)
from io import BufferedIOBase
import numpy as np
import struct

# NB this format is pretty complex, so for now we only support some primitive
# in-place operations such as vertex or UV shuffling.
# this allows us to skip the complicated re-assembling and offset shifts
# in the future this may be extended to support more things

class MDL0:
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
        section_offsets = struct.unpack(">" + "I" * num_sections, dataBuffer.read(4*num_sections))

        return MDL0(
            dataBuffer=dataBuffer,
            section_offsets=section_offsets,
            file_size=file_size,
            start_offset=start_offset
        )
    

    def get_polygon_vertex_indices(self, polygon_name: str):
        from .brres import BRRES, IndexGroupNode, SubFileNode
        """Returns a polygon's vertex index buffer. 
        """
        polygons_group_offset = self.section_offsets[10] + self.start_offset
        root_node = IndexGroupNode("root")
        BRRES.parse_index_group_entries(
            data=self.dataBuffer,
            indexGroupNode=root_node,
            group_start_offset=polygons_group_offset,
            nonrecursive=True
        )

        polygon = None
        
        for child in root_node.childNodes:
            if child.name == polygon_name and isinstance(child, SubFileNode):
                polygon = child.dataOffset
                break

        if not polygon:
            return None
        
        # TODO: read vertex data



    def set_polygon_vertex_buffer(self, polygon_name: str, buffer):
        """Sets a polygon's vertex index buffer. Must have the same length
           as the original buffer, and can obviously only reference the same
           vertices, but perhaps in a different order. Useful to rotate some
           models for puzzles."""
        pass

    def to_bytes(self):
        buf: bytearray = bytearray()

        self.dataBuffer.seek(self.start_offset)
        buf += self.dataBuffer.read(self.file_size)

        return buf