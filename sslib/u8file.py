from io import BufferedIOBase, BytesIO
from .fs_helpers import (
    read_u8,
    read_u24,
    read_u32,
    read_str_until_null_character,
    write_u24,
    write_u32,
)
from collections import OrderedDict
from typing import Tuple, List, Optional
import struct

MAGIC_HEADER = b"U\xaa8-"


class InvalidU8File(Exception):
    pass


class Node:
    def __init__(self, node_type, string_offset):
        self.node_type = node_type
        self.string_offset = string_offset

    def set_name(self, name):
        self.name = name

    def write_header_to(self, buffer):
        raise NotImplementedError

    def write_data_to(self, u8file, buffer):
        raise NotImplementedError


class DirNode(Node):
    def __init__(self, string_offset, parent_index, next_parent_index):
        super().__init__(b"\x01", string_offset)
        self.parent_index = parent_index
        self.new_parent_index = parent_index
        self.next_parent_index = next_parent_index
        self.new_next_parent_index = next_parent_index

    def write_header_to(self, buffer):
        buffer.write(b"\x01")
        write_u24(buffer, None, self.string_offset)
        write_u32(buffer, None, self.new_parent_index)
        write_u32(buffer, None, self.new_next_parent_index)


class FileNode(Node):
    def __init__(self, string_offset, data_offset, data_length):
        super().__init__(b"\x00", string_offset)
        self.data_offset = data_offset
        self.new_data_offset = data_offset
        self.data_length = data_length
        self.data_overwrite = None

    def write_header_to(self, buffer):
        buffer.write(b"\x00")
        write_u24(buffer, None, self.string_offset)
        write_u32(buffer, None, self.new_data_offset)
        write_u32(buffer, None, self.get_length())

    def write_data_to(self, u8file, buffer):
        buffer.seek(self.new_data_offset)
        if self.data_overwrite:
            buffer.write(self.data_overwrite)
        else:
            u8file.data.seek(self.data_offset)
            buffer.write(u8file.data.read(self.data_length))

    def get_length(self):
        if self.data_overwrite:
            return len(self.data_overwrite)
        else:
            return self.data_length

    def set_data(self, data: bytes):
        self.data_overwrite = data

    def get_data(self, u8file):
        if self.data_overwrite:
            return self.data_overwrite
        else:
            u8file.data.seek(self.data_offset)
            return u8file.data.read(self.data_length)


