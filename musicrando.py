import os
import yaml
import shutil
import random
from paths import RANDO_ROOT_PATH


def music_rando(self):
    with (RANDO_ROOT_PATH / "music.yaml").open() as f:
        self.musiclist = yaml.safe_load(f)

    try:
        shutil.rmtree(
            self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "wzs"
        )
    except:
        pass
    os.mkdir(self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "wzs")

    NON_SHUFFLED_TYPES = ["type10", "type11"]
    self.music = {}
    self.music_pool = {}
    rng = random.Random()
    rng.seed(self.rando.options["seed"])

    if self.rando.options["music-rando"] == "None":
        for f in self.musiclist.keys():
            self.music[f] = f
    else:
        i = 1
        while i <= 13:
            self.music_pool["type" + str(i)] = []
            i += 1
        for musicfile, musicdata in self.musiclist.items():
            musictype = "type" + str(musicdata["type"])
            self.music_pool[musictype].append(musicfile)

        self.music_pool["type1"] += self.music_pool["type2"]
        del self.music_pool["type2"]  # Type 2 is currently shuffled with 1

        for track, trackinfo in self.musiclist.items():
            tracklen = trackinfo["numsamples"]
            if trackinfo["type"] == 2:
                tracktype = "type1"
            else:
                tracktype = "type" + str(trackinfo["type"])

            if tracktype in NON_SHUFFLED_TYPES:
                self.music[track] = track
            elif tracktype in ["type1", "type4", "type5", "type6", "type7"]:
                print(
                    [
                        t
                        for t in self.music_pool[tracktype]
                        if self.musiclist[t]["numsamples"] <= tracklen
                    ]
                )
                if (
                    len(
                        [
                            t
                            for t in self.music_pool[tracktype]
                            if self.musiclist[t]["numsamples"] <= tracklen
                        ]
                    )
                    != 0
                ):
                    self.music[track] = rng.choice(
                        [
                            t
                            for t in self.music_pool[tracktype]
                            if self.musiclist[t]["numsamples"] <= tracklen
                        ]
                    )
                    if self.rando.options["music-rando"] == "Shuffled":
                        self.music_pool[tracktype].remove(self.music[track])
                else:
                    self.music[track] = rng.choice(self.music_pool[tracktype])
                    if self.rando.options["music-rando"] == "Shuffled":
                        self.music_pool[tracktype].remove(self.music[track])
            else:
                self.music[track] = rng.choice(self.music_pool[tracktype])
                if self.rando.options["music-rando"] == "Shuffled":
                    self.music_pool[tracktype].remove(self.music[track])

    print(self.music)
    for m, sm in self.music.items():
        shutil.copyfile(
            (self.rando.actual_extract_path / "DATA" / "files" / "Sound" / "wzs" / sm),
            (self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "wzs" / m),
        )
