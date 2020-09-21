from typing import List
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
    def __init__(self, name: str, patchparams: dict):
        self.name = name
        self.patchparams = patchparams
        self.item = None


with open('SS Rando Logic - Item Location.yaml') as f:
    checks = yaml.safe_load(f)
with open('items.yaml') as f:
    items = yaml.safe_load(f)
all_checks = []
item_pool = []
for name, check in checks.items():
    all_checks.append(Check(name, check))
    item = check.get('original item',None)
    if item is None:
        print(check)
        continue
    item_pool.append(check['original item'])
by_item_name=dict((x['name'],x) for x in items)
random.shuffle(item_pool)
for check, item in zip(all_checks, item_pool):
    check.item = by_item_name[item]
# (stage, room, layer) -> (object name, id?, itemid)
stagepatchv2 = defaultdict(list)
stageoarcs = defaultdict(set)
# eventfile: (line, itemid)
eventpatches = defaultdict(list)

stage_re = re.compile(r'stage/(?P<stage>[^/]+)/r(?P<room>[0-9]+)/l(?P<layer>[0-9]+)/(?P<objname>[a-zA-Z]+)(/(?P<objid>[^/]+))?')
event_re = re.compile(r'event/(?P<eventfile>[^/]+)/(?P<eventid>[^/]+)')
oarc_re = re.compile(r'oarc/(?P<stage>[^/]+)/l(?P<layer>[^/]+)')

for check in all_checks:
    for path in check.patchparams['Paths']:
        stage_match = stage_re.match(path)
        event_match = event_re.match(path)
        oarc_match = oarc_re.match(path)
        if stage_match:
            stage = stage_match.group('stage')
            room = int(stage_match.group('room'))
            layer = int(stage_match.group('layer'))
            objname = stage_match.group('objname')
            objid = stage_match.group('objid')
            oarc = check.item['oarc']
            if oarc:
                stageoarcs[(stage, layer)].add(oarc)
            stagepatchv2[(stage, room, layer)].append((objname, objid, check.item['id']))
        elif event_match:
            eventfile = event_match.group('eventfile')
            eventid = int(event_match.group('eventid'))
            eventpatches[eventfile].append((eventid, check.item['id']))
        elif oarc_match:
            stage = oarc_match.group('stage')
            layer = int(oarc_match.group('layer'))
            oarc = check.item['oarc']
            if oarc:
                stageoarcs[(stage, layer)].add(oarc)
        else:
            print(f'ERROR: {path} didn\'t match any regex!')