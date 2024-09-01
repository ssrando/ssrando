from .TEX0 import TEX0

from io import BufferedIOBase
import struct
from typing import List

MAGIC_HEADER = b"bres"
BOM_HEADER = b"\xfe\xff"
SECTION_TYPES = [
    b"MDL0",
    b"TEX0",
    b"SRT0",
    b"CHR0",
    b"PAT0",
    b"CLR0",
    b"SHP0",
    b"SCN0",
    b"PLT0",
    b"VIS0",
    b"RASD", # Follows the Same Formats as others with 4-byte sig.
    b"EXT ", # Not an actual sig, but used for data in external folder.
]


class FileNotFoundError(Exception):
    pass


class Node:
    def __init__(self, nodeType: str, name: str):
        self.nodeType: str = nodeType
        self.name: str = name


class IndexGroupNode(Node):
    def __init__(self, name: str):
        super().__init__("group", name=name)
        self.childNodes: List[Node] = []

    def add_child(self, newChild: Node):
        if self.get_child(newChild.name) is not None:
            print(f"{newChild.name} already exists in {self.name}")
            return
        self.childNodes.append(newChild)

    def get_child(self, childName: str) -> Node | None:
        for child in self.childNodes:
            if child.name == childName:
                return child
        return None


class SubFileNode(Node):
    def __init__(self, fileType: str, name: str, dataOffset: int):
        super().__init__(nodeType=fileType, name=name)
        self.dataOffset = dataOffset


