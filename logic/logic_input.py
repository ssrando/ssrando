from __future__ import annotations
from typing import Deque, Dict, Generic, List, Set, Any, Tuple, TypeVar
from functools import cache
from enum import Enum
from dataclasses import dataclass, field

from .logic_expression import DNFInventory, LogicExpression, EventAtom
from .inventory import EXTENDED_ITEM, Inventory
from .constants import *

import yaml


AllowedTimeOfDay = Enum("AllowedTimeOfDay", ("DayOnly", "NightOnly", "Both"))
DayOnly = AllowedTimeOfDay.DayOnly
NightOnly = AllowedTimeOfDay.NightOnly
Both = AllowedTimeOfDay.Both

yaml.add_representer(
    AllowedTimeOfDay, lambda dumper, data: dumper.represent_int(data.value)
)


class defaultfactorydict(dict):
    def __missing__(self, item):
        return item


events: List[EXTENDED_ITEM_NAME] = []
areas_list: List[Area[LogicExpression]] = []

LE = TypeVar("LE")
LE_bis = TypeVar("LE_bis")

map_exit_suffixes = None


@dataclass
class Area(Generic[LE]):
    name: str
    toplevel_alias: str | None = None
    allowed_time_of_day = AllowedTimeOfDay.DayOnly
    hint_region: str | None = None
    can_sleep: bool = False
    can_save: bool = False
    abstract: bool = False
    sub_areas: Dict[str, Area[LE]] = field(default_factory=dict)
    sub_area_aliases: Dict[str, Area[LE]] = field(default_factory=dict)
    locations: Dict[str, LE] = field(default_factory=dict)
    exits: Dict[str, LE] = field(default_factory=dict)
    entrances: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def of_dict(cls, args):
        return cls(**args)

    @classmethod
    def of_yaml(
        cls,
        name: str,
        raw_dict: Dict[str, Any],
        parent: Area[LogicExpression] | None = None,
    ):
        area: Area[LogicExpression] = cls(name)  # type: ignore

        if (v := raw_dict.get("allowed-time-of-day")) is not None:
            area.allowed_time_of_day = AllowedTimeOfDay[v]
        elif parent is not None:
            area.allowed_time_of_day = parent.allowed_time_of_day
        if (v := raw_dict.get("hint-region")) is not None:
            if v not in ALL_HINT_REGIONS:
                raise ValueError(f"Unknown hint region {v}.")
            area.hint_region = v
        elif parent is not None:
            area.hint_region = parent.hint_region
        if (s := raw_dict.get("toplevel-alias")) is not None:
            area.toplevel_alias = s
        if (b := raw_dict.get("can-sleep")) is not None:
            area.can_sleep = b
        if (b := raw_dict.get("can-save")) is not None:
            area.can_save = b

        if (d := raw_dict.get("macros")) is not None:
            area.abstract = True
            assert "locations" not in raw_dict
            area.locations = {k: LogicExpression.parse(v) for k, v in d.items()}
            for k in d:
                if " - " not in k:
                    events.append(with_sep_full(name, k))

        if (d := raw_dict.get("locations")) is not None:
            area.abstract = False
            assert "macros" not in raw_dict
            area.locations = {k: LogicExpression.parse(v) for k, v in d.items()}
            for k in d:
                if " - " not in k:
                    events.append(with_sep_full(name, k))

        if (d := raw_dict.get("exits")) is not None:
            area.exits = {k: LogicExpression.parse(v) for k, v in d.items()}

        if (v := raw_dict.get("entrance")) is not None:
            if parent is None:
                raise ValueError("An entrance was given but no parent to give it to.")
            rel_name = name.rsplit("\\", 1)[-1]
            req0 = parent.exits.get(rel_name)
            req1 = LogicExpression.parse(v)
            req = req0 | req1 if req0 is not None else req1
            parent.exits[rel_name] = req

        area.sub_areas = {
            k: cls.of_yaml(with_sep_full(name, k), v, area)
            for k, v in raw_dict.items()
            if "A" <= k[0] <= "Z"
        }
        areas_list.append(area)
        return area

    def map(
        self,
        floc: Callable[[str, str, LE], Tuple[str, LE_bis]],
        fexit: Callable[[str, str, LE], Tuple[Tuple[str, LE_bis] | None, str | None]],
    ):
        new_self: Area[LE_bis] = self  # type: ignore
        d: Dict[str, LE_bis] = {}
        for k, v in self.locations.items():
            k, v = floc(self.name, k, v)
            d[k] = v
        new_self.locations = d

        new_exits = {}
        entrances = dict()
        for k, v in self.exits.items():
            exit, entrance = fexit(self.name, k, v)
            if exit is not None:
                exit, req = exit
                new_exits[exit] = req
            if entrance is not None:
                entrances[entrance] = entrance

        new_self.exits = new_exits
        new_self.entrances = entrances

        for sub_area in self.sub_areas.values():
            sub_area.map(floc, fexit)

    def __getitem__(self, element: str):
        return self.lookup(element, direct=True)

    def __setitem__(self, alias, area):
        self.sub_area_aliases[alias] = area
        return

    def __hash__(self):
        return hash(self.name)

    @cache
    def lookup(self, element: str, /, direct: bool) -> EXTENDED_ITEM_NAME | Area:
        """
        Computes the thing referred by [element] in area [self]. Must not be ambiguous
        In a direct search, consider child elements as unambiguous.
        """

        assert " - " not in element
        found_as_child = None
        if (
            element in self.locations
            or element in self.entrances
            or (element in self.exits and element in map_exit_suffixes)
        ):
            # If exit, exclude logical exits and only keep map exits
            found_as_child = with_sep_full(self.name, element)

        if element in self.sub_areas:
            found_as_child = self.sub_areas[element]

        if element in self.sub_area_aliases:
            found_as_child = self.sub_area_aliases[element]

        if direct and found_as_child is not None:
            return found_as_child

        results = [
            r
            for sub_area in self.sub_areas.values()
            if (r := sub_area.lookup(element, direct=False)) is not None
        ]

        if len(results) == 0:
            return found_as_child
        if len(results) == 1 and found_as_child is None:
            return results[0]
        raise ValueError(f"Ambiguous element '{element}' from '{self.name}'.")


