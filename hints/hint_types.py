from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from logic.logic import Logic


@dataclass
class Hint:
    hint_type: str

    def __init__(self) -> None:
        raise NotImplementedError("abstract")

    def to_ingame_text(self) -> List[str]:
        """each string in the list appear in a separate textbox and will be line broken"""
        raise NotImplementedError("abstract")

    def to_spoiler_log_text(self) -> str:
        raise NotImplementedError("abstract")

    def to_spoiler_log_json(self):
        raise NotImplementedError("abstract")


@dataclass
class SongHint(Hint):
    hint_type: str = field(init=False)
    songhintname: str
    item: str

    def to_text(self) -> str:
        raise NotImplementedError("abstract")

    def to_ingame_text(self) -> List[str]:
        return [self.to_text()]

    def to_spoiler_log_text(self) -> str:
        return f"{self.to_ingame_text()} [{self.item}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.songhintname,
            "item": self.item,
            "type": self.hint_type,
        }


@dataclass
class SongEmptyHint(SongHint):
    hint_type = "song-empty"
    text = ""

    def to_text(self):
        return self.text


@dataclass
class SongDirectHint(SongHint):
    hint_type = "song-direct"
    text = "This trial holds {}"

    def to_text(self):
        return self.text.format(self.item)


@dataclass
class SongUselessHint(SongHint):
    hint_type = "song-useless"
    text = "It's probably not too important..."

    def to_text(self):
        return self.text


@dataclass
class SongUsefulHint(SongHint):
    hint_type = "song-useful"
    text = "You might need what it reveals..."

    def to_text(self):
        return self.text


@dataclass
class SongRequiredHint(SongHint):
    hint_type = "song-required"
    text = "Your spirit will grow by completing this trial"

    def to_text(self):
        return self.text


@dataclass
class GossipStoneHint(Hint):
    hint_type: str

    def to_text(self) -> str:
        raise NotImplementedError("abstract")

    def to_ingame_text(self) -> List[str]:
        return [self.to_text()]

    def __hash__(self):
        raise NotImplementedError("abstract")


@dataclass
class GossipStoneHintWrapper:
    hints: List[GossipStoneHint]

    def to_ingame_text(self) -> List[str]:
        return [hint_txt for hint in self.hints for hint_txt in hint.to_ingame_text()]

    def to_spoiler_log_json(self):
        return [hint.to_spoiler_log_json() for hint in self.hints]


@dataclass
class LocationGossipStoneHint(GossipStoneHint):
    location: str
    item: str
    location_name_override: Optional[str] = None

    def to_text(self) -> str:
        if override := self.location_name_override:
            return f"They say that {override} <y<{self.item}>>"

        zone, specific_loc = Logic.split_location_name_by_zone(self.location)
        return f"They say that <r<{zone}: {specific_loc}>> has <y<{self.item}>>"

    def to_spoiler_log_text(self) -> str:
        return f"{self.location} has {self.item} [{self.hint_type}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "nameoverride": self.location_name_override,
            "item": self.item,
            "type": self.hint_type,
        }

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class TrialGateGossipStoneHint(LocationGossipStoneHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False, default="trial")
    trial_gate: str

    def to_text(self) -> str:
        return f"They say that opening the <r<{self.trial_gate}>> will reveal <y<{self.item}>>"

    def to_spoiler_log_text(self) -> str:
        return f"{self.trial_gate} has {self.item}"

    def to_spoiler_log_json(self):
        return {
            "location": self.trial_gate,
            "item": self.item,
            "type": self.hint_type,
        }

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class ZoneItemGossipStoneHint(LocationGossipStoneHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False, default="zone_item")
    zone_override: str

    def to_text(self) -> str:
        return f"<y<{self.item}>> can be found in <r<{self.zone_override}>>"

    def to_spoiler_log_text(self) -> str:
        return f"{self.item} is in {self.zone_override} [{self.hint_type}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "item": self.item,
            "type": self.hint_type,
            "zone": self.zone_override,
        }

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class SotsGoalGossipStoneHint(LocationGossipStoneHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False)
    zone: str
    goal: str | None = None

    def __post_init__(self):
        self.hint_type = "sots" if self.goal is None else "goal"

    def to_text(self) -> str:
        if self.goal is not None:
            return f"The servant of the goddess who wishes to vanquish <ye<{self.goal}>> shall venture to <r<{self.zone}>>"

        return f"The <b+<Spirit of the Sword>> guides the goddess' chosen hero to <r<{self.zone}>>"

    def to_spoiler_log_text(self) -> str:
        if self.goal is not None:
            return f"{self.zone} is on the path to {self.goal} [{self.item}]"
        return f"{self.zone} is SotS [{self.item}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "item": self.item,
            "zone": self.zone,
            "goal": self.goal,
            "type": self.hint_type,
        }

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class CubeSotsGoalGossipStoneHint(LocationGossipStoneHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False)
    cube_zone: str
    goal: str | None = None

    def __post_init__(self):
        self.hint_type = "cube_sots" if self.goal is None else "cube_goal"

    def to_text(self) -> str:
        if self.goal is not None:
            return f"The servant of the goddess who wishes to vanquish <ye<{self.goal}>> shall unite <r<{self.cube_zone}>> with the skies."

        return f"The <ye<goddess>> left a sacred gift for the hero who unites <r<{self.cube_zone}>> with the skies."

    def to_spoiler_log_text(self) -> str:
        if goal := self.goal:
            return f"a cube in {self.cube_zone} is on the path to {goal} [{self.item}]"
        return f"{self.cube_zone} has a SotS cube [{self.item}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "item": self.item,
            "cube_zone": self.cube_zone,
            "goal": self.goal,
            "type": self.hint_type,
        }

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class BarrenGossipStoneHint(GossipStoneHint):
    hint_type: str = field(init=False, default="barren")
    zone: str

    def to_text(self) -> str:
        return f"They say that those who travel to <r<{self.zone}>> will never find anything for their quest"

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is barren"

    def to_spoiler_log_json(self):
        return {"zone": self.zone, "type": self.hint_type}

    def __hash__(self):
        return hash(self.zone)


@dataclass
class EmptyGossipStoneHint(GossipStoneHint):
    hint_type: str = field(init=False, default="junk")
    text: str

    def to_text(self) -> str:
        return self.text

    def to_spoiler_log_text(self) -> str:
        return self.text

    def to_spoiler_log_json(self):
        return {"text": self.text, "type": self.hint_type}

    def __hash__(self):
        return hash(self.text)
