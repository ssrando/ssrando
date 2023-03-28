from io import BufferedIOBase
import numpy as np
import struct

IMAGE_FORMATS_NAMES = {
    0: "I4",
    1: "I8",
    2: "IA4",
    3: "IA8",
    4: "RGB565",
    5: "RGB5A3",
    6: "RGBA32",
    8: "C4",
    9: "C8",
    10: "C14X2",
    14: "CMPR",
}

IMAGE_FORMATS_BITS_PER_PIXEL = {
    0: 4,
    1: 8,
    2: 8,
    3: 16,
    4: 16,
    5: 16,
    6: 32,
    8: 4,
    9: 8,
    10: 16,
    14: 4,
}

IMAGE_FORMATS_BLOCK_HEIGHT = {
    0: 8,
    1: 4,
    2: 4,
    3: 4,
    4: 4,
    5: 4,
    6: 4,
    8: 8,
    9: 4,
    10: 4,
    14: 8,
}

IMAGE_FORMATS_BLOCK_WIDTH = {
    0: 8,
    1: 8,
    2: 8,
    3: 4,
    4: 4,
    5: 4,
    6: 4,
    8: 8,
    9: 8,
    10: 4,
    14: 8,
}

MASK5 = 0b011111
MASK6 = 0b111111


class TEX0:
    def __init__(
        self,
        dataBuffer: BufferedIOBase,
        imgDataOffset: int,
        imageFormat: str,
        width: int,
        height: int,
        numberOfBytesInImage: int,
    ):
        self.dataBuffer: BufferedIOBase = dataBuffer
        self.imageDataOffset: int = imgDataOffset
        self.imageFormat: str = imageFormat
        self.width: int = width
        self.height: int = height
        self.numberOfBytesInImage: int = numberOfBytesInImage

    @staticmethod
    def parse_TEX0(dataBuffer: BufferedIOBase, start_offset: int):
        dataBuffer.seek(start_offset + 16)
        section_0_offset = struct.unpack(">I", dataBuffer.read(4))[0]
        img_data_offset = start_offset + section_0_offset

        dataBuffer.seek(start_offset + 28)
        width = struct.unpack(">H", dataBuffer.read(2))[0]
        height = struct.unpack(">H", dataBuffer.read(2))[0]
        image_format = struct.unpack(">I", dataBuffer.read(4))[0]

        number_of_bytes_in_image = (
            height * width * IMAGE_FORMATS_BITS_PER_PIXEL[image_format]
        ) // 8

        return TEX0(
            dataBuffer=dataBuffer,
            imgDataOffset=img_data_offset,
            imageFormat=image_format,
            width=width,
            height=height,
            numberOfBytesInImage=number_of_bytes_in_image,
        )

    def get_image_data(self) -> bytes:
        self.dataBuffer.seek(self.imageDataOffset)
        imageData = self.dataBuffer.read(self.numberOfBytesInImage)
        return imageData

    def convert_raw_image_data_to_RGBA(self, data: bytes) -> np.array:
        match IMAGE_FORMATS_NAMES[self.imageFormat]:
            case "I4":
                return self.cvt_I4_to_RGBA(data=data)
            case "I8":
                pass
            case "IA4":
                pass
            case "IA8":
                pass
            case "RGB565":
                return self.cvt_RGB565_to_RGBA(data=data)
            case "RGB5A3":
                pass
            case "RGBA32":
                pass
            case "C4":
                pass
            case "C8":
                pass
            case "C14X2":
                pass
            case "CMPR":
                return self.cvt_CMPR_to_RGBA(data=data)
            case _:
                raise Exception(
                    f"Invalid image format {self.imageDataOffset} in convert_raw_image_data_to_RGBA"
                )

    def convert_RGBA_to_raw_image_data(self, data: np.array) -> bytes:
        match IMAGE_FORMATS_NAMES[self.imageFormat]:
            case "I4":
                pass
            case "I8":
                pass
            case "IA4":
                pass
            case "IA8":
                pass
            case "RGB565":
                return self.cvt_RGBA_to_RGB565(data=data)
            case "RGB5A3":
                pass
            case "RGBA32":
                pass
            case "C4":
                pass
            case "C8":
                pass
            case "C14X2":
                pass
            case "CMPR":
                return self.cvt_RGBA_to_CMPR(data=data)
            case _:
                raise Exception(
                    f"Invalid image format {self.imageDataOffset} in convert_RGBA_to_raw_image_data"
                )

    def cvt_I4_to_RGBA(self, data: bytes) -> np.array:
        RGBAList = []

        for byte in data:
            formattedByte = bin(byte)[2:].zfill(8)
            color1 = int(formattedByte[:4].zfill(8), 2)
            color2 = int(formattedByte[4:].zfill(8), 2)
            r = color1 * 0x11
            g = color1 * 0x11
            b = color1 * 0x11
            a = 0xFF
            RGBAList.append((r, g, b, a))
            r = color2 * 0x11
            g = color2 * 0x11
            b = color2 * 0x11
            RGBAList.append((r, g, b, a))

        return self.reorder_blocks(data=RGBAList)

    def cvt_RGB565_to_RGBA(self, data: bytes) -> np.array:
        RGBAList = []

        for colorStart in range(0, len(data), 2):
            RGB565 = struct.unpack(">H", data[colorStart : colorStart + 2])[0]
            RGBAList.append(self.cvt_single_RGB565_to_RGBA(RGB565))

        return self.reorder_blocks(data=RGBAList)

    def cvt_RGBA_to_RGB565(self, data: np.array) -> bytes:
        dataList: list = self.reorder_blocks_back(data=data)

        RGB565List: bytearray = bytearray()

        for color in dataList:
            RGB565 = self.cvt_single_RGBA_to_RGB565(color)
            RGB565List += struct.pack(">H", RGB565)

        return RGB565List

    def cvt_CMPR_to_RGBA(self, data: bytes) -> np.array:
        RGBAList = []

        for blockStart in range(0, len(data), 32):
            block = data[blockStart : blockStart + 32]  # CMPR have 32 byte long blocks
            blockRGBAList = []
            for subBlockStart in (0, 8, 16, 24):
                subBlock = block[
                    subBlockStart : subBlockStart + 8
                ]  # CMPR have four 8 byte long sub-blocks
                c0 = struct.unpack(">H", subBlock[:2])[0]
                c1 = struct.unpack(">H", subBlock[2:4])[0]
                transparency = False
                if c1 >= c0:
                    transparency = True
                c0 = self.cvt_single_RGB565_to_RGBA(c0)
                c1 = self.cvt_single_RGB565_to_RGBA(c1)
                cTable = struct.unpack(">L", subBlock[4:])[0]

                if transparency:
                    c2 = (
                        ((c0[0] + c1[0]) // 2),
                        ((c0[1] + c1[1]) // 2),
                        ((c0[2] + c1[2]) // 2),
                        255,
                    )
                    c3 = (0, 0, 0, 0)
                else:
                    c2 = (
                        (((2 * c0[0]) + c1[0]) // 3),
                        (((2 * c0[1]) + c1[1]) // 3),
                        (((2 * c0[2]) + c1[2]) // 3),
                        255,
                    )
                    c3 = (
                        ((c0[0] + (2 * c1[0])) // 3),
                        ((c0[1] + (2 * c1[1])) // 3),
                        ((c0[2] + (2 * c1[2])) // 3),
                        255,
                    )

                for i in range(30, -2, -2):
                    colorCode = (cTable >> i) & 0x03
                    match colorCode:
                        case 0:
                            blockRGBAList.append(c0)
                        case 1:
                            blockRGBAList.append(c1)
                        case 2:
                            blockRGBAList.append(c2)
                        case 3:
                            blockRGBAList.append(c3)

            # restrucures sub-blocks in each block to be correctly ordered
            splitblockRGBAList = [
                (blockRGBAList[:16], blockRGBAList[16:32]),
                (blockRGBAList[32:48], blockRGBAList[48:]),
            ]
            newBlockTopHalf = []
            newBlockBottomHalf = []

            for currentRow in range(0, 16, 4):
                newBlockTopHalf += splitblockRGBAList[0][0][currentRow : currentRow + 4]
                newBlockTopHalf += splitblockRGBAList[0][1][currentRow : currentRow + 4]
                newBlockBottomHalf += splitblockRGBAList[1][0][
                    currentRow : currentRow + 4
                ]
                newBlockBottomHalf += splitblockRGBAList[1][1][
                    currentRow : currentRow + 4
                ]

            RGBAList += newBlockTopHalf
            RGBAList += newBlockBottomHalf

        return self.reorder_blocks(data=RGBAList)

    def cvt_RGBA_to_CMPR(self, data: np.array) -> bytes:
        CMPRBytes: bytearray = bytearray()

        dataList: list = self.reorder_blocks_back(data=data)
        numOfBlocks = len(dataList) // 64

        for currentBlock in range(numOfBlocks):
            block = dataList[(currentBlock * 64) : ((currentBlock * 64) + 64)]
            blockTopHalf = block[:32]
            blockBottomHalf = block[32:]
            splitBlockRGBAList1: list = []
            splitBlockRGBAList2: list = []
            splitBlockRGBAList3: list = []
            splitBlockRGBAList4: list = []

            for currentRow in range(0, 32, 8):
                splitBlockRGBAList1 += blockTopHalf[currentRow : currentRow + 4]
                splitBlockRGBAList2 += blockTopHalf[currentRow + 4 : currentRow + 8]
                splitBlockRGBAList3 += blockBottomHalf[currentRow : currentRow + 4]
                splitBlockRGBAList4 += blockBottomHalf[currentRow + 4 : currentRow + 8]

            blockRGBAlist = (
                splitBlockRGBAList1
                + splitBlockRGBAList2
                + splitBlockRGBAList3
                + splitBlockRGBAList4
            )

            for subBlockStart in (0, 16, 32, 48):
                subBlockRGBAList = blockRGBAlist[subBlockStart : subBlockStart + 16]
                subBlockRGB565List = []

                transparency = False
                colors = []
                for color in subBlockRGBAList:
                    if color[3] == 0:
                        transparency = True
                        subBlockRGB565List.append("ALPHA")
                        continue
                    RGB565Color = self.cvt_single_RGBA_to_RGB565(color)
                    if RGB565Color not in colors:
                        colors.append(RGB565Color)
                    subBlockRGB565List.append(RGB565Color)

                colors.sort()
                if transparency:
                    if (
                        len(colors) == 0
                    ):  # for full sub block of alpha, nothing will be added to colors list
                        c0 = self.cvt_single_RGBA_to_RGB565((255, 255, 255, 0))
                        c1 = c0
                        c2 = c0
                        c3 = c0
                    else:
                        c0 = colors[0]
                        c1 = colors[-1]
                        RGBAc0 = self.cvt_single_RGB565_to_RGBA(c0)
                        RGBAc1 = self.cvt_single_RGB565_to_RGBA(c1)
                        RGBAc2 = (
                            ((RGBAc0[0] + RGBAc1[0]) // 2),
                            ((RGBAc0[1] + RGBAc1[1]) // 2),
                            ((RGBAc0[2] + RGBAc1[2]) // 2),
                            255,
                        )
                        c2 = self.cvt_single_RGBA_to_RGB565(RGBAc2)
                        c3 = self.cvt_single_RGBA_to_RGB565((255, 255, 255, 0))
                else:
                    c0 = colors[-1]
                    c1 = colors[0]
                    RGBAc0 = self.cvt_single_RGB565_to_RGBA(c0)
                    RGBAc1 = self.cvt_single_RGB565_to_RGBA(c1)
                    RGBAc2 = (
                        (((2 * RGBAc0[0]) + RGBAc1[0]) // 3),
                        (((2 * RGBAc0[1]) + RGBAc1[1]) // 3),
                        (((2 * RGBAc0[2]) + RGBAc1[2]) // 3),
                        255,
                    )
                    RGBAc3 = (
                        ((RGBAc0[0] + (2 * RGBAc1[0])) // 3),
                        ((RGBAc0[1] + (2 * RGBAc1[1])) // 3),
                        ((RGBAc0[2] + (2 * RGBAc1[2])) // 3),
                        255,
                    )
                    c2 = self.cvt_single_RGBA_to_RGB565(RGBAc2)
                    c3 = self.cvt_single_RGBA_to_RGB565(RGBAc3)

                cTable = 0b0
                for i, color in enumerate(subBlockRGB565List):
                    if color == "ALPHA":
                        cTable = (cTable << 2) + 3
                        continue

                    diff = abs(color - c0)
                    closest = 0

                    if diff > abs(color - c1):
                        diff = abs(color - c1)
                        closest = 1
                    if diff > abs(color - c2):
                        diff = abs(color - c2)
                        closest = 2
                    if not transparency:
                        if diff > abs(color - c3):
                            closest = 3

                    cTable = (cTable << 2) + closest

                CMPRBytes += struct.pack(">H", c0)
                CMPRBytes += struct.pack(">H", c1)
                CMPRBytes += struct.pack(">I", cTable)

        return CMPRBytes

    def cvt_single_RGBA_to_RGB565(self, data: tuple[int, int, int, int]) -> int:
        R = data[0]
        G = data[1]
        B = data[2]

        conR = (R // 0x8) << 11
        conG = (G // 0x4) << 5
        conB = B // 0x8

        RGB565 = conR | conG | conB

        return RGB565

    def cvt_single_RGB565_to_RGBA(self, data: int) -> tuple[int, int, int, int]:
        R = ((data >> 11) & MASK5) * 0x8
        G = ((data >> 5) & MASK6) * 0x4
        B = ((data) & MASK5) * 0x8

        return (R, G, B, 255)

    def reorder_blocks(self, data: list) -> np.array:
        blockHeight = IMAGE_FORMATS_BLOCK_HEIGHT[self.imageFormat]
        blockWidth = IMAGE_FORMATS_BLOCK_WIDTH[self.imageFormat]
        yBlocks = -(self.height // -blockHeight)
        xBlocks = -(self.width // -blockWidth)

        reorderedArray = np.empty(shape=(self.height, self.width, 4), dtype=np.uint8)

        i = 0

        for currentYBlock in range(yBlocks):
            for currentXBlock in range(xBlocks):
                for currentRow in range(blockHeight):
                    for currentPixelInRow in range(blockWidth):
                        currentData = data[i]
                        reorderedArray[(currentYBlock * blockHeight) + currentRow][
                            (currentXBlock * blockWidth) + currentPixelInRow
                        ] = currentData
                        i += 1

        return reorderedArray

    def reorder_blocks_back(self, data: np.array) -> list:
        blockHeight = IMAGE_FORMATS_BLOCK_HEIGHT[self.imageFormat]
        blockWidth = IMAGE_FORMATS_BLOCK_WIDTH[self.imageFormat]
        yBlocks = -(self.height // -blockHeight)
        xBlocks = -(self.width // -blockWidth)

        reorderedList = []

        for currentYBlock in range(yBlocks):
            for currentXBlock in range(xBlocks):
                for currentRow in range(blockHeight):
                    for currentPixelInRow in range(blockWidth):
                        currentPixInArray = data[
                            (currentYBlock * blockHeight) + currentRow
                        ][(currentXBlock * blockWidth) + currentPixelInRow]
                        reorderedList.append(
                            (
                                currentPixInArray[0],
                                currentPixInArray[1],
                                currentPixInArray[2],
                                currentPixInArray[3],
                            )
                        )

        return reorderedList
