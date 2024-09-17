# BRLAN tools

In order for the randomizer to display the correct tablets and gemstones
in the pause menu (instead of a fixed order - Emerald, Ruby, Amber),
the randomizer requires patches to the brlan file that contains UI animation
data in a binary format. This document describes what changes were made,
since the changed binary file cannot be inspected and I'd like the process
to be reproducible in case someone wants to touch that file again.

Required tools:

* [BrawlCrate](https://github.com/soopercool101/BrawlCrate)
* [Benzin](https://horizon.miraheze.org/wiki/Benzin)

* Open `DATA/files/US/Layout/MenuPause.arc` with BrawlCrate
* Extract `anim/pause_00_sekiban.brlan` in BrawlCrate
* Run `.\BENZIN.exe r pause_00_sekiban.brlan pause_00_sekiban.xmlan`
* Change `<pai1 framesize="5" flags="00">` to `<pai1 framesize="8" flags="00">`
  * This extends the animation to 8 frames total (keyframes 0 to 7)
* Add four `<timg name="tr_sekiban_03.tpl" />` entries (03 through 06) at the end of the `<timg />` list
  * This adds the additional tablet combinations to the texture pattern index
* Add four keyframe `<pair>`s to `P_sekiban_00`: [3.0, 0014], [4.0, 0015], [5.0, 0016], [6.0, 0017]
  * This gives the tablet element the info to pick the correct texture
* Add keyframes to `N_stone_00`, `N_stone_01`, `N_stone_02`:
  * `N_stone_00`: [4.0, 0] (turned off at frame 4)
  * `N_stone_01`: [3.0, 0], [5.0, 1]
  * `N_stone_02`: [6.0, 0]
* Run `.\BENZIN.exe w pause_00_sekiban.xmlan pause_00_sekiban.modified.brlan`

Now you have a brlan file that works with the rando patches (cf. )