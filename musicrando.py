import os
import yaml
import shutil
import random
from collections import defaultdict
import struct
from typing import List
from paths import RANDO_ROOT_PATH


def is_derangement(l: List[int]) -> bool:
    for i, n in enumerate(l):
        if i == n:
            return False
    return True


def get_derangement(length: int, rng: random.Random) -> List[int]:
    """
    Generates a list of the range [0,length),
    shuffled such that no number is at its index
    """
    if length <= 1:
        raise ValueError("length needs to be at least 2")
    lst = list(range(length))
    rng.shuffle(lst)
    while not is_derangement(lst):
        rng.shuffle(lst)
    return lst


def music_rando(placement_file, modified_extract_path):
    with (RANDO_ROOT_PATH / "music.yaml").open() as f:
        musiclist = yaml.safe_load(f)

    NON_SHUFFLED_TYPES = [10, 11]
    TADTONES_FILE_NAME = "F63D5DB51DE748A3729628C659397A49"
    music = {}
    music_pool = defaultdict(list)
    # self.loop_patch_list = []

    if placement_file.options["music-rando"] == "None":
        for f in musiclist.keys():
            music[f] = f
    else:
        rng = random.Random(placement_file.music_rando_seed)
        for musicfile, musicdata in musiclist.items():
            music_type = musicdata["type"]
            if music_type == 2:  # Type 2 is currently shuffled with 1
                music_type = 1
            music_pool[music_type].append(musicfile)

        for music_type, tracks in music_pool.items():
            if music_type not in NON_SHUFFLED_TYPES and len(tracks) > 1:
                if placement_file.options["music-rando"] == "Shuffled (Limit Vanilla)":
                    derangement = get_derangement(len(tracks), rng)
                    for i in range(len(tracks)):
                        music[tracks[i]] = tracks[derangement[i]]
                else:
                    shuffled_tracks = tracks[:]
                    rng.shuffle(shuffled_tracks)
                    for orig_track, shuf_track in zip(tracks, shuffled_tracks):
                        # if orig_track == TADTONES_FILE_NAME:
                        #     print("Tadtones replacing: " + shuf_track)
                        music[orig_track] = shuf_track
            else:  # this should not be shuffled
                for track in tracks:
                    music[track] = track
                # Force vanilla tadtones music to prevent softlock.
                # Tadtones music can still be randomized to other locations.
                music[TADTONES_FILE_NAME] = TADTONES_FILE_NAME

    # patch WZSound.brsar for filename and length requirements
    with (modified_extract_path / "DATA" / "files" / "Sound" / "WZSound.brsar").open(
        "r+b"
    ) as brsar:
        for original_track, new_track in music.items():
            # patch filename
            filenameLoc = musiclist[original_track]["filenameLoc"]
            brsar.seek(filenameLoc)
            brsar.write(new_track.encode("ASCII"))
            # patch track length
            if (
                placement_file.options["cutoff-gameover-music"]
                and original_track == "C47D3DF4C435739443D195F7265A7D57"
            ):
                track_len = musiclist[original_track]["audiolen"]
            else:
                if placement_file.options["allow-custom-music"]:
                    track_len = 0x7FFFFFFF  # 2GB
                else:
                    track_len = musiclist[new_track]["audiolen"]
            audiolenLoc = musiclist[original_track]["audiolenLoc"]
            brsar.seek(audiolenLoc)
            brsar.write(struct.pack(">I", track_len))
