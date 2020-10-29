from tkinter import *;


class RandoGUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.running = True


root = Tk()
root.title("Skyward Sword Randomizer")
rando = RandoGUI(root)
while rando.running:
    root.update_idletasks()
    root.update()