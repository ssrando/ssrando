
PROGRESS_ITEMS = [
  "Slingshot",
  "Bomb Bag",
  "Gust Bellows",
  "Whip",
  "Bow",

  "Water Scale",
  "Fireshield Earrings",
  "Clawshots",
  "Stone of Trials",
  
  "Sea Chart",

  # currently, all pillars are open at the start
  "Emerald Tablet",
  "Ruby Tablet",
  "Amber Tablet",

  "Adventure Pouch",
  "Baby Rattle",
  "Cawlin's Letter",
  "Hornet Colossus Beetle",

  "Goddess Harp",
  "Ballad of the Goddess",
  "Farore's Courage",
  "Nayru's Wisdom",
  "Din's Power",
  "Faron Song of the Hero Part",
  "Eldin Song of the Hero Part",
  "Lanayru Song of the Hero Part",

  "Revitalizing Potion"
] + \
  ["5 Gratitude Crystals"]*13 + \
  ["Gratitude Crystal"]*15 + \
  ["Progressive Sword"]*6 + \
  ["Progressive Mitts"]*2 + \
  ["Progressive Beetle"]*2 + \
  ["Key Piece"]*5 + \
  ["Empty Bottle"]*4

NONPROGRESS_ITEMS = [
  "Wooden Shield",
  "Hylian Shield",

  "Cursed Medal",
  "Treasure Medal",
  "Life Medal",
  "Potion Medal",

  "Pouch Expansion",
  "Small Seed Satchel",
  "Small Bomb Bag",
  "Small Quiver",
  
] + \
  ["Heart Medal"]*2 + \
  ["Rupee Medal"]*2 + \
  ["Heart Piece"]*24 + \
  ["Heart Container"]*6 + \
  ["Progressive Wallet"]*4

  # not: Wallets are currently not considered progress items since they don't lock anything

CONSUMABLE_ITEMS = \
   4 * ["Blue Rupee"] + \
  25 * ["Red Rupee"] + \
  12 * ["Silver Rupee"] + \
  10 * ["Gold Rupee"] + \
  10 * ["Semi Rare Treasure"] + \
   1 * ["Golden Skull"] + \
  12 * ["Rare Treasure"] + \
   2 * ["Evil Crystal"] + \
   2 * ["Eldin Ore"] + \
   1 * ["Goddess Plume"] + \
   1 * ["Dusk Relic"] + \
   1 * ["Tumbleweed"] + \
   1 * ["5 Bombs"]

# Once all the items that have a fixed number per seed are used up, this list is used.
# Unlike the other lists, this one does not have items removed from it as they are placed.
# The number of each item in this list is instead its weighting relative to the other items in the list.
DUPLICATABLE_CONSUMABLE_ITEMS = [
  "Blue Rupee",
  "Red Rupee",
  "Semi Rare Treasure",
  "Rare Treasure",
]

DUNGEON_PROGRESS_ITEMS = \
  ["SW Boss Key"]  *1 + ["SW Small Key"]  *2 + \
  ["ET Boss Key"]  *1 + ["ET Small Key"]  *0 + \
  ["LMF Boss Key"] *1 + ["LMF Small Key"] *1 + \
  ["AC Boss Key"]  *1 + ["AC Small Key"]  *2 + \
  ["LanayruCaves Small Key"]  *1 + \
  ["SS Boss Key"]  *1 + ["SS Small Key"]  *2 + \
  ["FS Boss Key"]  *1 + ["FS Small Key"]  *3 + \
  ["SK Boss Key"]  *0 + ["SK Small Key"]  *1

  # note: Lanayru Caves is technically not a dungeon, but has to be treated as such for non key sanity

DUNGEON_NONPROGRESS_ITEMS = \
  ["SW Map"] + \
  ["ET Map"] + \
  ["LMF Map"] + \
  ["AC Map"] + \
  ["SS Map"] + \
  ["FS Map"] + \
  ["SK Map"]
