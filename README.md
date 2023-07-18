# The Legend of Zelda - Skyward Sword Randomizer

This is a randomizer for the game _The Legend of Zelda: Skyward Sword_.

You can access most resources on the [Skyward Sword Randomizer website](https://ssrando.com); you can also come discuss or ask for help on the [Skyward Sword Randomizer & Modding Discord](https://discord.gg/evpNKkaaw6).

## Requirements
- A computer (to run the randomizer)
- A clean NTSC-U 1.00 ISO (MD5 hash: e7c39bb46cf938a5a030a01a677ef7d1)
- The randomizer (see below for installation)

- Something to run the randomized game:
    + An emulator (Dolphin is the most widely used one)
    + A homebrewed Wii that can launch games from an external medium, such as a SD card, a USB drive or an external hard drive. Visit [https://wii.guide](https://wii.guide) for homebrewing information

## Installation

You can either run from a compiled binary (recommended for Windows, required for tournaments) or directly from source ([jump here](#Installing-from-source), required for Linux). Currently, only the command-line interface works for OSX; it needs an installation from source.


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
If you really wish to play on hero mode, there are options to enable its features.
When these options selected, even if they don't appear as such in the menu, all files will be set to hero mode.

If you didn't follow these rules, your progress cannot be restored; delete the save from the Wii menu / Dolphin's toolbar and correct the settings to play the game.

### For Dolphin
1. Just open the generated `SOUE01.wbfs` in Dolphin

### For console
1. Move the generated `SOUE01.wbfs` to your external medium in this folder (the folder name may change depending on the game loader you are using):

    `/wbfs/The Legend of Zelda Skyward Sword [SOUE01]/`
2. Launch the USB loader, you should see the game as "The Legend of Zelda Skyward Sword"


## Installing from source

You will need Python (at least version 3.9) and pip (which should come with Python)

1. In a terminal, navigate to the directory where you want to install the randomizer (using `cd`)
2. Clone the repository with git and enter the directory

        git clone https://github.com/ssrando/ssrando
        cd ssrando

3. Choose the branch you want to run (`main` is the most up-to-date), or the version you want to run (`v1.x.x` for stable releases, `async-[month]-[yy]` for async races; you can check the releases in Github):

        git checkout [BRANCH OR VERSION]
    Replace `[BRANCH OR VERSION]` with the desired branch or version in the command
4. Install `poetry`, which is used to install the dependencies
        pip install poetry
    If your system uses old versions of Python, you may need to replace `pip` with `python3 -mpip`
    
5. Install the dependencies:

        poetry install

6. [Run](#Running-the-randomizer) the randomizer:

        poetry run python randoscript.py

## The command-line interface

If you installed from source, you can run the randomizer without using the GUI by using `--noui` when running `randoscript.py`.

You will need to select the settings using the command-line options, use `--help` to list them.

For now, you have to run the GUI once so the ISO can be extracted (ask for a workaround in Discord if needed)

You can also pass options when launching the GUI, they will be pre-entered (this can be useful when creating a script to run the randomizer)

## Model Customization
After running the randomizer once, a folder `oarc` will be created, which contains Link's model (`Alink.arc`) and the Loftwing's model (`Bird_Link.arc`) as well as several other arc files. All arcs can also be found in the `actual-extract` folder. These folders can be used to get unmodified models from your clean ISO and can be used for creating custom models.

To modify them, you need one or more external programs to edit, save, and convert the existing game models (more information can be found in the [Skyward Sword Randomizer & Modding Discord](https://discord.gg/evpNKkaaw6)).

Modified Link and Loftwing models should be placed in a model pack using `models/[model pack name]/Player` and `models/[model pack name]/Loftwing` folders respectively. Other modifed arcs should be placed in the `arc-replacements` folder (or alternatively in `models/[model pack name]/Player/AdditionalArcs` for easier model pack creation).

Modified arcs **must** have the same same name as the original model they replace.

## Tests
Tests need a source installation and an extracted ISO:

    python -mpytest test
If your system uses old versions of Python, you may need to replace `python` with `python3`

## Contributing
Contributions are always welcome! Discussion happens on Discord.

We are using `black` to format code; you can run `black .` to format all files.

To install developing dependencies (including `black`):

    poetry install --only=dev
If your system uses old versions of Python, you may need to replace `pip` with `python3 -mpip`

### Executable
To build the executable, you need `PyInstaller` installed:

    poetry install --only=build

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
