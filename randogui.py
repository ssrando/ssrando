from collections import OrderedDict
from io import BytesIO
from pathlib import Path
from tkinter import *
from tkinter import ttk
from threading import Thread
from ssrando import Randomizer
from urllib import request

import subprocess
import zipfile


wit_url = "https://wit.wiimm.de/download/wit-v3.03a-r8245-cygwin.zip"
wit_folder = "wit-v3.03a-r8245-cygwin"


def randomize():
    Thread(target=offthread_randomize).start()


def offthread_randomize():
    if not (Path(".") / wit_folder).is_dir():
        # fetch and unzip wit dependency
        with zipfile.ZipFile(BytesIO(request.urlopen(wit_url).read())) as wit_zip:
            wit_zip.extractall(Path(".") / wit_folder)

    if not (Path(".") / "actual-extract").is_dir():
        subprocess.run([(Path(".") / wit_folder / "bin" / "wit").name, "-P", "extract", "disc.iso", "actual-extract"])
    if not (Path(".") / "modified-extract").is_dir():
        subprocess.run(["xcopy", "/E", "/I", "actual-extract", "modified-extract"])
    rando = Randomizer(OrderedDict([('dry-run', False), ('randomize-tablets', False), ('closed-thunderhead', True), ('swordless', False), ('invisible-sword', False), ('empty-unrequired-dungeons', True), ('banned-types', ''), ('seed', -1)]))
    print(rando.seed)
    rando.randomize()
    iso_name = "SS Randomizer " + str(rando.seed) + ".iso"
    subprocess.run([(Path(".") / wit_folder / "bin" / "wit").name, "-P", "copy", "modified-extract", iso_name])


root = Tk()
root.title("Skyward Sword Randomizer")

frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))

ttk.Button(frame, text="Randomize", command=randomize).grid(column=2, row=2, sticky=(W, E))

# root.mainloop()
while True:
    root.update()
    root.update_idletasks()
