from collections import OrderedDict
from pathlib import Path
from tkinter import *
from tkinter import ttk
from threading import Thread
from ssrando import Randomizer

import subprocess
import os


def randomize():
    Thread(target=offthread_randomize).start()


def offthread_randomize():
    if not (Path(".").parent / "actual-extract").is_dir():
        subprocess.run(["wit", "-P", "extract", "disc.iso", "actual-extract"])
    if not (Path(".").parent / "modified-extract").is_dir():
        subprocess.run(["xcopy", "/E", "/I", "actual-extract", "modified-extract"])
    rando = Randomizer(OrderedDict([('dry-run', False), ('randomize-tablets', True), ('closed-thunderhead', False), ('swordless', False), ('invisible-sword', False), ('empty-unrequired-dungeons', True), ('banned-types', ''), ('seed', -1)]))
    print(rando.seed)
    rando.randomize()
    subprocess.run(["wit", "-P", "copy", "modified-extract", "rando.iso"])


root = Tk()
root.title("Skyward Sword Randomizer")

frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))

ttk.Button(frame, text="Randomize", command=randomize).grid(column=2, row=2, sticky=(W, E))

# root.mainloop()
while True:
    root.update()
    root.update_idletasks()
