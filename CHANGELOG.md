# Changelog

## Dev
### Options
- Added option to randomize music (by Battlecats59)
- Added option to force swords at the end of dungeons (by YourAverageLink)
- Added option to visually swap Skyloft and hero's clothes
### Changes
- Various name changes (by NULL and cjs07)
- Added playername and hash to textboxes after Demise (by Battlecats59)
- CLI improvements
- Hint changes (by cjs07)
  - Added 2 new always hinted locations:
    - LMF - Boss Key Chest
    - FS - Chest after Bombable Wall
  - Added 11 new sometimes hinted locations:
    - SV - Chest behind Three Eyes
    - SSH - Boss Key Chest
    - SSH - Tentalus Heart Container
    - SSH - Bow
    - Thunderhead - Isle of Songs - Din's Power
    - Sealed Grounds - Zelda's Blessing
    - Sand Sea - Skipper's Retreat - Chest in Shack
    - Volcano Summit - Item behind Digging
    - Faron Woods - Slingshot
    - Sky - Beedle's Crystals
    - Sealed Grounds - Gorko's Goddess Wall Reward
  - The Sea Chart can now be hinted when Sandship is a required dungeon
### Bugfixes
- Added some tricks that were in the logic files but not in options (by NULL)
- Fix bug with arc-replacements causing an error if the arc doesn't exist in ObjectPack, it's ignored now
- Fix Sandship Timeshift stone not being unset when leaving the dungeon in entrance rando
- Fix a bug in trials where you could be unable to get the item with glitches

## 1.1.0
### Options
### Changes
- Redesigned GUI
- Added Boko Base Checks to Volcano Summit
- Added hint for Stone of Trial to Impa in the past
- Added dialogue option to Rupin to make him buy different treasures
### Bugfixes
- Fix Softlock in FS, this removes the mogma cutscene after the double magmanos fight
- Fix a bug with trial rando hinting to the wrong trial
- Fix some buggy logic in Fire Sanctuary

## 1.0.7
### Options
- Keysanity
- Choose Required Sword for Gate of Time
- Add Way of the Hero and Barren Region Hints
- Glitched Logic
- Logic Tricks for both BiTless and Glitched Logic
- Added option to make BiT not crash in areas where it normally would
- Added option to randomize which trial corresponds to which trial gate
- Added option to start with Lanayru Mining Facility being already raised
- Added hints with customizable amounts for various hint types
### Changes
- Split up Skyloft in different Areas for logic
### Bugfixes
- Fix a bunch of typos
- Fix potential softlocks when playing Clean Cut or Thrill Digger without the necessary item
- Fix softlocking in Koloktos' Boss Room without Goddess Sword
- Fix textwrapping for hints and Beedle's shop

## 1.0.6
### Options
- Added option to randomize beetles shop
- Added No Logic Option
### Changes
- Optionally added seed to permalink
- Make faron BiT easy by setting all relevant flags in link's room
- Bring back isle of songs crest and remove chests
### Bugfixes
- Fixed digging spots always giving key pieces
- Fixed bokoblin in AC not giving any item if it was a random treasure

## 1.0.5
### Options
- Added option to randomize dungeon entrances
- Added option to add rupoors into the junk item pool
- Added bulk and json options (for mass testing seeds)
### Changes
- Verify ISO checksum
- Item after LMF is given before exiting out of the back
- Treasure and Rupee dowsing are now obtainable after getting the Goddess Whitesword
- Shorten timeshift stone cutscenes
- Make it possible to not get pumpkin soup when doing lumpy pumpkin quest with spiral charge

## 1.0.4
### Options
- Add option to not generate a spoiler log
- Add option to start with Adventure pouch
- Changed Batreaux type to a specific max count
- Add option to skip imp 2
- Add permalink to options that can be specified on the command line
### Changes
- Songs give a hint if the item their trial has is potentially useful
- Eldin Entrance statue is always checked, prevents softlocks if BiTsaving out of an area without checking a statue first
### Bugfixes
- Fix Bomb Bag having a wrong text sometimes
- Fix potential softlock in the Skyview Beetle room
- Fix potential softlock when getting Spiral Charge in the Lumpy Pumpkin

## 1.0.3
### Options
- Change tablet rando option to select amount of tablets to randomize
- More types and Area types
### Changes
- Removed more text triggers and cutscenes
- Show a hash on the file select screen to make it easier to verify that everyone has the same seed
- Make Fun Fun island quest be startable immediately
- Always skip opening the inventory screen after treasures/bug/crystals
### Bugfixes
- Fix double increasing pouch counter
- Fixed a shared storyflag, causing levias to sometimes not give an item
- Fixed layers in Volcano Summit
- Fix some NPCs holding items in their hands

## 1.0.2
### Options
- add hero mode option
- add scrapper quests/peatrice types
- add permalink to share settings more easily
### Changes
- GUI only asks for ISO once
- progress bars for WIT and copy commands in GUI
- remove even more unnecessary text triggers
- all skippable cutscenes can always be skipped
- add logic for normal mode
- make pouch and pouch expansion progressive
- added spiral charge as an obtainable item
- levias item is randomized after calming him
- increase max loftwing speed from 80 to 350
- ancient sea chart now gives ship dowsing instead of immediately opening sandship
### Bugfixes
- fix required dungeon text not being readable with 4+ dungeons
- fix being able to buy a pouch upgrade from beetle before having the adventure pouch
- fix CS in Fire Sanctuary setting Sealed Grounds intro storyflag, causing sceneflags to not be set
- fix various doubled NPCs
- fix crash when recieving a sword upgrade in ghirahims room by delaying the visual sword upgrade until the next reload

## 1.0.2-rc1
### Options
- checks can be filtered by types
- add option to make sure unrequired dungeons are useless
- add option to skip skykeep
- make number of required dungeons dynamic
### Gameplay
- remove various unnecessary text triggers
### Misc
- gui
- custom title screen logo
### Bugfixes
- fix soil items being indefinetly reobtainable
- fix a softlock in fire sanctuary, related to the mogma near the second key

## 1.0.0
- Initial Randomization of Items
- Option to start with open/closed thunderhead
- Option to start with light pillars open/closed
- Option to start with/without a sword
- Option to specify a seed
