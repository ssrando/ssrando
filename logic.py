from typing import List, Optional
import random
import yaml
from collections import defaultdict
import re

DUNGEONS = ['Skyview', 'ET', 'LMF', 'AC', 'Sandship', 'FS', 'Skykeep', 'Lanayru Caves'] # caves has a key

def get_randomized_checks():
    with open('SS Rando Logic - Item Location.yaml') as f:
        checks = yaml.safe_load(f)
    with open('items.yaml') as f:
        items = yaml.safe_load(f)

    filled_checks = dict()
    empty_checks = set()
    dungeonchecks = defaultdict(list)

    seed = random.randint(0, 1000000-1)
    random.seed(seed)

    all_checks = []
    item_pool = []
    for i, (name, check) in enumerate(checks.items()):
        area = name.split(' - ')[0]
        item = check.get('original item',None)
        if item is None:
            print(check)
            continue
        if area in DUNGEONS:
            dungeonchecks[area].append(name)
        else:
            all_checks.append(name)
        item_pool.append(item)

    by_item_name=dict((x['name'],x) for x in items)

    # make sure dungeon items exist
    for dungeon in DUNGEONS:
        by_item_name[f'{dungeon} Small Key'] = by_item_name['Small Key']
        # by_item_name[f'{dungeon} Map'] = by_item_name['Map']

    # shuffle dungeon specific items only in the dungeon itself
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

    with open('spoiler.txt','w') as f:
        f.write(f'Seed: {seed}\n')
        for name in checks.keys():
            f.write(f'{name}: {filled_checks[name]}\n')
    # (stage, room) -> (object name, layer, id?, itemid)
    stagepatchv2 = defaultdict(list)
    # (stage, layer) -> oarc
    stageoarcs = defaultdict(set)
    # # eventfile: (line, itemid)
    eventpatches = defaultdict(list)

    stage_re = re.compile(r'stage/(?P<stage>[^/]+)/r(?P<room>[0-9]+)/l(?P<layer>[0-9]+)/(?P<objname>[a-zA-Z]+)(/(?P<objid>[^/]+))?')
    event_re = re.compile(r'event/(?P<eventfile>[^/]+)/(?P<eventid>[^/]+)')
    oarc_re = re.compile(r'oarc/(?P<stage>[^/]+)/l(?P<layer>[^/]+)')

    for checkname, itemname in filled_checks.items():
        check = checks[checkname]
        item = by_item_name[itemname]
        for path in check['Paths']:
            stage_match = stage_re.match(path)
            event_match = event_re.match(path)
            oarc_match = oarc_re.match(path)
            if stage_match:
                stage = stage_match.group('stage')
                room = int(stage_match.group('room'))
                layer = int(stage_match.group('layer'))
                objname = stage_match.group('objname')
                objid = stage_match.group('objid')
                oarc = item['oarc']
                if oarc:
                    if isinstance(oarc, list):
                        for o in oarc:
                            stageoarcs[(stage, layer)].add(o)
                    else:
                        stageoarcs[(stage, layer)].add(oarc)
                stagepatchv2[(stage, room)].append((objname, layer, objid, item['id']))
            elif event_match:
                eventfile = event_match.group('eventfile')
                eventid = int(event_match.group('eventid'))
                eventpatches[eventfile].append((eventid, item['id']))
            elif oarc_match:
                stage = oarc_match.group('stage')
                layer = int(oarc_match.group('layer'))
                oarc = item['oarc']
                if oarc:
                    if isinstance(oarc, list):
                        for o in oarc:
                            stageoarcs[(stage, layer)].add(o)
                    else:
                        stageoarcs[(stage, layer)].add(oarc)
            else:
                print(f'ERROR: {path} didn\'t match any regex!')
    return stagepatchv2, stageoarcs, eventpatches