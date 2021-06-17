This is still under heavy development, be careful to use it!  
**IMPORTANT NOTES**  
This only works if the game language is set to ENGLISH, other languages will NOT WORK and will break  
Do NOT use hero mode files, instead select the "hero mode" option in the randomizer. Some hero mode files break the randomizer!  
There is also the [Skyward Sword Randomizer Discord](https://discord.gg/evpNKkaaw6)

## Running the compiled binary (Windows)(recommended)
1. For stable releases, grab the compiled program from the [github release section](https://github.com/lepelog/sslib/releases), for the newest, although potentially untested build get them from [github actions](https://nightly.link/lepelog/sslib/workflows/build.yaml/master).
2. Download the zipfile, extract it somewhere (if you already have an older version installed, install it over and replace the existing files)
3. run `ssrando.exe`
4. Select a clean NTSC-U 1.00 ISO
5. Customize the settings however you want
6. hit randomize, it might take a while

### For dolphin
Just open the generated `SOUE01.wbfs` in dolphin and enjoy!
### For console
1. Make sure to have homebrew and a USB loader installed (for example Configurable USB Loader)
2. copy the generated `SOUE01.wbfs` to your SD card in this folder: /wbfs/The Legend of Zelda Skyward Sword [SOUE01]/ and put the SD into your Wii
3. Power up your Wii, homebrew channel, configurable USB Loader, Profit
## Installing from source (for development)
1) Clone [https://github.com/lepelog/sslib](https://github.com/lepelog/sslib)
2) Install Python 3.8(!) (3.9 won't work on Windows) and pip (comes with most python installers)
3) Download and Install wit from [here](https://wit.wiimm.de/download.html) (there's a simple installer.exe for Windows, you will probably have to reboot your system)
4) Open a terminal of your choice and use the `cd` command to navigate to the directory where you have sslib saved
5)
On Linux:

    python3 -mpip install -r requirements.txt

On Windows:

    pip install -r requirements.txt

6) Take a clean E 1.00 ISO (make sure to verify the hashes in dolphin: crc="2b48d050" md5="e7c39bb46cf938a5a030a01a677ef7d1" sha1="9cf9a4a7ed2a6a4abb4582e3304af1327c160640") and put it somewere you can find it again(in the following steps it will be simply called disc.iso)
7)Start the GUI/Setup by writeing this into your terminal

On Linux:

    python3 randoscript.py

On Windows:

    py randoscript.py
Or:

    python randoscript.py

It will ask you to choose an iso and will extract it for you into the sslib directory (you should see 2 new folders in the directory afterwards).
The GUI will also Test your ISO version if you haven't checked yourself before and won't extract unless you have the right version.
After it is complete it should show up the GUI you can use to modify your game.
The randomized game will then show up in the folder you choose in the GUI.


#### MORE OPTIONS
To access more options you can start the GUI by starting the randoscript.py (see above).
If you don't want to use the GUI you can do `--noui`, otherwise this extra information is not important for you
To see all options, use `--help` or see options.yaml

#### Model Customization
After running the randomizer once, a folder `oarc` will be created, which has Link's model (Alink.arc) and his bird (Bird_Link.arc)

To modify them, you need an external program. To include make sure the models get actually replaced when running the randomizer, save the modified arcs (the name **has** to stay the same) in the `arc-replacements` folder, which needs to be located next to the randomizer executable

### Tests
`python3 -mpytest test`  
Make sure to have the extracted game prepared as stated in Installing, otherwise they won't work

### Contributing
Contributions are always welcome!  
To make sure we don't have to fight about formatting, make sure to install `black`  
On Linux:

    python3 -mpip install -r requirements_dev.txt

On Windows:

    pip install -r requirements_dev.txt

Then run `black .` and you are good to go!

### Executable
To build the executable, you need PyInstaller installed:

    python3 -mpip install pyinstaller

Then, build the executable using

    pyinstaller ssrando.spec

### Changes
#### Storyflag
900: Beat Ancient Cistern
901: Beat Fire Sanctuary
11 & 13: Imp2 Requirements reached (should be set at once)
902: Beat Required dungeon 1
903: Beat Required dungeon 2

904: Progressive Mitts1 (Digging Mitts)
905: Progressive Mitts2 (Mogma Mitts)

906: Progressive Sword1 (Practice Sword)
907: Progressive Sword2 (Goddess Sword)
908: Progressive Sword3 (Goddess Long Sword)
909: Progressive Sword4 (Goddess White Sword)
910: Progressive Sword5 (Master Sword)
911: Progressive Sword6 (True Master Sword)

912: Progressive Beetle1
913: Progressive Beetle2 (Hook Beetle)

914: Change Temple of Time Layer, storyflag 9 is associated with harp

915: Medium Wallet
916: Big Wallet
917: Giant Wallet
918: Tycoon Wallet

New Trial Completed Storyflags:
919: Faron
920: Eldin
921: Lanayru
922: Skyloft

923: Obtained Item from Fledge at start
924: Obtained Item from Cawlin
925: Obtained Item from Strich

926: Required Dungeon 3  
927: Required Dungeon 4  
928: Required Dungeon 5  
929: Required Dungeon 6  

931: Adventure Pouch 932 Pouch Expansion

933: Defeat Tentalus
934: Obtained Item from Levias

935: Exit out of back of LMF for first time
936: Obtained Item at end of LMF

937: bought Beetles first 100R item
938: bought Beetles second 100R item
939: bought Beetles third 100R item
940: bought Beetles Bug Net item
941: bought Beetles Bug Medal item

#### Sceneflags
Ancient Cistern:
- 85, after recieving item from flame CS
Sandship:
- 87, after recieving item from flame CS

### Shoutouts
- Peppernicus2000: Logic, fixes
- Azer67: Logic
- MrCheeze: Reverse engineering file formats
- LagoLunatic: For implementing the logic for [TWWR](https://github.com/LagoLunatic/wwrando), which is also used here
- DGod63: title screen logo
- cjs07: GUI
