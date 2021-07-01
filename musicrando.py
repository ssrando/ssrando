import os
import shutil
import random
from paths import RANDO_ROOT_PATH


def music_rando(self):
    music_list = []

    for d in os.listdir(
        RANDO_ROOT_PATH / "modified-extract" / "DATA" / "files" / "Sound" / "wzs"
    ):
        if not os.path.exists(RANDO_ROOT_PATH / "music" / d):
            shutil.copyfile(
                (
                    RANDO_ROOT_PATH
                    / "modified-extract"
                    / "DATA"
                    / "files"
                    / "Sound"
                    / "wzs"
                    / d
                ),
                (RANDO_ROOT_PATH / "music" / d),
            )

    try:
        shutil.rmtree(
            RANDO_ROOT_PATH / "modified-extract" / "DATA" / "files" / "Sound" / "wzs"
        )
    except:
        pass
    os.mkdir(RANDO_ROOT_PATH / "modified-extract" / "DATA" / "files" / "Sound" / "wzs")

    for f in os.listdir(RANDO_ROOT_PATH / "music"):
        music_list.append(f)
        music_list_2 = music_list.copy()

    rng = random.Random()
    rng.seed(self.rando.options["seed"])
    if self.rando.options["music-rando"] == True:
        rng.shuffle(music_list_2)

    for m, m2 in zip(music_list, music_list_2):
        shutil.copyfile(
            (RANDO_ROOT_PATH / "music" / m2),
            (
                RANDO_ROOT_PATH
                / "modified-extract"
                / "DATA"
                / "files"
                / "Sound"
                / "wzs"
                / m
            ),
        )
