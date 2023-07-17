# Changelog

## Dev
### Options
- Added Tadtonesanity (by CovenEsme)
  - Added 17 "Group of Tadtones" items to the item pool
    - You can hand in all 17 to the Water Dragon to get an item
    - You can check how many tadtone groups you have by talking to Fi
  - Added 17 checks in Flooded Faron Woods
    - Collecting each vanilla group of tadtones in Flooded Faron Woods will give you an item
- Added an option to reduce the number of Peatrice conversations needed before she calls you "Darling" (by CovenEsme)
- Renamed "shopsanity" option to "Beedle Shopsanity" (by CovenEsme)
- Added option for "Gear Shopsanity" (by CovenEsme)
- Added option for "Potion Shopanity" (by CovenEsme)
### Changes
- Getting an item underwater gives the item immediately (instead of having to stand on solid ground)
- Added Fi hints (by YourAverageLink)
  - Fi hints are a new field in hint distribution files. The number indicated on the field is how many gossip stone hints will be placed in the Fi menu
    - Fi hints take priority over gossip stone hints; that is, they will be placed on Fi first, then on gossip stones if needed
    - You may now set the hints per stone count of gossip stones to 0
    - Fi's hints may be seen in her menu, by selecting Information -> Hints
      - The information menu is also where Play Time now resides
- Moved Golo to layer 0 in Lanayru Caves
- Add an option for a custom hint distribution (by cjs07)
- The Sand Sea boat moves faster (by YourAverageLink)
  - Its base speed is 1.5x faster. Sprinting now multiplies its speed by 3 instead of 2, for a total change of 2.25x from before.
