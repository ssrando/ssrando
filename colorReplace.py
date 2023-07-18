import cv2
import numpy as np
import colorsys


def replace_mask(texture: np.mat, mask: np.mat, new_color: str) -> np.mat:
    mask_inv = cv2.bitwise_not(mask)

    new_color = cvt_hex_to_RGBA(new_color)
    new_color = [i / 255 for i in new_color]

    unmaskedTexture = cv2.bitwise_and(texture, texture, mask=mask)

    maskedTexture = cv2.bitwise_or(texture, texture, mask=mask_inv)
    maskedTexture = cv2.cvtColor(maskedTexture, cv2.COLOR_BGR2HSV)
    hChannel = maskedTexture[:, :, 0]
    sChannel = maskedTexture[:, :, 1]
    vChannel = maskedTexture[:, :, 2]
    targetHSV = colorsys.rgb_to_hsv(new_color[0], new_color[1], new_color[2])
    hChannel = (targetHSV[0] * 180) + (0 * hChannel)
    sChannel = (targetHSV[1] * 255) + (0 * sChannel)
    vChannel = targetHSV[2] * (vChannel * (255 / vChannel.max()))
    maskedTexture[:, :, 0] = hChannel
    maskedTexture[:, :, 1] = sChannel
    maskedTexture[:, :, 2] = vChannel

    maskedTexture = cv2.cvtColor(maskedTexture, cv2.COLOR_HSV2BGR)
    maskedTexture = cv2.cvtColor(maskedTexture, cv2.COLOR_BGR2RGBA)
    maskedTexture = cv2.bitwise_or(maskedTexture, maskedTexture, mask=mask_inv)

    final = maskedTexture + unmaskedTexture

    return final


def process_texture(texture: np.array, maskPaths: list, colors: list) -> np.array:
    masks = get_masks_from_mask_paths(maskPaths=maskPaths)
    i = 0
    modified_texture: np.array = texture
    for i, m in enumerate(masks):
        modified_texture = replace_mask(
            texture=modified_texture, mask=m, new_color=colors[i]
        )

    return modified_texture


def get_masks_from_mask_paths(maskPaths: list) -> list:
    masks: list = []
    for path in maskPaths:
        mask = cv2.imread(path, 0)
        masks.append(mask)

    return masks


def cvt_hex_to_RGBA(hex: str) -> list:
    RGBA = []
    for i in (0, 2, 4, 6):
        decimal = int(hex[i + 1 : i + 3], 16)
        RGBA.append(decimal)

    RGBAList = [RGBA[0], RGBA[1], RGBA[2], 255]

    return RGBAList
