from paths import RANDO_ROOT_PATH
import yaml
from typing import Dict, List, Tuple
from dataclasses import dataclass

CACHE = {}


def read_yaml_file_cached(filename: str):
    if filename in CACHE:
        return CACHE[filename]
    else:
        with (RANDO_ROOT_PATH / filename).open() as f:
            yaml_file = yaml.safe_load(f)
        CACHE[filename] = yaml_file
        return yaml_file


@dataclass
class EntranceDefinition:
    stage: str
    room: int
    layer: int
    entrance: int


@dataclass
class ExitDefinition:
    stage: str
    room: int
    index: int


class EntranceTable:
    def __init__(
        self,
        entrance_map: Dict[str, EntranceDefinition],
        exit_map: Dict[str, List[ExitDefinition]],
        entrances: List[str],
        exits: List[str],
        statue_exits: List[str],
    ):
        self.entrance_map = entrance_map
        self.exit_map = exit_map
        self.entrances = entrances
        self.exits = exits
        self.statue_exits = statue_exits


cached_entrance_table = None


def get_entrance_table() -> EntranceTable:
    global cached_entrance_table
    if cached_entrance_table is not None:
        return cached_entrance_table
    with (RANDO_ROOT_PATH / "entrance_table2.yaml").open("r") as f:
        entrance_table = yaml.safe_load(f)

    def to_exit_name(entry):
        disambig = entry.get("disambiguation")
        door = entry.get("door")
        if door is not None:
            door = f"{door} Door"
        return f'{entry["stage"]} to {", ".join(filter(None, (entry["to-stage"], disambig, door)))}'

    def to_entrance_name(entry):
        disambig = entry.get("disambiguation")
        door = entry.get("door")
        if door is not None:
            door = f"{door} Door"
        return f'{entry["to-stage"]} (from {", ".join(filter(None, (entry["stage"], disambig, door)))})'

    entrance_map = {}
    exit_map = {}
    entrances = []
    exits = []
    statue_exits = []
    for entry in entrance_table:
        if entry.get("type") == "statue":
            # todo name
            for statue_scen in entry["scens"]:
                name = f'{statue_scen["stage"]}, {statue_scen["room"]}, {statue_scen["index"]}'
                exit_map[name] = [statue_scen]
                statue_exits.append(name)
        else:
            entrance_name = to_entrance_name(entry)
            exit_name = to_exit_name(entry)
            entrance_map[entrance_name] = entry["orig"]
            exit_map[exit_name] = entry["scens"]
            exits.append(exit_name)
            entrances.append(entrance_name)
    cached_entrance_table = EntranceTable(
        entrance_map, exit_map, entrances, exits, statue_exits
    )
    return cached_entrance_table


class YamlOrderedDictLoader(yaml.SafeLoader):
    pass


YamlOrderedDictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)),
)