class BRRES:
    def __init__(self, dataBuffer: BufferedIOBase, rootGroupNode: IndexGroupNode):
        self.dataBuffer: BufferedIOBase = dataBuffer
        self.rootGroupNode: IndexGroupNode = rootGroupNode

    @staticmethod
    def parse_brres(dataBuffer: BufferedIOBase):
        dataBuffer.seek(0)
        if dataBuffer.read(4) != MAGIC_HEADER:
            raise Exception("Invalid magic header.")
        if dataBuffer.read(2) != BOM_HEADER:
            raise Exception("Invalid byte order mark.")
        dataBuffer.seek(12)  # skip to root offset data
        root_offset = struct.unpack(">H", dataBuffer.read(2))[0]

        dataBuffer.seek(root_offset + 8)  # skip over root header

        group_start = dataBuffer.tell()

        rootGroupNode = IndexGroupNode("root")
        BRRES.parse_index_group_entries(
            data=dataBuffer,
            indexGroupNode=rootGroupNode,
            group_start_offset=group_start,
        )
        return BRRES(dataBuffer=dataBuffer, rootGroupNode=rootGroupNode)

    @staticmethod
    def parse_index_group_entries(
        data: BufferedIOBase, indexGroupNode: IndexGroupNode, group_start_offset: int
    ):
        data.seek(group_start_offset)
        data.seek(data.tell() + 4)
        num_of_subfolders = struct.unpack(">L", data.read(4))[0]
        data.seek(data.tell() + 16)  # skips reference point entry

        entries_start = data.tell()
        for i in range(num_of_subfolders):
            data.seek(
                entries_start + (i * 16) + 8
            )  # move to current entry and skip to name offset
            name_offset = struct.unpack(">L", data.read(4))[0]
            data_offset = struct.unpack(">L", data.read(4))[0]

            data.seek(group_start_offset + name_offset - 4)

            name_len = struct.unpack(">L", data.read(4))[0]
            name = str(struct.unpack(f">{name_len}s", data.read(name_len))[0], "utf-8")

            data.seek(group_start_offset + data_offset)

            identifier = data.read(4)

            if identifier in SECTION_TYPES:
                entryNode = SubFileNode(
                    fileType=identifier,
                    name=name,
                    dataOffset=(group_start_offset + data_offset),
                )
            elif indexGroupNode.name == "External":
                entryNode = SubFileNode(
                    fileType=b"EXT ",
                    name=name,
                    dataOffset=(group_start_offset + data_offset),
                )
            else:
                entryNode = IndexGroupNode(name=name)
                BRRES.parse_index_group_entries(
                    data=data,
                    indexGroupNode=entryNode,
                    group_start_offset=(group_start_offset + data_offset),
                )

            indexGroupNode.add_child(entryNode)

    def get_all_paths(self) -> list[str]:
        def _get_all_paths(
            group_node: IndexGroupNode, folder_path: str, name_list: list[str]
        ):
            for node in group_node.childNodes:
                full_path = folder_path + "/" + node.name
                if type(node) is SubFileNode:
                    name_list.append(full_path)
                if node.nodeType == "group":
                    _get_all_paths(node, full_path, name_list)

        str_list = []
        _get_all_paths(self.rootGroupNode, "", str_list)
        return str_list

    def get_file_node(self, path: str) -> SubFileNode:
        path = path.lstrip("/")
        currentNode: Node = self.rootGroupNode
        for part in path.split("/"):
            if type(currentNode) is not IndexGroupNode:
                raise FileNotFoundError(
                    f"Invalid path: {path} in get_file_node- file not final part of path."
                )
            found = False
            for node in currentNode.childNodes:
                if node.name == part:
                    currentNode = node
                    found = True
                    break
            if not found:
                raise FileNotFoundError(
                    f"Invalid path: {path} in get_file_node- {part} not found."
                )

        if type(currentNode) is not SubFileNode:
            raise FileNotFoundError(
                f"Invalid path: {path} in get_file_node- {currentNode.name} is a folder, not a file."
            )

        return currentNode

    def get_file_data(self, path: str) -> any:
        file = self.get_file_node(path=path)
        dataOffset = file.dataOffset

        match file.nodeType:
            case b"MDL0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"TEX0":
                tex0: TEX0 = TEX0.parse_TEX0(
                    dataBuffer=self.dataBuffer, start_offset=dataOffset
                )
                rawImageData = tex0.get_image_data()
                return tex0.convert_raw_image_data_to_RGBA(data=rawImageData)
            case b"SRT0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"CHR0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"PAT0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"CLR0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"SHP0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"SCN0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"PLT0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"VIS0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"RASD":
                # Usually found in External Folder, but follows the common
                # signature pattern as other brres types
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"EXT ":
                # This just returns the bytes to be parsed from the caller.
                # This is because data stored in the external folder can be of
                #    any type. The Caller needs to truncate to the size needed
                self.dataBuffer.seek(dataOffset)
                return self.dataBuffer.read()
            case _:
                raise FileNotFoundError(
                    f"Invalid subfile type {file.nodeType} in get_file_data."
                )

    def set_file_data(self, path: str, data: any):
        file = self.get_file_node(path=path)
        dataOffset = file.dataOffset

        match file.nodeType:
            case b"MDL0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"TEX0":
                tex0: TEX0 = TEX0.parse_TEX0(
                    dataBuffer=self.dataBuffer, start_offset=dataOffset
                )
                rawImageData = tex0.convert_RGBA_to_raw_image_data(data=data)

                if len(rawImageData) != tex0.numberOfBytesInImage:
                    raise Exception(
                        "Cannot replace data- Supplied data not same length as original data."
                    )

                self.dataBuffer.seek(tex0.imageDataOffset)
                self.dataBuffer.write(rawImageData)
            case b"SRT0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"CHR0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"PAT0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"CLR0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"SHP0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"SCN0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"PLT0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"VIS0":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"RASD":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case b"EXT ":
                raise Exception(f"Unsupported file type {file.nodeType}.")
            case _:
                raise FileNotFoundError(
                    f"Invalid subfile type {file.nodeType} in get_file_data."
                )

    def to_buffer(self) -> BufferedIOBase:
        self.dataBuffer.seek(0)
        return self.dataBuffer


# debug method
# @staticmethod
# def print_nodes(groupNode: IndexGroupNode, layersDeep:int = 0):
#     if layersDeep is 0:
#         print('root')
#     layersDeep+= 1
#     for node in groupNode.childNodes:
#         print('\t'*layersDeep, node.name, node.nodeType)
#         if type(node) is SubFileNode:
#             print('\t'*layersDeep, node.dataOffset)
#         if node.nodeType == 'group':
#             BRRES.print_nodes(node, layersDeep=layersDeep)
