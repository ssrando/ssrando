from collections import OrderedDict
from io import BytesIO
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from ssrando import Randomizer
from urllib import request

import subprocess
import zipfile


class RandoGUI:
    def __init__(self, root=None):

        self.wit_url = "https://wit.wiimm.de/download/wit-v3.03a-r8245-cygwin.zip"
        self.wit_folder = "wit-v3.03a-r8245-cygwin"

        frame = ttk.Frame(root, padding="3 3 12 12", width=800, height=600)
        frame.grid(column=0, row=0, sticky=(N, W, E, S))

        ttk.Button(frame, text="Randomize", command=self.randomize).grid(column=2, row=2, sticky=(W, E))
        ttk.Label(frame, text="Clean SS NTSC-U 1.0 ISO").grid(column=0, row=0)
        self.iso_location = ttk.Entry(frame)
        self.iso_location.grid(column=1, row=0, columnspan=10)
        ttk.Button(frame, text="Browse", command=self.set_iso_location).grid(column=11, row=0)

    def randomize(self):
        Thread(target=self.offthread_randomize).start()

    def set_iso_location(self):
        iso_path = filedialog.askopenfile()
        if iso_path is not None:
            self.iso_location.delete(0, 'end')
            self.iso_location.insert(0, iso_path.name)

    def offthread_randomize(self):
        if not (Path(".") / self.wit_folder).is_dir():
            # fetch and unzip wit dependency
            with zipfile.ZipFile(BytesIO(request.urlopen(self.wit_url).read())) as wit_zip:
                wit_zip.extractall(Path(".") / self.wit_folder)

        if not (Path(".") / "actual-extract").is_dir():
            subprocess.run([(Path(".") / self.wit_folder / "bin" / "wit"), "-P", "extract", "disc.iso", "actual-extract"])
        if not (Path(".") / "modified-extract").is_dir():
            subprocess.run(["xcopy", "/E", "/I", "actual-extract", "modified-extract"])
        rando = Randomizer(OrderedDict([('dry-run', False), ('randomize-tablets', False), ('closed-thunderhead', True), ('swordless', False), ('invisible-sword', False), ('empty-unrequired-dungeons', True), ('banned-types', ''), ('seed', -1)]))
        print(rando.seed)
        rando.randomize()
        iso_name = "SS Randomizer " + str(rando.seed) + ".iso"
        subprocess.run([(Path(".") / self.wit_folder / "bin" / "wit").name, "-P", "copy", "modified-extract", iso_name])


window_root = Tk()
window_root.title("Skyward Sword Randomizer")

gui = RandoGUI(window_root)

# root.mainloop()
while True:
    window_root.update()
    window_root.update_idletasks()
    print(Path(gui.iso_location.get()).name)