# The Legend of Zelda - Skyward Sword Randomizer

This is a randomizer for the game _The Legend of Zelda: Skyward Sword_.

You can access most resources on the [Skyward Sword Randomizer website](https://ssrando.com); you can also come discuss or ask for help on the [Skyward Sword Randomizer Discord](https://discord.gg/evpNKkaaw6).

## Requirements
- A computer (to run the randomizer)
- A clean NTSC-U 1.00 ISO (MD5 hash: e7c39bb46cf938a5a030a01a677ef7d1)
- The randomizer (see below for installation)

- Something to run the randomized game:
    + An emulator (Dolphin is the most widely used one)
    + A homebrewed Wii that can launch games from an external medium, such as a SD card, a USB drive or an external hard drive. Visit [https://wii.guide](https://wii.guide) for homebrewing information

## Installation

You can either run from a compiled binary (recommended for Windows, required for tournaments) or directly from source ([jump here](#Installing-from-source), recommended for Linux). Currently, only the command-line interface works for OSX; it needs an installation from source.


## Installing from a compiled binary
1. Choose the version of the randomizer on the [website](https://ssrando.com) and download it
2. Extract the ZIP file where you want to install the randomizer
    + if you already have another version installed, you can use the same folder for multiple instances and rename the executables to avoid conflicts
3. [Run](#Running-the-randomizer) the extracted executable (`ssrando.exe`)


## Running the randomizer

1. As indicated, select a clean NTSC-U 1.00 ISO. The randomizer will then check its integrity, which may take a few minutes
2. Choose the folder where the randomized file will be created; by default, it is the randomizer installation folder
3. Customize the settings to your liking. You can use permalinks to store and share selected settings
4. Hit randomize; this may also take a few minutes


## Playing the randomized game

The randomized game will only work if the game language is set to **English**, other languages **will not work**.

Do **not** use the game's hero-mode files, it **will not work**.  
If you only want it to skip cutscenes, they are made skippable even in normal mode.  
If you really wish to play on hero mode, select the "hero mode" option in the randomizer.
When this option is selected, even if they don't appear as such in the menu, all files will be set to hero mode.

If you didn't follow these rules, your progress cannot be restored; delete the save from the Wii menu / Dolphin's toolbar and correct the settings to play the game.

### For Dolphin
1. Just open the generated `SOUE01.wbfs` in Dolphin

### For console
1. Move the generated `SOUE01.wbfs` to your external medium in this folder (the folder name may change depending on the game loader you are using):

    `/wbfs/The Legend of Zelda Skyward Sword [SOUE01]/`
2. Launch the USB loader, you should see the game as "The Legend of Zelda Skyward Sword"


## Installing from source

You will need Python (version 3.8 for Windows) and pip (which should come with Python)

1. In a terminal, navigate to the directory where you want to install the randomizer (using `cd`)
2. Clone the repository with git and enter the directory

        git clone https://github.com/ssrando/ssrando
        cd ssrando

3. Choose the branch you want to run (`master` is the most up-to-date), or the version you want to run (`v1.x.x` for stable releases, `async-[month]-[yy]` for async races; you can check the releases in Github):

        git checkout [BRANCH OR VERSION]
    Replace `[BRANCH OR VERSION]` with the desired branch or version in the command
4. Install the dependencies:

        pip install -r requirements.txt
    If your system uses old versions of Python, you may need to replace `pip` with `python3 -mpip`

5. [Run](#Running-the-randomizer) the randomizer:

        python randoscript.py
    If your system uses old versions of Python, you may need to replace `python` with `python3`

## The command-line interface

If you installed from source, you can run the randomizer without using the GUI by using `--noui` when running `randoscript.py`.

You will need to select the settings using the command-line options, use `--help` to list them.

For now, you have to run the GUI once so the ISO can be extracted (ask for a workaround in Discord if needed)

You can also pass options when launching the GUI, they will be pre-entered (this can be useful when creating a script to run the randomizer)

## Model Customization
After running the randomizer once, a folder `oarc` will be created, which contains Link's model (Alink.arc) and his bird's (Bird_Link.arc)

To modify them, you need an external program. Then save the modified arcs (the name **must** stay the same) in the `arc-replacements` folder of the randomizer installation directory.

## Tests
Tests need a source installation and an extracted ISO:

    python -mpytest test
If your system uses old versions of Python, you may need to replace `python` with `python3`

## Contributing
Contributions are always welcome! Discussion happens on Discord.

We are using `black` to format code; you can run `black .` to format all files.

To install developing dependencies (including `black`):

    pip install -r requirements_dev.txt
If your system uses old versions of Python, you may need to replace `pip` with `python3 -mpip`

### Executable
To build the executable, you need `PyInstaller` installed:

    pip install -r requirements_build.txt

Then, build the executable using

    pyinstaller ssrando.spec

### Contributors
- lepelog: Main developer
- Peppernicus2000: Logic, fixes
- Azer67: Logic
- MrCheeze: Reverse engineering file formats
- LagoLunatic: For implementing the logic for [TWWR](https://github.com/LagoLunatic/wwrando), which is also used here
- DGod63: title screen logo
- cjs07: GUI
