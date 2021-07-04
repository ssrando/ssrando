import os
import yaml
import shutil
import random
from paths import RANDO_ROOT_PATH


def music_rando(self):
    with (RANDO_ROOT_PATH / "music.yaml").open() as f:
        self.musiclist = yaml.safe_load(f)

    if os.path.exists(RANDO_ROOT_PATH / "music") == False:
        os.mkdir(RANDO_ROOT_PATH / "music")

    for m in self.musiclist.keys():
        if os.path.exists(RANDO_ROOT_PATH / "music" / m) == False:
            shutil.copyfile(
                (
                    self.rando.actual_extract_path
                    / "DATA"
                    / "files"
                    / "Sound"
                    / "wzs"
                    / m
                ),
                (RANDO_ROOT_PATH / "music" / m),
            )

    try:
        shutil.rmtree(
            self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "wzs"
        )
    except:
        pass
    os.mkdir(self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "wzs")

    NON_SHUFFLED_TYPES = ["type10", "type11"]
    self.music = {}
    self.shuffled_music = {}
    i = 1
    while i <= 13:
        self.music["type" + str(i)] = []
        i += 1

    for musicfile, musicdata in self.musiclist.items():
        musictype = "type" + str(musicdata["type"])
        self.music[musictype].append(musicfile)

    self.music["type1"] += self.music["type2"]
    del self.music["type2"]

    rng = random.Random()
    rng.seed(self.rando.options["seed"])

    for type, music in self.music.items():
        if type in NON_SHUFFLED_TYPES:
            continue
        shuffled_music = music.copy()
        rng.shuffle(shuffled_music)
        self.shuffled_music[type] = shuffled_music

    for music_list, shuffled_music_list in zip(
        self.music.values(), self.shuffled_music.values()
    ):
        for m, sm in zip(music_list, shuffled_music_list):
            shutil.copyfile(
                (RANDO_ROOT_PATH / "music" / sm),
                (
                    self.rando.modified_extract_path
                    / "DATA"
                    / "files"
                    / "Sound"
                    / "wzs"
                    / m
                ),
            )
