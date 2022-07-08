# SSR Hint Distributions

Hint distributions define everything about how gossip stone hints are placed by the randomizer. Distributions have the ability to fine tune exactly how hints are placed in the world, by banning specific stones, adding and removing items and locations from their respecitve pools, and more.


**Hint Types**
- **Always**: Always hints hint locations that are long, out of the way, or have differeing requirements from other nearby checks causing for long double dips. When enabled, they are placed first, regardless of order, and all of them are always generated
- **Sometimes**: Sometimes hints are locations that annoying for various reasons, they have differing requirements, they require a lot of items, or they can be routed around if they are junk, among others.
- **Spirit of the Sword (SotS)**: SotS hints hint regions that contain items that are required to beat the game. The randomizer decides if an item is required by removing it from the game and checking if it is still beatable.
- **Goal Hints (aka as path hints)**: Goal hints act similarly to SotS hints, but they hint regions that contain items specifically required to complete a given required dungeon, and they will show both the dungeon boss referred to and the region containing the item. The randomizer decides if an item is on the path to a boss by removing it from the game and checking if it is still possible to defeat the boss. IMPORTANT - The fixed count works a bit differently for goal hints. For each fixed count in the distribution, one goal hint will be placed for a required dungeon. For example: a fixed of 1 with 3 required dungeons will result in three goal hints being placed, one for each required dungeon.
- **Barren**: Barren hints hint to regions that do not require any progression items, regardless of if the items thenselvews are reqired
- **Item**: Item hints directly hint the location of a potentially valuable item.
- **Random**: Random hints tell the item on randomly selected locations
- **Junk**: Junk hints are random tips or community memes


## Existing Distributions
- **Balanced**: The recommended way to play the randomizer casually. Balances the various hint types can includes all the important locations and items for hints. Hints will neither be too strong or to weak, nor will their be many junk hints eating away at your valuable hint slots
- **Junk**: Fills the seed entirely with junk hints. Reading gossip stones will be a complete waste of time, but should get a good laugh out of you
- **Strong**: Fills the world with stronger hints. Removes some of the less important hintable locations and items to make the average hint stronger. Contains even less junk hints than Balanced.


## Creating New Distributions
All fields are **required** in all distribution files, however, specific hint types can be omitted from the actual distribution, however this is not recommended.

## Fields
- banned_stones (Array of strings)
  - List of all the gossip stones that cannot have useful hints placed on them
  - Names must match the exact internal naming structure of the randomizer, which can be found in hints.yaml in the root directory
- added_locations([{ location: string, type: "always" | "sometimes"}])
  - Adds a location to the specified location pool
  - Must match the check name exactly, as specified in checks.yaml in the root directory
- removed_locations (Array of strings)
  - Removes a location from all location pools. Note that this does not mean it cannot be hinted at all, just not as a location hint
  - Must match the check name exactly, as specified in checks.yaml in the root directory
- added_items ([{ name: string, amount: number }])
  - Adds the sepcified number of copies of the item to the item hint pool
- removed_items (Array of strings)
  - Prevents the specified item from being hinted for any hint type
- dungeon_sots_limit (number)
  - Limits the number of dungeon SotS/Goal hints that can be placed. They will attempt be replaced by a different SotS/Goal hint if a hint past the limit would be placed.
- dungeon_barren_limit (number)
  - Limits the number of barren dungeon hints that can be placed. They will attempt to be replaced by an overworld barren hint if another hint past the limit would be placed.
- distribution (name: distribution_data (see below))
  - Defines the specifics of the distribution

### Distribution Data
- order: defines what order hints should have their fixed quantities generated. Types with the same order will be resolved in the order they are listed in the distribution
- weight: The relative chance that this hint type is randomly selected to be placed
- fixed: Generates the specified number of hints prior to randomly selecting additional hints by weight. Note that this **does not** guarantee that all these hints will be placed depending on the rest of the distribution. For goal hints, the fixed count is multiplied by the number of required dungeons.
- copies: Generates the specified number of copies of the hint everytime a hint of this type is generated (both randomly and fixed). Note that this **does not** guarantee that all copies will be placed, but they will all be generated before the next hint is generated.
