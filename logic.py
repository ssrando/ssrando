from typing import List, Optional
import random
import yaml
from collections import defaultdict
import re

class Item:
    def __init__(self, name: str, id: int, oarcs: List[str]):
        self.name = name
        self.id = id
        self.oarcs = oarcs

class Check:
    def __init__(self, name: str, patchparams: dict, index: int, item: Optional[Item]):
        self.name = name
        self.patchparams = patchparams
        self.index = index
        self.original_item = item
        self.item = None
    
    def __str__(self):
        return f'{self.name}: {self.item["name"]}'

DUNGEONS = ['Skyview', 'ET', 'LMF', 'AC', 'Sandship', 'FS', 'Skykeep', 'Lanayru Caves'] # caves has a key


with open('SS Rando Logic - Item Location.yaml') as f:
    checks = yaml.safe_load(f)
with open('items.yaml') as f:
    items = yaml.safe_load(f)

filled_checks = dict()
empty_checks = set()
dungeonchecks = defaultdict(list)

all_checks = []
item_pool = []
for i, (name, check) in enumerate(checks.items()):
    area = name.split(' - ')[0]
    item = check.get('original item',None)
    if item is None:
        print(check)
        continue
    check = Check(name, check, i, item)
    if area in DUNGEONS:
        dungeonchecks[area].append(name)
    else:
        all_checks.append(name)
    item_pool.append(item)

by_item_name=dict((x['name'],x) for x in items)

for dungeon in DUNGEONS:
    dungeon_items = list(filter(lambda item: item.startswith(dungeon), item_pool))
    for item in dungeon_items:
        item_pool.remove(item)
    random.shuffle(dungeonchecks[dungeon])
    for item in dungeon_items:
        check = dungeonchecks[dungeon].pop()
        filled_checks[check] = item
    all_checks.extend(dungeonchecks[dungeon])

assert len(all_checks) == len(item_pool)

random.shuffle(item_pool)
for check, item in zip(all_checks, item_pool):
    filled_checks[check] = item

for name in checks.keys():
    print(f'{name}: {filled_checks[name]}')
# (stage, room, layer) -> (object name, id?, itemid)
# stagepatchv2 = defaultdict(list)
# stageoarcs = defaultdict(set)
# # eventfile: (line, itemid)
# eventpatches = defaultdict(list)

# stage_re = re.compile(r'stage/(?P<stage>[^/]+)/r(?P<room>[0-9]+)/l(?P<layer>[0-9]+)/(?P<objname>[a-zA-Z]+)(/(?P<objid>[^/]+))?')
# event_re = re.compile(r'event/(?P<eventfile>[^/]+)/(?P<eventid>[^/]+)')
# oarc_re = re.compile(r'oarc/(?P<stage>[^/]+)/l(?P<layer>[^/]+)')

# for check in all_checks:
#     for path in check.patchparams['Paths']:
#         stage_match = stage_re.match(path)
#         event_match = event_re.match(path)
#         oarc_match = oarc_re.match(path)
#         if stage_match:
#             stage = stage_match.group('stage')
#             room = int(stage_match.group('room'))
#             layer = int(stage_match.group('layer'))
#             objname = stage_match.group('objname')
#             objid = stage_match.group('objid')
#             oarc = check.item['oarc']
#             if oarc:
#                 stageoarcs[(stage, layer)].add(oarc)
#             stagepatchv2[(stage, room, layer)].append((objname, objid, check.item['id']))
#         elif event_match:
#             eventfile = event_match.group('eventfile')
#             eventid = int(event_match.group('eventid'))
#             eventpatches[eventfile].append((eventid, check.item['id']))
#         elif oarc_match:
#             stage = oarc_match.group('stage')
#             layer = int(oarc_match.group('layer'))
#             oarc = check.item['oarc']
#             if oarc:
#                 stageoarcs[(stage, layer)].add(oarc)
#         else:
#             print(f'ERROR: {path} didn\'t match any regex!')