- Removed Fi text trigger surrounding the Hook Beetle Fight check
- The shortcut log from the Sealed Grounds Spiral to Behind the Temple is now always pushed down
- The progress text shown at the bottom of save files now shows information about your progress towards the end of the seed (rather than the vanilla game) (by CovenEsme)
- Expanded Shopsanity (by CovenEsme)
  - Beedle Shopsanity checks have been renamed based on their location in the shop (instead of their prices)
  - Gear Shopsanity adds a check to each of the item slots in Rupin's shop (next to Peatrice's Item Check in the Bazaar)
    - All shop slots are always available to be bought
    - After buying an item, it will become sold out until you leave and re-enter the Bazaar after which the vanilla item can be bought repeatedly
    - If disabled, each shop slot will contain its vanilla item which can be bought repeatedly
  - Potion Shopsanity adds a check to each potion vat (next to Sparrot's Fortune-telling Stall in the Bazaar)
    - Each potion requires an Adventure Pouch and an Empty Bottle
      - The Stamina Potion also requires Lanayru Mining Facility to be raised
      - The Air Potion also requires you to have the Water Scale
    - When buying a specific potion for the first time, you will also get a random item (in addition to the potion)
    - The potion lady (Luv) tells you the item you can get by interacting with each potion vat (even if you can't buy it yet)

### Bugfixes
- Ensure the tadtones jingle music isn't randomized or manually replaced to prevent a softlock
- Fix bug where Fledge wouldn't correctly spawn for the Archery minigame when starting with the bow

## 1.4.1
### Bugfixes
- Fix Sealed Grounds crashing after receiving the fire dragon item after obtaining the other dragon items

## 1.4.0
### Options
- Split hero mode options to make each effect individually toggleable (by Zeldex)
  - Option to allow recovery hearts to spawn
  - Option to have upgraded skyward strike
  - Option to have faster air meter depletion
- Added option to freely choose the damage multiplier
- Added option to start with various items (by CovenEsme)
  - Includes: b-wheel items, pouches, quest items, songs, triforces, wallets, extra wallets, gratitude crystal packs, harp, water scale, earrings, mitts, life tree seedling, sea chart, spiral charge, stone of trials and Earth Temple key pieces.
  - Added option to start with extra health
  - Added option to start with a random progress item
  - Added option to start with max bugs and treasures
  - Added option to start with a full wallet
  - Added option to start with Hylian Shield
  - Added option to start with Empty Bottles
- Added the ability to ban individual locations (by cjs07)
- Removed the "Banned Types" option
- Added chest dowsing functionality as an option (by YourAverageLink)
  - Uses the main quest dowsing slot (top slot), with a custom dowsing icon to indicate its usage for chests.
  - Vanilla: No change in dowsing functionality (rupee/treasure dowsing works on chests)
  - All Chests: Main quest dowsing will point to all chests. This means you cannot dowse for chests with rupee/treasure dowsing.
  - Progress Items: Main quest dowsing will point to chests that contain progress items
  - Currently does not work on goddess chests
- Added option to enable dowsing in dungeons (by YourAverageLink, but shoutouts to Zeldex)
- Added hint distribution designed for use with the new chest dowsing feature 
  - Removes hints for easily dowsable chests and adds some for non-dowsable checks
  - Only shows one hint per Gossip Stone
- Added an accessibility toggle for light and dark themes (by CovenEsme)
  - You can now pick to have a light theme, dark theme, or to automatically change based on the theme of your computer
- Accessibility options (by CovenEsme)
  - Added a toggle for enabling and disabling a custom theme 
  - Added a button that opens a window with customization options for the theme of the randomizer
    - It is now possible to customize the way the randomizer program looks in fine detail
    - You can customize the light and dark mode colors of each widget to create a custom theme that works in both light and dark modes
    - Widgets are grouped into categories that can be selected with a drop down menu
    - Hovering over a widget label will show a tooltip describing what it does
  - Added theme presets
    - Allows you to choose between various theme presets. Currently, there are "Default", "High Contrast", and "Readibility" options
    - The "Readibility" theme preset also changes the font family to "OpenDyslexic3"
  - Added font settings
    - It is now possible to set the font family used by the randomizer program
    - It is also possible to change the font point size. The default value is 10 (previously 9), can go as small as 6 and as large as 14.
  - Added option to make the curved corners of the randomizer interace sharp and pointy instead of curved
- Added option to make wallet upgrades come pre-filled with Rupees
- Added option to make sword reward place swords on heart containers rather than final checks (by YourAverageLink)
- Added options to control entry into Lake Floria
  - Talk to Yerbal: You are required to talk to Yerbal and he will open the floria door
  - Vanilla: You are logically required to talk to Yerbal and draw on the floria door
  - Open: The floria door is open from the start of the game. You are not required to talk to Yerbal or draw on the floria door
- Updated existing `fix-bit-crashes` option to a `bit-patches` option (by CovenEsme)
  - This option is now a drop-down choice instead of a toggle
  - A new option for `disable-bit` has been added that prevents all instances of the Back in Time (BiT) trick from being performed
  - A new option for `vanilla` has been added that keeps the vanilla game behaviour where BiT is possible but crashes under certain circumstances
  - The `fix-bit-crashes` option works the same as it did previously
- Added cosmetic option to set the in-game interface setting from the start of the game (by CovenEsme)
  - It is now possible to start with the Standard, Light, or Pro interface without having to change the setting from the inventory screen
- Added cosmetic option to control the number of stars that appear in the sky (by CovenEsme)
  - This works with both the stars in the daytime sky (if the "Starry Skies" cosmetic option is enabled) and the usual stars in the nighttime sky
  - The default value is 700 and matches how things worked before
  - Values larger than 700 will decrease the performance of the game
- Added cosmetic option to have stars appear in the sky during both day and night (by CovenEsme)
  - Stars appear on the surface regions, the Sky and Skyloft
  - Some users (particularly Wii Console users) may experience some minor lag when enabling this option (can be adjusted)
- Added cosmetic option to have a lightning skyward strike effects. (by Zeldex)
- Added option to randomize the boss key puzzles (by CovenEsme)
- Added option to get all extra dowsing abilities after obtaining Whitesword (by Peppernicus)
- Added option to remove enemy battle music (by YourAverageLink)
### Changes
- Added Bokoblin Base as a region visitable in the randomizer (by CovenEsme)
  - Talking to the Shiekah Stone in the first room in Eldin Volcano takes you to the Bokoblin Base jail
  - Talking to the Shiekah Stone in the Bokoblin Base jail takes you back to Eldin Volcano
  - Adds 10 total checks to Bokoblin Base
    - Moves the first 2 chests in Volcano Summit back to Bokoblin Base now that it can be accessed
  - Summit cannot be entered without Fireshield Earrings. Fi will appear as in Eldin Volcano
  - Talking to the Fire Dragon sets Boko Base as completed
    - Leaving the Fire Dragon's Lair after talking to him puts you back in normal Volcano Summit
    - The 3 chests in Boko Base Volcano Summit can be obtained in normal Volcano Summit after talking to the Fire Dragon
    - The lava platforms found in Boko Base will also appear in Eldin Volcano after talking to the Fire Dragon
- Added 2 new hint stones in Eldin Volcano / Bokoblin Base (by CovenEsme)
  - Accessible via the lava platforms in Boko Base (or the newly added ones in Eldin), the 2 Eldin caves each contain a Gossip Stone
- Added Water Dragon to the Great Tree (by CovenEsme)
- Added entrance and exit to and from Flooded Great Tree (by CovenEsme)
  - Entering Flooded Great Tree for the first time automatically starts the Tadtones story quest
  - New logical option for completing the Owlan's Crystals check
    - Added access to Flooded Faron Woods as an alternative to needing bomb bag
- New GUI (by cjs07)
  - Rearranged options and regrouped into simpler, broader categories
  - Removed the Progress Locations tab
  - Made many miscellaneous changes
- Added quick text (by CovenEsme and Muzugalium - with help from Lepelog and YourAverageLink)
  - Removes the delay between clearing a textbox and being able to clear the next one
  - Removes the delay between opening a textbox and being able to clear the textbox
  - Removes the background blur to text due to a visual bug
  - Added the ability to hold down the B button to clear textboxes
- Removed first time textboxes (by CovenEsme)
  - Removes rupee, heart, arrow, bomb, deku seed, stamina fruit, silent realm tear and light fruit first time textboxes
- Removed/shortened cutscenes/dialogue
  - Removed all skippable cutscenes except boss intro cutscenes (by CovenEsme)
    - When starting a new file, Link will now spawn directly in his room
  - Removed the panning cutscenes during the Fledge's Gift check (by CovenEsme)
  - Shortened Yerbal's text to become in-line with the rest of the randomizer (by CovenEsme)
  - Removed the cutscene after completing the Isle of Songs puzzle (by CovenEsme and Zeldex)
  - Removed thrill digger tower cutscene (by Muzugalium)
  - Removed lily pad flipping cutscenes (by Muzugalium)
  - Removed pyrup cutscene (by Muzugalium)
  - Removed camera pans during Golo's gift (by Muzugalium)
  - Removed mogma cutscene before circles (by Muzugalium)
  - Sped up bridge extending cutscenes in Eldin (by lepelog)
- Presets (by cjs07)
  - Presets allow users to save and load their favorite settings quickly from the main page of the randomizer
  - The randomizer is distributed with a set of default presets that cannot be changed
    - This list includes all 6 Season 2 Tournament modes and a new beginner friendly mode
  - Presets persist between versions and are forward compatible with new versions.
  - User preset data is sharable between users via the `presets.txt` file
  - Only options included in permalinks are saved, with the exception of the spoiler log toggle
- Overhauled call Fi menu (by Muzu, CovenEsme, and lepelog)
  - Added menu choice to view required dungeons
    - Removed required dungeons from notice board in academy
  - Added menu choice to view dungeon status
    - Complete/Incomplete/Unrequired
    - Small key count (key piece count for ET)
    - Boss key obtained status
    - Dungeon map obtained status
  - Added menu choice to view item status, this shows the obtained status of items that don't show up on the inventory screen
    - These include caves key, spiral charge, and life tree fruit (with space for life tree seedling when that gets added)
  - Added menu choice to view general requirements for beating a seed (e.g. how to raise and open Gate of Time, etc.)
  - Added explicit menu choice to view play time (temporarily to fill space)
- Added back the Sword Pedestal in the Goddess Statue (by CovenEsme)
  - Pulling out the Goddess Sword from its pedestal now gives the 2 checks within the Goddess Statue
  - The 2 small chests previously found within the Goddess Statue have been removed
- Removed bipping after getting slingshot, practice sword, the Potion Lady's Gift check, buying a shield and Owlan's Gift check (by CovenEsme)
- Expanded arc replacements to cover the remaining unpatched arcs (by Muzugalium)
  - Previously unpatched arcs (such as DoButton.arc) are now picked up from the arc replacements folder and patched
  - The arc replacements folder now supports sub folders so people can organise arcs freely
  - The arc replacements folder is now auto-generated if it doesn't exist
  - Existing Title2D and DoButton patches to add custom title screen and dowsing icons now pull from modified_extract instead of actual_extract so they don't overwrite replaced arcs
  - Due to duplicate arc names, the text arcs found in DATA/files/US/Object and the cursor arcs found in DATA/files/Layout and DATA/files/sys/mpls_movie/layout require specific names in the arc replacements folder
    - Text arcs intended for the en_US folder support the default names (e.g. 0-Common.arc) but also support being prefixed with "en" for consistency (e.g. en0-Common.arc)
    - Text arcs intended for the es_US folder must be prefixed with "es" (e.g. es0-Common.arc)
    - Text arcs intended for the fr_US folder must be prefixed with "fr" (e.g. fr0-Common.arc) 
    - The cursor arc intended for the regular layout folder supports the default name (i.e. cursor.arc)
    - The cursor arc intended for the mpls_movie/layout folder (motion plus tutorial cursor) must be prefixed with "mpls" (i.e. mplscursor.arc)
- Added a copy button that copies the settings string to the clipboard (by CovenEsme)
- Updated and standardized the option tooltip text (by CovenEsme)
  - Tooltip text is now more descriptive
  - Tooltip text now features **bold** highlights for **WARNINGS** regarding potentially troublesome settings and option names for drop down choices
- Renamed Slingshot check to Kikwi Elder's Reward (by YourAveragelink)
- Machi is no longer rescued after beating Skyview (by lepelog)
- Added custom dowsing images for new chest dowsing functionality (by YourAverageLink)
- Added Lanayru Desert map of the past as a starting item (by CovenEsme)
- Shooting the bell during pumpkin archery ends the minigame immediately (by lepelog)
- Removed first set of bars in Sky Keep (by CovenEsme)
  - The first chest in Sky Keep is no longer required to get the other checks within Sky Keep
- Removed lavafall in front of ET boss door (by CovenEsme and Peppernicus)
- Added seed and permalink to error messages (by cjs07)
- Removed the check for a button combination to show the built in crash screen (by lepelog)
- Added changelog to the download
### Bugfixes
- Fixed a bug that prevented tricks from being properly reloaded when the randomizer restarted multiple times without changes to the list
- Fixed a softlock caused by collecting the last 2 tears in a trial too close together
- Fixed a bug that would make sandship dowsing sometimes not be the top dowsing slot icon; it now has top priority
- Fixed light pillars not visually appearing when obtaining a tablet until a reload
- Fixed Early Lake Floria Tricks not actually changing logic
- Fixed Yerbal's map hint not showing the X marker on the map
- Fixed bug where setting the `map-mode` or `boss-key-mode` options to "Vanilla" AND starting with some but not all maps or boss keys would throw an error
  - Any maps or boss keys NOT added as starting items will now be placed in their vanilla locations (if the `map-mode`/`boss-key-mode` options are set to "Vanilla")
  - Any maps or boss keys added as starting items will be added to the starting inventory
- Fixed UI scaling issues. The randomizer program now scales when resized instead of remaining a fixed size.
- Fixed bug where most items in Beedle's Shop where partially hidden in the table
- Fixed bulk mode for Windows
- Fixed barbed wire staying after obtaining triforce of wisdom
- Fixed Windows file encoding bug
- Fixed Beedle's Shop rupees showing the wrong color
- Fixed crash in Bug Heaven minigame


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
    - Faron Woods - Kikwi Elder's Reward
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
