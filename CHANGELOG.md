# Changelog

## Dev
### Options
- Added option to make sword reward place swords on heart containers rather than final checks (by YourAverageLink)
- Added option to randomize progression in Flooded Faron Woods (by CovenEsme)
  - Added Faron SotH check that is obtained when completing the Tadtones story quest
- Added chest dowsing functionality as an option (by YourAverageLink)
  - Uses the main quest dowsing slot (top slot), with a custom dowsing icon to indicate its usage for chests.
  - Vanilla: No change in dowsing functionality (rupee/treasure dowsing works on chests)
  - All Chests: Main quest dowsing will point to all chests. This means you cannot dowse for chests with rupee/treasure dowsing.
  - Progress Items: Main quest dowsing will point to chests that contain progress items
  - Currently does not work on goddess chests
- Added option to enable dowsing in dungeons (by YourAverageLink, but shoutouts to Zeldex)
- Added option to start with various items (by CovenEsme)
  - Includes: b-wheel items, pouches, quest items, songs, triforces, wallets, harp, water scale, earrings, mitts, life tree seedling, sea chart, spiral charge, stone of trials and Earth Temple key pieces.
- Added option to start with extra health (by CovenEsme)
- Added option to start with a random progress item (by CovenEsme)
### Changes
- Presets (by cjs07)
  - Presets allow users to save and load their favorite settings quickly from the main page of the randomizer
  - The randomizer is distributed with a set of default presets that cannot be changed
    - This list includes all 6 Season 2 Tournament modes and a new beginner friendly mode
  - Presets persist between versions and are forward compatible with new versions.
  - User preset data is sharable between users via the `presets.txt` file
  - Only options included in permalinks are saved, with the exception of the spoiler log toggle
- Added Water Dragon to the Great Tree (by CovenEsme)
- Added entrance and exit to and from Flooded Great Tree (by CovenEsme)
  - Entering Flooded Great Tree for the first time automatically starts the Tadtones story quest
  - New logical option for completing the Owlan's Crystals check
    - Added access to Flooded Faron as an alternative to needing bomb bag
- Machi is no longer rescued after beating Skyview
- Added custom dowsing images for new chest dowsing functionality (by YourAverageLink)
- Shooting the bell during pumpkin archery ends the minigame immediately
- Removed first time textboxes (by CovenEsme)
  - Removes rupee, heart, arrow, bomb, stamina fruit, silent realm tear and light fruit first time textboxes
- Removed bipping after getting slingshot, practice sword, the Potion Lady's Gift check and buying a shield (by CovenEsme)
### Bugfixes
- Fixed a bug that prevented tricks from being properly reloaded when the randomizer restarted multiple times without changes to the list
- Fixed a softlock caused by collecting the last 2 tears in a trial too close together
- Fixed a bug that would make sandship dowsing sometimes not be the top dowsing slot icon; it now has top priority
- Fixed light pillars not visually appearing when obtaining a tablet until a reload


## 1.3.2
### Changes
- Added Boss Key (BK) hints as a new hint type (by Muzugalium)
  - A BK hint will point to the precise location of the boss key of a required dungeon
- Added Stamina Potion for logical access to the end of Lanayru Mine and Lanayru Desert when Open LMF is set to Open (by CovenEsme)
### Bugfixes
- Fixed a crash when the arc-replacements folder was missing

## 1.3.1
### Changes
### Bugfixes
- Fix broken rare treasures (regression from previous version)
- Fix glitched logic (regression from previous version)

## 1.3.0
### Options
- Added bomb throw tricks for Beedle's Shop and Skyview (by NULL)
- Added option to randomize Triforces (by YourAverageLink)
  - Skip Skykeep has been split into two new triforce-related options: Triforce Required & Triforce Shuffle
  - When Triforce Required is enabled, the door to Hylia's Realm will only open if the player has the full Triforce; a confirmation textbox will appear in Hylia's Realm if the Triforce is complete.
    - Disabling Triforce Required acts similarly to the old Skip Sky Keep option; Sky Keep is an unrequired dungeon, and the horde door is always open.
    - Enabling Triforce Required and setting Triforce Shuffle to Vanilla acts like the old Skip Sky Keep OFF option.
  - Triforces act similarly to dungeon keys; they can be vanilla, restricted to Sky Keep, or anywhere.
    - When set to be placed anywhere, Sky Keep counts as an unrequired dungeon (empty if EUD is on).
  - To prevent kicking players out of Sky Keep for having a complete triforce, the game no longer forces you out of Sky Keep once you pick up the third Triforce.
  - The locations originally containing the Triforces are now randomizable checks.
