from collections import OrderedDict

POTENTIALLY_REQUIRED_DUNGEONS = ['Skyview','Earth Temple','Lanayru Mining Facility','Ancient Cistern','Sandship','Fire Sanctuary']

DUNGEON_NAMES = OrderedDict([
    ("SV",  "Skyview"),
    ("ET",   "Earth Temple"),
    ("LMF", "Lanayru Mining Facility"),
    ("AC",   "Ancient Cistern"),
    ("SS",   "Sandship"),
    ("FS",   "Fire Sanctuary"),
    ("SK",   "Sky Keep"),
    ('LanayruCaves', 'Lanayru Caves'), # "short name" doesn't allow space
])
DUNGEON_NAME_TO_SHORT_DUNGEON_NAME = OrderedDict([v, k] for k, v in DUNGEON_NAMES.items())

SHOP_CHECKS = [
    "Skyloft - Beedle 50 Rupee Item",
    "Skyloft - Beedle First 100 Rupee Item",
    "Skyloft - Beedle Second 100 Rupee Item",
    "Skyloft - Beedle Third 100 Rupee Item",
    "Skyloft - Beedle 300 Rupee Item",
    "Skyloft - Beedle 600 Rupee Item",
    "Skyloft - Beedle 800 Rupee Item",
    "Skyloft - Beedle 1000 Rupee Item",
    "Skyloft - Beedle 1200 Rupee Item",
    "Skyloft - Beedle 1600 Rupee Item",
]

MAP_CHECKS = [
    'Skyview - Map Chest',
    'Earth Temple - Map Chest',
    'Lanayru Mining Facility - Map Chest',
    'Ancient Cistern - Map Chest',
    'Sandship - Map Chest',
    'Fire Sanctuary - Map Chest',
    'Sky Keep - Map Chest',
]

SMALL_KEY_CHECKS = [
    'Skyview - Behind Two Eyes',
    'Skyview - Behind Three Eyes',
    'Lanayru Mining Facility - First Chest in Hub Room',
    'Ancient Cistern - Small Key Chest',
    'Ancient Cistern - Bokoblin',
    'Sandship - Behind Combination Lock',
    'Sandship - Robot in Brig',
    'Fire Sanctuary - First Room',
    'Fire Sanctuary - Second Small Key Chest',
    'Fire Sanctuary - Third Small Key Chest',
    'Lanayru Caves - Golo',
    'Sky Keep - Small Key Chest'
]

BOSS_KEY_CHECKS = [
    'Skyview - Boss Key',
    'Earth Temple - Boss Key',
    'Lanayru Mining Facility - Boss Key',
    'Ancient Cistern - Boss Key',
    'Sandship - Boss Key',
    'Fire Sanctuary - Boss Key',
]

ALL_TYPES = ['skyloft', 'sky', 'thunderhead', 'faron', 'eldin', 'lanayru', 'dungeon', 'mini dungeon',  'free gift',
             'freestanding', 'miscellaneous', 'silent realm', 'digging', 'bombable', 'combat', 'song', 'spiral charge',
             'minigame', 'crystal', 'short', 'long', 'fetch', 'crystal quest', 'scrapper', 'peatrice', 'beedle',
             'cheap', 'medium', 'expensive',
             'goddess', 'faron goddess', 'eldin goddess', 'lanayru goddess', 'floria goddess', 'summit goddess',
             'sand sea goddess']
