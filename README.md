This is still under heavy development, be careful to use it!

## Running the compiled binary (Windows)(recommended)
1. For stable releases, grab the compiled program from the [github release section](https://github.com/lepelog/sslib/releases), for the newest, although potentially untested build get them from [appveyor](https://ci.appveyor.com/project/lepelog/sslib).
2. Download the zipfile, extract it somewhere (if you already have an older version installed, install it over and replace the existing files)
3. Take a clean E 1.00 ISO (make sure to verify the hashes in dolphin: crc="2b48d050" md5="e7c39bb46cf938a5a030a01a677ef7d1" sha1="9cf9a4a7ed2a6a4abb4582e3304af1327c160640") and put it in the sslib directory as disc.iso (make sure it isn't called disc.iso.iso)
## Installing from source
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

It will ask you to choose a iso and will extract it for you into the sslib directory (you should see 2 new foulders in the directory afterwards).
The GUI will also Test your ISO version if you haven't checked yourself before and wont extract unless you have the right version.
After it is complete it should show up the GUI you can use to modify your game.
The ranodmized game will then show up in the foulder you choose in the GUI.


#### MORE OPTIONS
To access more options you can start the GUI by starting the randoscript.py (see obove).
I you don't want to use the GUI you can do `--noui`, otherwise this extra information is not important for you
If you write `--noui` it will read extra instrucions you send with it like this:

To start with all light pillars closed and needing to find the tablets to unlock them, use `--randomize-tablets`

To start with the thunderhead closed, use `--closed-thunderhead`. It is automatically opened after obtaining Ballad of the Goddess

To start without a sword, use `--swordless`. Otherwise, you start with the goddess sword

To only generate a spoiler log, use the `--dry-run` option as a command line argument

There are more optons to call, check out the options.py to see them all.


#### FOR EMULATOR
11a) Open disc.wbfs in Dolphin
12a) Profit
#### FOR CONSOLE
10b) The exact steps may differ from what i write down, but this worked for me using Configurable USB Loader, loading from a SD card:

    wit -P copy -z modified-extract SOUE01.wbfs

11b) Take the 2! files (SOUE01.wbfs & SOUE01.wbf1), copy them to your SD card in this folder: /wbfs/The Legend of Zelda Skyward Sword [SOUE01]/ and put the SD into your Wii
12b) Power up your Wii, HBC, CFG USB Loader, Profit

### Tests
`python3 -mpytest test`  
Make sure to have the extracted game prepared as stated in Installing, otherwise they won't work

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

914: Beat LMF (more precisely, watch harp CS), storyflag 9 is associated with harp

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

### Shoutouts
- Peppernicus2000: Logic, fixes
- Azer67: Logic
- MrCheeze: Reverse engineering file formats
- LagoLunatic: For implementing the logic for [TWWR](https://github.com/LagoLunatic/wwrando), which is also used here
- DGod63: title screen logo
- cjs07: GUI
