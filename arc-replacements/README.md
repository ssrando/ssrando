# arc-replacements guide
## Overview
You can use this folder to add custom `.arc` files into the randomizer. Files that have a name matching a Skyward Sword *arc* will get patched with your custom file. This can be used for custom models and textures.

You can create sub-folders to help organize your *arcs*. The randomizer will search through all the folders in `arc-replacements` for you. Any *arcs* with a name that doesn't match a name expected by the randomizer will be ignored.

## Basic Use
If you provide the randomizer an NTSC-U 1.0 ISO, it will create an `actual-extracts` folder. You can use this to find all the *arcs* that are possible to customize.

For more information about how to edit models and textures, consider joining the modding community in the [Skyward Sword Randomizer Discord](https://discord.gg/evpNKkaaw6).

## Duplicate ARC Names
Unfortunately, there are a few *arcs* that share names. The randomizer handles these in slightly different ways. These are:
* Duplicate stage *arcs*
  * *arcs* found in the `actual-extract/DATA/files/Stage` folder may contain duplicates (e.g. the heart container arc appears multiple times).
  * These *arcs* cannot be individually customized. Adding a stage *arc* into `arc-replacements` will replace every occurance of that *arc*. So replacing the heart container *arc* will use your custom *arc* for every heart container in the game.
* Duplicate text *arcs*
  * *arcs* found in the `actual-extract/DATA/files/US/Object` are the text localisations for `en_US`, `es_US`, and `fr_US`.
  * Each contains 6 *arcs* of the form `[number]-[region-name].arc` (e.g. `0-Common.arc`).
  * To replace these, prefix your custom *arc* name with the language. So to replace `fs_US/2-Forest.arc`, name your custom *arc* `fr2-Forest.arc`.
  * A custom *arc* with an unprefixed name (e.g.) `3-Mountain.arc` will replace `en_US/3-Mountain.arc`.
* Duplicate `cursor.arc`
  * There are two `cursor.arc` files used by Skyward Sword - the normal cursor and the one used in the Wii Motion Plus tutorial.
  * The normal cursor *arc* (`actual-extract/DATA/files/Layout`) can be replaced with a custom *arc* named `cursor.arc` added to the `actual-extracts` folder.
  * The Wii Motion Plus cursor *arc* (`actual-extract/DATA/files/sys/mpls_movie/layout`) can be replaced with a custom *arc* named `mplscursor.arc`.

## Overwritten Textures
Currently, the randomizer replaces 2 textures. These are the title screen logo and the sandship dowsing icon. It is currently not possible to customize these textures (although this is planned). Other resources in their parent *arcs* can still be customised though.