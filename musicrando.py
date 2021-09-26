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


def music_rando(self):
    with (RANDO_ROOT_PATH / "music.yaml").open() as f:
        self.musiclist = yaml.safe_load(f)

    NON_SHUFFLED_TYPES = [10, 11]
    self.music = {}
    self.music_pool = defaultdict(list)
    # self.loop_patch_list = []
    rng = random.Random()
    rng.seed(self.rando.options["seed"])

    if self.rando.options["music-rando"] == "None":
        for f in self.musiclist.keys():
            self.music[f] = f
    else:
        for musicfile, musicdata in self.musiclist.items():
            music_type = musicdata["type"]
            if music_type == 2:  # Type 2 is currently shuffled with 1
                music_type = 1
            self.music_pool[music_type].append(musicfile)

        for music_type, tracks in self.music_pool.items():
            if music_type not in NON_SHUFFLED_TYPES and len(tracks) > 1:
                if self.rando.options["music-rando"] == "Shuffled (Limit Vanilla)":
                    derangement = get_derangement(len(tracks), rng)
                    for i in range(len(tracks)):
                        self.music[tracks[i]] = tracks[derangement[i]]
                else:
                    shuffled_tracks = tracks[:]
                    rng.shuffle(shuffled_tracks)
                    for orig_track, shuf_track in zip(tracks, shuffled_tracks):
                        self.music[orig_track] = shuf_track
            else:  # this should not be shuffled
                for track in tracks:
                    self.music[track] = track

    # patch WZSound.brsar for filename and length requirements
    with (
        self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "WZSound.brsar"
    ).open("r+b") as brsar:
        for original_track, new_track in self.music.items():
            # patch filename
            filenameLoc = self.musiclist[original_track]["filenameLoc"]
            brsar.seek(filenameLoc)
            brsar.write(new_track.encode("ASCII"))
            # patch track length
            if (
                self.rando.options["cutoff-gameover-music"]
                and original_track == "C47D3DF4C435739443D195F7265A7D57"
            ):
                audiolenLoc = self.musiclist[original_track]["audiolenLoc"]
                track_len_bytes = struct.pack(
                    ">I", self.musiclist[original_track]["audiolen"]
                )
                brsar.seek(audiolenLoc)
                brsar.write(track_len_bytes)
            else:
                audiolenLoc = self.musiclist[original_track]["audiolenLoc"]
                track_len_bytes = struct.pack(
                    ">I", self.musiclist[new_track]["audiolen"]
                )
                brsar.seek(audiolenLoc)
                brsar.write(track_len_bytes)