class U8File:
    # constant
    FIRST_NODE_OFFSET = 0x20

    def __init__(
        self,
        data: BufferedIOBase,
        nodes: List[Node],
    ):
        self.data = data
        self.nodes = nodes

    @staticmethod
    def parse_u8(data: BufferedIOBase):
        nodes = []
        data.seek(0)
        if data.read(4) != MAGIC_HEADER:
            raise InvalidU8File("Invalid magic header.")
        first_node_offset = struct.unpack(">I", data.read(4))[0]
        if first_node_offset != U8File.FIRST_NODE_OFFSET:
            raise InvalidU8File("Invalid first node offset.")
        _all_node_size = struct.unpack(">I", data.read(4))[0]
        _start_data_offset = struct.unpack(">I", data.read(4))[0]
        # read the first node, to figure out where the filenames start
        # should be a directory
        data.seek(first_node_offset)
        if data.read(1) != b"\x01":
            raise InvalidU8File
        # the root node always starts at string offset 0
        if read_u24(data, None) != 0:
            raise InvalidU8File
        # it has no parent directory
        if read_u32(data, None) != 0:
            raise InvalidU8File
        # total count of nodes with 12 bytes each, after that the string
        # section starts
        total_node_count = read_u32(data, None)
        node = DirNode(0, 0, total_node_count)
        node.set_name("")
        nodes.append(node)
        string_pool_base_offset = first_node_offset + total_node_count * 12
        for i in range(1, total_node_count):
            data.seek(first_node_offset + i * 12)
            nodetype = data.read(1)
            string_offset = read_u24(data, None)
            if nodetype == b"\x00":
                data_offset = read_u32(data, None)
                data_length = read_u32(data, None)
                node = FileNode(string_offset, data_offset, data_length)
                node.set_name(
                    read_str_until_null_character(
                        data, string_pool_base_offset + string_offset
                    )
                )
                nodes.append(node)
            elif nodetype == b"\x01":
                parent_index = read_u32(data, None)
                next_parent_index = read_u32(data, None)
                node = DirNode(string_offset, parent_index, next_parent_index)
                node.set_name(
                    read_str_until_null_character(
                        data, string_pool_base_offset + string_offset
                    )
                )
                nodes.append(node)
            else:
                raise InvalidU8File(f"Unknown nodetype {nodetype}.")
        return U8File(data, nodes)

    def writeto(self, buffer: BufferedIOBase):
        self.first_node_offset = 0x20
        # do strings
        string_pool_base_offset = self.first_node_offset + len(self.nodes) * 12
        buffer.seek(string_pool_base_offset)
        for node in self.nodes:
            node.string_offset = buffer.tell() - string_pool_base_offset
            buffer.write(node.name.encode("ASCII"))
            buffer.write(b"\x00")
        self.all_node_size = buffer.tell() - self.first_node_offset
        # padding before data section to 16
        pad = 32 - (buffer.tell() % 32)
        if pad == 32:
            pad = 0
        buffer.write(b"\x00" * pad)
        self.data_offset = buffer.tell()

        buffer.seek(0)
        buffer.write(MAGIC_HEADER)
        buffer.write(struct.pack(">I", self.first_node_offset))
        buffer.write(struct.pack(">I", self.all_node_size))
        buffer.write(struct.pack(">I", self.data_offset))
        buffer.seek(self.first_node_offset)
        cur_data_offset = self.data_offset

        for i, node in enumerate(self.nodes):
            if node.node_type == b"\x00":
                # todo modified/unmodified
                node.new_data_offset = cur_data_offset
                buffer.seek(cur_data_offset)
                node.write_data_to(self, buffer)
                cur_data_offset += node.get_length()
                # pad to 32
                pad = 32 - (buffer.tell() % 32)
                if pad == 32:
                    pad = 0
                cur_data_offset += pad
            buffer.seek(self.first_node_offset + i * 12)
            node.write_header_to(buffer)

        buffer.seek(cur_data_offset)
        # final padding to 16
        pad = 16 - (cur_data_offset % 16)
        if pad == 16:
            pad = 0
        buffer.write(b"\x00" * pad)

    def to_buffer(self):
        out = BytesIO()
        self.writeto(out)
        return out.getbuffer()

    def get_file(self, path: str):
        index = self._get_file_index(path)
        if index is None:
            return None
        else:
            return self.nodes[index]

    def _get_file_index(self, path: str) -> int:
        """
        Returns the index of the file, if found
        If the file isn't found, None is returned
        """
        total_nodes = self.nodes[0].new_next_parent_index
        foundindex = 1
        path = path.lstrip("/")
        for part in path.split("/"):
            currnode = self.nodes[foundindex]
            if isinstance(currnode, DirNode):
                while part != currnode.name:
                    foundindex = currnode.new_next_parent_index
                    if foundindex >= total_nodes:
                        return None
                    currnode = self.nodes[foundindex]
                foundindex += 1
            else:
                while part != currnode.name:
                    foundindex += 1
                    if foundindex >= total_nodes:
                        return None
                    currnode = self.nodes[foundindex]
        return foundindex

    def get_file_data(self, path: str) -> Optional[bytes]:
        file = self.get_file(path)
        if not file:
            return None
        return file.get_data(self)

    def set_file_data(self, path: str, data: bytes):
        file = self.get_file(path)
        if not file:
            raise Exception("File not found.")
        file.set_data(data)

    def add_file_data(self, path: str, data: bytes):
        # if the file already exists, just overwrite it
        already_exists_file = self.get_file(path)
        if already_exists_file:
            already_exists_file.set_data(data)
            return
        # can't add directories for now
        new_node = FileNode(
            -1,
            -1,
            -1,
        )
        total_nodes = self.nodes[0].new_next_parent_index
        foundindex = 1
        for part in path.split("/"):
            currnode = self.nodes[foundindex]
            if isinstance(currnode, DirNode):
                while part != currnode.name:
                    foundindex = currnode.new_next_parent_index
                    if foundindex >= total_nodes:
                        break
                    currnode = self.nodes[foundindex]
                foundindex += 1
            else:
                while part < currnode.name:
                    foundindex += 1
                    if foundindex >= total_nodes:
                        break
                    currnode = self.nodes[foundindex]
                new_node.set_name(part)
        # found place to insert the new node in
        new_node.set_data(data)
        # fix all node references: if it's higer than index add one
        for node in self.nodes:
            if isinstance(node, DirNode):
                if node.new_parent_index >= foundindex:
                    node.new_parent_index += 1
                if node.new_next_parent_index >= foundindex:
                    node.new_next_parent_index += 1
        self.nodes.insert(foundindex, new_node)

    def delete_file(self, path: str):
        fileindex = self._get_file_index(path)
        if fileindex is None:
            return None
        for node in self.nodes:
            if isinstance(node, DirNode):
                if node.new_parent_index >= fileindex:
                    node.new_parent_index -= 1
                if node.new_next_parent_index >= fileindex:
                    node.new_next_parent_index -= 1
        return self.nodes.pop(fileindex)

    def get_all_paths(self, start=0) -> List[str]:
        """
        Returns a list of all paths in the ARC,
        paths are strings and start with a '/'
        """
        all_paths = []
        next_out = self.nodes[start].new_next_parent_index
        dirname = self.nodes[start].name
        indx = start + 1
        while indx < next_out:
            currnode = self.nodes[indx]
            if isinstance(currnode, DirNode):
                all_paths.extend(self.get_all_paths(indx))
                indx = currnode.new_next_parent_index
            else:
                all_paths.append(currnode.name)
                indx += 1
        return map(lambda x: dirname + "/" + x, all_paths)