- Added option to randomize objects such as tears and light fruits in trials (by cjs07)
### Changes
- Allow calling Fi underwater and without a sword
- Force english regardless of system language
- Write hints as json in json spoiler log
- Added option to fight multiple Demises at the end of the game
- Added option to allow custom music (by Battlecats59)
- Added even more cutscene skips, plus text patches for clarity (by YourAverageLink)
- New Hint System (by cjs07)
  - Removed all counter options for hints
  - Added Hint Distributions
    - Distributions can specufy the follwing *new* parameters
      - Maximum hints SotS dungeons
      - Maximum hinted barren dungeons
    - Distributions additionally can do the following
      - Add items to the hintable pool
      - Remove items from the hintable pool
      - Add locations to the always/sometimes pools
      - Remove locations from the always/sometimes pools
  - Reworked the interaction between Goddess Cubes and hints (by YourAverageLink)
    - Goddess chests are now linked to the region their associated cube is in for the purpose of hints
      - For example, a SotS hint that would have previously pointed to the goddess chest next to Isle of Songs would say Mogma Turf is SotS not Thunderhead
      - Additionally, an option has been added for whether or not cube SotS hints should look different (above example would say Eldin Volcano has a SotS cube)
      - Barren region calculation now factors in the goddess cubes in the region; a region with no progress items but a cube that unlocks a progress item is NOT barren
  - Added option to choose between specific locations for item hints or just the general region (by YourAverageLink)
    - Note that the default setting is DISABLED, however previous versions of the randomizer always used the precise locations for item hints (ENABLED).
    - When this option is disabled (which uses general regions), it will follow the same logic for Goddess Cubes 
      - Example: Sword in the Goddess Chest next to Isle of Songs -> Progressive Sword can be found in Mogma Turf
  - New hint types
    - Junk
    - Random
    - Sometimes
    - Goal (by YourAverageLink)
      - Goal hints are a new hint type that may be specified in a hint distribution. They act similar to SotS hints, but they specify a required dungeon boss locked by an item in that region
        - Example: Gust Bellows on Sparring Hall Chest with LMF as a required dungeon = Knight Academy is on the path to Moldarach
      - At the moment, goal hints are not compatible with the separate cube sots; they will be hinted like normal goal hints
      - Goal hints inherit the dungeon sots limit and use the same limit.
        - Example: If one goal hint is placed for a dungeon, the sots dungeon limit is 2, and goal hints are ordered before sots in the distribution, only up to one dungeon sots hint may be placed.
      - The fixed count specified in a hint distribution is multiplied by the required dungeon count. For example, a fixed of 1 and 3 required dungeons means 3 goal hints will be placed
      - The order of dungeon boss goals for goal hints is randomized once at the start, and then chosen in sequence to try to ensure one exists for each goal, if possible.
        - Example: If there are 3 required dungeons and 1 fixed goal hint (3 after multiplication by dungeon count, with 0 weight), there will be one goal hint for each of the three goals.
        - Exception: If there are no applicable goal-satisfying items left for a goal (can happen if already always/sometimes hinted, or with low-requirement dungeons like Skyview), the hint will be placed for the next goal in the chain (potentially causing a second goal hint for one of the goals)
    - Some of these hint types existed in prior versions, but users had no control over them
- Changed item hints, that point to a specific location, to use the same hint format as location hints
- Temple of Time is always in post LMF finish state
- Beating Skyview (even if it's in a different dungeon) rescues Machi
- Beating Ancient Cistern (even if it's in a different dungeon) removes the void in the Great Tree
- Added "Main Node" option to Open LMF (by YourAverageLink)
  - When enabled, the fire, water, and lightning nodes will start out as active, but the player still needs to activate the main node (which requires an explosive to reveal the timeshift stone) to raise LMF.
- Barren areas are now less likely to receive random location hints
- Change goddess walls to only require Harp and BotG, this removes the Skyview dependency from Gorko's Goddess Wall
- arc-replacements will now also replace arcs in stages
### Bugfixes
- always copy layer 0, this fixes various bugs, where changes from previous randomizations were not reverted
- fix gorko sometimes asking to draw bombs even when you don't have them
- Butterflies now spawn correctly near trial gates

## 1.2.0
### Options
- Added option to randomize music (by Battlecats59)
- Added option to force swords at the end of dungeons (by YourAverageLink)
- Added option to visually swap Skyloft and hero's clothes
- Added options to skip Horde, Ghirahim 3, and Demise (by Battlecats59)
- Added option to start with Earth Temple opened
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
  - Improved how the randomizer categorizes regions as barren
- Spoiler logs are now put into the `logs` folder next to the exe
- Make tornadoes spawn away further away to adjust for the increased loftwing speed
- Added more cutscene skips (by YourAverageLink)
### Bugfixes
- Added some tricks that were in the logic files but not in options (by NULL)
- Fix bug with arc-replacements causing an error if the arc doesn't exist in ObjectPack, it's ignored now
- Fix Sandship Timeshift stone not being unset when leaving the dungeon in entrance rando
- Fix a bug in trials where you could be unable to get the item with glitches
- Fix a bug which prevented hints from being placed correctly 

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
- Treasure and Rupee dowsing are now obtainable after getting the Goddess White Sword
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
