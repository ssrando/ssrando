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
    # self.loop_patch_list = []
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
            trackname = trackinfo["name"]
            if trackinfo["type"] == 2:
                tracktype = "type1"
            else:
                tracktype = "type" + str(trackinfo["type"])

            if tracktype in NON_SHUFFLED_TYPES:
                self.music[track] = track
            else:
                if self.rando.options["limit-vanilla-music"] == True:
                    self.music[track] = rng.choice(
                        [
                            t
                            for t in self.music_pool[tracktype]
                            if self.musiclist[t]["name"] != trackname
                        ]
                    )
                else:
                    self.music[track] = rng.choice(self.music_pool[tracktype])
                if self.rando.options["music-rando"] == "Shuffled":
                    self.music_pool[tracktype].remove(self.music[track])

    for m, sm in self.music.items():
        shutil.copyfile(
            (self.rando.actual_extract_path / "DATA" / "files" / "Sound" / "wzs" / sm),
            (self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "wzs" / m),
        )

    # patch WZSound.brsar for length requirements
    with (
        self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "WZSound.brsar"
    ).open("r+b") as brsar:
        for original_track, new_track in self.music.items():
            new_track_len = int.to_bytes(
                int(self.musiclist[new_track]["audiolen"], base=16), 0x4, "big"
            )
            tracklenLoc = self.musiclist[original_track]["audiolenLoc"]
            brsar.seek(tracklenLoc)
            brsar.write(new_track_len)

    """ for track in self.loop_patch_list:
        with open(self.rando.modified_extract_path / "DATA" / "files" / "Sound" / "wzs" / track, 'r+b') as mfile:
            mfile.seek(0x61) # Loop flag offset
            mfile.write(0x01.to_bytes(1, "big")) """
