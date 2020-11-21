from collections import OrderedDict

POTENTIALLY_REQUIRED_DUNGEONS = ['Skyview','Earth Temple','Lanayru Mining Facility','Ancient Cistern','Sandship','Fire Sanctuary']

DUNGEON_NAMES = OrderedDict([
    ("SW",  "Skyview"),
    ("ET",   "Earth Temple"),
    ("LMF", "Lanayru Mining Facility"),
    ("AC",   "Ancient Cistern"),
    ("SS",   "Sandship"),
    ("FS",   "Fire Sanctuary"),
    ("SK",   "Skykeep"),
    ('LanayruCaves', 'Lanayru Caves'), # "short name" doesn't allow space
])
DUNGEON_NAME_TO_SHORT_DUNGEON_NAME = OrderedDict([v, k] for k, v in DUNGEON_NAMES.items())

ALL_TYPES = ['sky', 'thunderhead', 'faron', 'eldin', 'lanayru', 'dungeon', 'mini dungeon',  'free gift',
             'freestanding', 'miscellaneous', 'silent realm', 'digging', 'bombable', 'combat', 'song', 'spiral charge',
             'minigame', 'batreaux', 'crystal', 'short', 'long', 'crystal quest', 'scrapper', 'goddess', 'faron goddess', 'eldin goddess',
             'lanayru goddess', 'floria goddess', 'summit goddess', 'sand sea goddess']
