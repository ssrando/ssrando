from collections import OrderedDict

POTENTIALLY_REQUIRED_DUNGEONS = [
    "Skyview",
    "Earth Temple",
    "Lanayru Mining Facility",
    "Ancient Cistern",
    "Sandship",
    "Fire Sanctuary",
]

DUNGEON_NAMES = OrderedDict(
    [
        ("SV", "Skyview"),
        ("ET", "Earth Temple"),
        ("LMF", "Lanayru Mining Facility"),
        ("AC", "Ancient Cistern"),
        ("SS", "Sandship"),
        ("FS", "Fire Sanctuary"),
        ("SK", "Sky Keep"),
        ("LanayruCaves", "Lanayru Caves"),  # "short name" doesn't allow space
    ]
)
DUNGEON_NAME_TO_SHORT_DUNGEON_NAME = OrderedDict(
    [v, k] for k, v in DUNGEON_NAMES.items()
)

ENTRANCE_CONNECTIONS = {
    "Dungeon Entrance in Deep Woods": "Skyview",
    "Dungeon Entrance in Eldin Volcano": "Earth Temple",
    "Dungeon Entrance in Lanayru Desert": "Lanayru Mining Facility",
    "Dungeon Entrance in Lake Floria": "Ancient Cistern",
    "Dungeon Entrance in Sand Sea": "Sandship",
    "Dungeon Entrance in Volcano Summit": "Fire Sanctuary",
    "Dungeon Entrance on Skyloft": "Sky Keep",
}

SILENT_REALMS = OrderedDict(
    [
        ("Skyloft Silent Realm", "Skyloft Trial Gate"),
        ("Faron Silent Realm", "Faron Trial Gate"),
        ("Lanayru Silent Realm", "Lanayru Trial Gate"),
        ("Eldin Silent Realm", "Eldin Trial Gate"),
    ]
)

SILENT_REALM_CHECKS = OrderedDict(
    [
        ("Skyloft Silent Realm - Stone of Trials", "Trial Gate on Skyloft"),
        ("Faron Silent Realm - Water Scale", "Trial Gate in Faron Woods"),
        ("Lanayru Silent Realm - Clawshots", "Trial Gate in Lanayru Desert"),
        ("Eldin Silent Realm - Fireshield Earrings", "Trial Gate in Eldin Volcano"),
    ]
)

SHOP_CHECKS = [
    "Beedle - 50 Rupee Item",
    "Beedle - First 100 Rupee Item",
    "Beedle - Second 100 Rupee Item",
    "Beedle - Third 100 Rupee Item",
    "Beedle - 300 Rupee Item",
    "Beedle - 600 Rupee Item",
    "Beedle - 800 Rupee Item",
    "Beedle - 1000 Rupee Item",
    "Beedle - 1200 Rupee Item",
    "Beedle - 1600 Rupee Item",
]

MAP_CHECKS = [
    "Skyview - Chest on Tree Branch",
    "Earth Temple - Chest in West Room",
    "Lanayru Mining Facility - Chest after Armos Fight",
    "Ancient Cistern - Chest after Whip Hooks",
    "Sandship - Chest before 4-Door Corridor",
    "Fire Sanctuary - Chest after Second Trapped Mogma",
    "Sky Keep - First Chest",
]

SMALL_KEY_CHECKS = [
    "Skyview - Chest behind Two Eyes",
    "Skyview - Chest behind Three Eyes",
    "Lanayru Mining Facility - First Chest in Hub Room",
    "Ancient Cistern - Chest in East Part",
    "Ancient Cistern - Bokoblin",
    "Sandship - Chest behind Combination Lock",
    "Sandship - Robot in Brig's Reward",
    "Fire Sanctuary - Chest in First Room",
    "Fire Sanctuary - Chest near First Trapped Mogma",
    "Fire Sanctuary - Chest after Bombable Wall",
    "Lanayru Caves - Golo's Gift",
    "Sky Keep - Chest after Dreadfuse",
]

BOSS_KEY_CHECKS = [
    "Skyview - Boss Key Chest",
    "Earth Temple - Boss Key Chest",
    "Lanayru Mining Facility - Boss Key Chest",
    "Ancient Cistern - Boss Key Chest",
    "Sandship - Boss Key Chest",
    "Fire Sanctuary - Boss Key Chest",
]

END_OF_DUNGEON_CHECKS = OrderedDict(
    [
        ("Skyview", "Skyview - Ruby Tablet"),
        ("Earth Temple", "Earth Temple - Amber Tablet"),
        ("Lanayru Mining Facility", "Lanayru Mining Facility - Goddess Harp"),
        ("Ancient Cistern", "Ancient Cistern - Farore's Flame"),
        ("Sandship", "Sandship - Nayru's Flame"),
        ("Fire Sanctuary", "Fire Sanctuary - Din's Flame"),
    ]
)

STARTING_SWORD_COUNT = {
    "Swordless": 0,
    "Practice Sword": 1,
    "Goddess Sword": 2,
    "Goddess Longsword": 3,
    "Goddess White Sword": 4,
    "Master Sword": 5,
    "True Master Sword": 6,
}

ALL_TYPES = [
    "skyloft",
    "sky",
    "thunderhead",
    "faron",
    "eldin",
    "lanayru",
    "dungeon",
    "mini dungeon",
    "free gift",
    "freestanding",
    "miscellaneous",
    "silent realm",
    "digging",
    "bombable",
    "combat",
    "song",
    "spiral charge",
    "minigame",
    "crystal",
    "short",
    "long",
    "fetch",
    "crystal quest",
    "scrapper",
    "peatrice",
    "beedle",
    "cheap",
    "medium",
    "expensive",
    "goddess",
    "faron goddess",
    "eldin goddess",
    "lanayru goddess",
    "floria goddess",
    "summit goddess",
    "sand sea goddess",
]