class Areas:
    areas: Dict[str, Area[DNFInventory]]

    def __getitem__(self, loc):
        return self.areas[loc]

    def search(
        self, base_address_str: str, partial_address_str: str
    ) -> EXTENDED_ITEM_NAME:
        """Computes the thing referred by [partial_address] when located at [base_address]"""

        areas = []
        area = self.parent_area
        for base_addr_atom in base_address_str.split("\\"):
            if base_addr_atom == "":
                continue
            areas.append(area)
            area = area.sub_areas[base_addr_atom]

        partial_address = partial_address_str.split(" - ")
        j = 0
        if partial_address[0] == "General":
            area = self.parent_area
            j = 1

        while area[partial_address[j]] is None and areas:
            area = areas.pop()

        for head in partial_address[j:]:
            assert isinstance(area, Area), (base_address_str, partial_address_str, area)
            area = area[head]

            if area is None:
                if base_address_str:
                    s = f"Could not find '{partial_address_str}' from '{base_address_str}'."
                else:
                    s = f"Could not find '{partial_address_str}'."
                raise ValueError(s)
        if isinstance(area, Area):
            return EIN(area.name)
        return area

    def prettify(self, s):
        if s in ALL_ITEM_NAMES:
            return strip_item_number(s)
        if s in self.checks:
            check = self.checks[s]
            return check["short_name"]
        if s in self.gossip_stones:
            return self.gossip_stones[s]["short_name"]
        if "\\" not in s and "#" not in s:
            return s
        raise ValueError(f"Can't find a shortname for {s}.")

    def __init__(
        self,
        raw_area: Dict[str, Any],
        checks: Dict[str, Any],
        gossip_stones: Dict[str, Any],
        map_exits_entrances: Dict[str, Any],
    ):
        map_entrances = {
            k: v
            for k, v in map_exits_entrances.items()
            if v["type"] == "entrance" and not v.get("disabled", False)
        }
        map_exits = {
            k: v
            for k, v in map_exits_entrances.items()
            if v["type"] == "exit" and not v.get("disabled", False)
        }

        self.parent_area = Area.of_yaml(name="", raw_dict=raw_area)
        areas = {}
        for area in areas_list:
            areas[area.name] = area
            if area.toplevel_alias is not None:
                self.parent_area[area.toplevel_alias] = area

        assert not EXTENDED_ITEM.complete
        EXTENDED_ITEM.items_list.extend(events)
        for area in areas_list:
            if area.allowed_time_of_day == Both:
                EXTENDED_ITEM.items_list.append(make_day(area.name))
                EXTENDED_ITEM.items_list.append(make_night(area.name))
            else:
                EXTENDED_ITEM.items_list.append(EIN(area.name))

        global map_exit_suffixes
        map_exit_suffixes = {}
        map_exits_entrances: dict[str, str] = {"Exit": "Entrance"}
        for exit_full_name in map_exits:
            exit_name = exit_full_name.rsplit(" - ", 1)[-1]
            map_exit_suffixes[exit_name] = False
            if exit_name.endswith(" Exit"):
                map_exit_suffixes[exit_name[: -len(" Exit")]] = True
                if (
                    entrance_full_name := exit_full_name.replace("Exit", "Entrance")
                ) in map_entrances:
                    entrance_name = entrance_full_name.rsplit(" - ", 1)[-1]
                    map_exits_entrances[exit_name] = entrance_name
            if "Exit to " in exit_name:
                if (
                    entrance_full_name := exit_full_name.replace(
                        "Exit to", "Entrance from"
                    )
                ) in map_entrances:
                    entrance_name = entrance_full_name.rsplit(" - ", 1)[-1]
                    map_exits_entrances[exit_name] = entrance_name

        map_entrances_suffixes = {
            entrance_name.rsplit(" - ", 1)[-1] for entrance_name in map_entrances
        }

        def fexit(prefix, k, v):
            v = v.localize(lambda text: self.search(prefix, text))
            if k in map_entrances_suffixes:
                return (None, k)
            if k not in map_exit_suffixes:
                return ((self.search(prefix, k), v), None)
            if map_exit_suffixes[k]:
                k = k + " Exit"
            if k in map_exits_entrances:
                return ((k, v), map_exits_entrances[k])
            else:
                return ((k, v), None)

        self.parent_area.map(
            lambda prefix, k, v: (
                self.search(prefix, k) if " - " in k else k,
                v.localize(lambda text: self.search(prefix, text)),
            ),
            fexit,
        )

        self.areas: Dict[str, Area[DNFInventory]] = areas

        self.short_full: List[Tuple[str, EXTENDED_ITEM_NAME]] = [("", EIN(""))]
        self.entrance_allowed_time_of_day = {}
        self.checks = {}
        self.gossip_stones = {}
        self.events = {}
        self.map_exits = {}
        self.map_entrances = {}

        for partial_address in checks:
            full_address = self.search("", partial_address)
            area_name, suffix = full_address.rsplit("\\", 1)
            self.short_full.append((partial_address, full_address))
            check = checks[partial_address]
            check["req_index"] = EXTENDED_ITEM[full_address]
            check["short_name"] = partial_address
            hint_region = self.areas[area_name].hint_region
            assert hint_region is not None
            check["hint_region"] = hint_region
            self.checks[full_address] = check

        for partial_address in gossip_stones:
            full_address = self.search("", partial_address)
            self.short_full.append((partial_address, full_address))
            stone = gossip_stones[partial_address]
            stone["req_index"] = EXTENDED_ITEM[full_address]
            stone["short_name"] = partial_address
            self.gossip_stones[full_address] = stone

        for event in events:
            if event in self.checks or event in self.gossip_stones:
                continue
            self.events[event] = {"req_index": EXTENDED_ITEM[event]}

        for partial_address in map_exits:
            full_address = self.search("", partial_address)
            self.short_full.append((partial_address, full_address))
            EXTENDED_ITEM.items_list.append(full_address)
            exit = map_exits[partial_address]
            exit["req_index"] = len(EXTENDED_ITEM.items_list) - 1
            exit["short_name"] = partial_address
            self.map_exits[full_address] = exit

        for partial_address in map_entrances:
            full_address = self.search("", partial_address)
            area_name, suffix = full_address.rsplit("\\", 1)
            entrance = map_entrances[partial_address]
            allowed_time_of_day_str = entrance.get("allowed-time-of-day", None)
            allowed_time_of_day = (
                AllowedTimeOfDay[allowed_time_of_day_str]
                if allowed_time_of_day_str is not None
                else self.areas[area_name].allowed_time_of_day
            )
            entrance["allowed_time_of_day"] = allowed_time_of_day
            entrance["req_index"] = len(EXTENDED_ITEM.items_list)
            self.entrance_allowed_time_of_day[full_address] = allowed_time_of_day
            if allowed_time_of_day == Both:
                EXTENDED_ITEM.items_list.append(make_day(full_address))
                EXTENDED_ITEM.items_list.append(make_night(full_address))
            else:
                EXTENDED_ITEM.items_list.append(full_address)

            entrance["short_name"] = partial_address
            entrance["hint_region"] = self.areas[area_name].hint_region
            self.map_entrances[full_address] = entrance

        EXTENDED_ITEM.complete = True

        def short_to_full(elt: str):
            if elt in LOGIC_OPTIONS or "Trick" in elt:
                return EIN(elt)
            for tag in ["_DAY", "_NIGHT"]:
                if elt[-len(tag) :] == tag:
                    return EIN(short_to_full(elt[: -len(tag)]) + tag)
            for a, b in self.short_full:
                if a == elt:
                    return b
            b = self.search("", elt)
            self.short_full.append((elt, b))
            return b

        def full_to_short(elt: EXTENDED_ITEM_NAME):
            for a, b in self.short_full:
                if b == elt:
                    return a
            raise ValueError(f"Error: association list, cannot find {elt}.")

        self.short_to_full = short_to_full
        self.full_to_short = full_to_short

        self.exit_to_area = {}

        self.requirements = [DNFInventory() for _ in EXTENDED_ITEM.items()]
        self.opaque = [True for _ in EXTENDED_ITEM.items()]

        reqs = self.requirements  # Local alias
        DNFInv = DNFInventory

        for area_name, area in self.areas.items():
            if area.can_sleep:
                # If one day we allow sleeping to be randomized, change the following to regular connections
                assert area.allowed_time_of_day == Both
                darea_bit = EXTENDED_ITEM[make_day(area_name)]
                narea_bit = EXTENDED_ITEM[make_night(area_name)]
                self.opaque[darea_bit] = False
                self.opaque[narea_bit] = False
                reqs[darea_bit] |= DNFInv(narea_bit)
                reqs[narea_bit] |= DNFInv(darea_bit)

            for loc, req in area.locations.items():
                if area.abstract:
                    timed_req = req
                elif area.allowed_time_of_day == Both:
                    timed_req = (req.day_only() & DNFInv(make_day(area_name))) | (
                        req.night_only() & DNFInv(make_night(area_name))
                    )
                elif area.allowed_time_of_day == DayOnly:
                    timed_req = req.day_only() & DNFInv(EIN(area_name))
                else:
                    timed_req = req.night_only() & DNFInv(EIN(area_name))
                full_loc = with_sep_full(area_name, loc)
                loc_bit = EXTENDED_ITEM[full_loc]

                reqs[loc_bit] |= timed_req
                self.opaque[loc_bit] = req.opaque

            for exit, req in area.exits.items():
                if exit in self.areas:  # Logical exit, the name is the area
                    area_dest = self.areas[exit]
                    if area_dest.allowed_time_of_day == Both:
                        darea_bit = EXTENDED_ITEM[make_day(area_dest.name)]
                        narea_bit = EXTENDED_ITEM[make_night(area_dest.name)]
                        self.opaque[darea_bit] = False
                        self.opaque[narea_bit] = False

                        if area.allowed_time_of_day == Both:
                            reqs[darea_bit] |= req.day_only() & DNFInv(
                                make_day(area_name)
                            )
                            reqs[narea_bit] |= req.night_only() & DNFInv(
                                make_night(area_name)
                            )
                        elif area.allowed_time_of_day == DayOnly:
                            reqs[darea_bit] |= req.day_only() & DNFInv(EIN(area_name))
                        elif area.allowed_time_of_day == NightOnly:
                            reqs[narea_bit] |= req.night_only() & DNFInv(EIN(area_name))
                    else:
                        area_bit = EXTENDED_ITEM[area_dest.name]
                        self.opaque[area_bit] = False
                        if area_dest.allowed_time_of_day == DayOnly:
                            timed_req = req.day_only()
                            timed_area = make_day(area_name)
                        else:
                            timed_req = req.night_only()
                            timed_area = make_night(area_name)
                        if area.allowed_time_of_day == Both:
                            reqs[area_bit] |= timed_req & DNFInv(timed_area)
                        elif area.allowed_time_of_day == area_dest.allowed_time_of_day:
                            reqs[area_bit] |= timed_req & DNFInv(EIN(area_name))
                        else:
                            raise ValueError("Time makes this exit impossible.")

                else:  # Map exit
                    exit_full = with_sep_full(area_name, exit)
                    exit_bit = EXTENDED_ITEM[exit_full]
                    self.opaque[exit_bit] = False
                    self.exit_to_area[exit_full] = area
                    if area.abstract:
                        assert exit == START
                        reqs[exit_bit] = req
                    elif area.allowed_time_of_day == Both:
                        reqs[exit_bit] |= req.day_only() & DNFInv(make_day(area_name))
                        reqs[exit_bit] |= req.night_only() & DNFInv(
                            make_night(area_name)
                        )
                    elif area.allowed_time_of_day == DayOnly:
                        reqs[exit_bit] |= req.day_only() & DNFInv(EIN(area_name))
                    elif area.allowed_time_of_day == NightOnly:
                        reqs[exit_bit] |= req.night_only() & DNFInv(EIN(area_name))
                    else:
                        assert False

            for entrance in area.entrances.keys():
                entrance = with_sep_full(area_name, entrance)
                allowed_time_of_day = self.entrance_allowed_time_of_day[entrance]
                if allowed_time_of_day == Both:
                    darea_bit = EXTENDED_ITEM[make_day(area_name)]
                    narea_bit = EXTENDED_ITEM[make_night(area_name)]
                    self.opaque[darea_bit] = False
                    self.opaque[narea_bit] = False
                    reqs[darea_bit] |= DNFInv(make_day(entrance))
                    reqs[narea_bit] |= DNFInv(make_night(entrance))
                else:
                    if area.allowed_time_of_day == Both:
                        if allowed_time_of_day == DayOnly:
                            area_bit = EXTENDED_ITEM[make_day(area_name)]
                        else:
                            area_bit = EXTENDED_ITEM[make_night(area_name)]
                    else:
                        area_bit = EXTENDED_ITEM[area_name]
                    self.opaque[area_bit] = False
                    reqs[area_bit] |= DNFInv(entrance)

    def to_dict(self):
        def filter_values(data: Dict[str, dict], keys: List[str]):
            return dict(
                {
                    id: dict({k: v for k, v in value.items() if k in keys})
                    for id, value in data.items()
                }
            )

        return {
            "items": EXTENDED_ITEM.items_list,
            "areas": self.parent_area,
            "checks": filter_values(
                self.checks, ["short_name", "type", "original item"]
            ),
            "gossip_stones": dict(
                {k: v["short_name"] for k, v in self.gossip_stones.items()}
            ),
            # NB "stage" should not really be needed in downstream consumers but it controls
            # whether exits/entrances are available in Entrance Randomizer
            "exits": filter_values(
                self.map_exits,
                [
                    "type",
                    "vanilla",
                    "allowed_time_of_day",
                    "subtype",
                    "stage",
                    "short_name",
                    "pillar-province",
                ],
            ),
            "entrances": filter_values(
                self.map_entrances,
                [
                    "type",
                    "can-start-at",
                    "allowed_time_of_day",
                    "subtype",
                    "stage",
                    "province",
                    "short_name",
                ],
            ),
        }

    def __str__(self):
        return f"{EXTENDED_ITEM.items_list}\n{self.parent_area}\n{self.checks}\n{self.gossip_stones}\n{self.map_exits}\n{self.map_entrances}\n"


yaml.add_representer(
    Area,
    lambda dumper, data: dumper.represent_dict(
        {
            "abstract": data.abstract,
            "allowed_time_of_day": data.allowed_time_of_day,
            "can_save": data.can_save,
            "can_sleep": data.can_sleep,
            "entrances": list(data.entrances.keys()),
            "exits": data.exits,
            "hint_region": data.hint_region,
            "locations": data.locations,
            "name": data.name,
            "sub_areas": data.sub_areas,
            "toplevel_alias": data.toplevel_alias,
        }
    ),
)
