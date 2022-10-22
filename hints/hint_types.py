from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from graph_logic.constants import EXTENDED_ITEM_NAME


@dataclass
class Hint:
    hint_type: str

    def __init__(self) -> None:
        raise NotImplementedError("abstract")

    def to_ingame_text(self, norm) -> List[str]:
        """each string in the list appear in a separate textbox and will be line broken"""
        raise NotImplementedError("abstract")

    def to_spoiler_log_text(self, norm) -> str:
        raise NotImplementedError("abstract")

    def to_spoiler_log_json(self):
        raise NotImplementedError("abstract")


HINT_MODES = Enum("HINT_MODES", ["Empty", "Direct", "Useless", "Useful", "Required"])

hint_types = {
    HINT_MODES.Empty: "empty",
    HINT_MODES.Direct: "direct",
    HINT_MODES.Useless: "useless",
    HINT_MODES.Useful: "useful",
    HINT_MODES.Required: "required",
}


@dataclass
class NonStoneHint(Hint):
    hint_type: str = field(init=False)
    hint_mode: Enum
    songhintname: str
    item: str

    base_type: str = field(init=False)
    raw_texts: dict[Enum, str] = field(init=False)

    def __init__(self):
        raise NotImplementedError("abstract")

    def __post_init__(self):
        self.hint_type = f"{self.base_type}-{hint_types[self.hint_mode]}"

    def to_text(self, norm) -> str:
        if self.hint_mode == HINT_MODES.Direct:
            return self.raw_texts[self.hint_mode].format(norm(self.item))
        return self.raw_texts[self.hint_mode]

    def to_ingame_text(self, norm) -> List[str]:
        return [self.to_text(norm)]

    def to_spoiler_log_text(self, norm) -> str:
        return f"{self.to_text(norm)} [{self.item}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.songhintname,
            "item": self.item,
            "type": self.hint_type,
        }


@dataclass
class SongHint(NonStoneHint):
    base_type = "song"
    raw_texts = {
        HINT_MODES.Empty: "",
        HINT_MODES.Direct: "This trial holds {}",
        HINT_MODES.Useless: "It's probably not too important...",
        HINT_MODES.Useful: "You might need what it reveals...",
        HINT_MODES.Required: "Your spirit will grow by completing this trial",
    }


@dataclass
class GossipStoneHint(Hint):
    hint_type: str

    def to_text(self, norm) -> str:
        raise NotImplementedError("abstract")

    def to_ingame_text(self, norm) -> List[str]:
        return [self.to_text(norm)]


@dataclass
class GossipStoneHintWrapper:
    hints: List[GossipStoneHint]

    def to_ingame_text(self, norm) -> List[str]:
        return [
            hint_txt for hint in self.hints for hint_txt in hint.to_ingame_text(norm)
        ]

    def to_spoiler_log_json(self):
        return [hint.to_spoiler_log_json() for hint in self.hints]


@dataclass
class LocationGossipStoneHint(GossipStoneHint):
    location: EXTENDED_ITEM_NAME
    item: EXTENDED_ITEM_NAME
    location_name_override: Optional[str] = None

    def to_text(self, norm) -> str:
        if override := self.location_name_override:
            return f"They say that {override} <y<{norm(self.item)}>>"

        return f"They say that <r<{norm(self.location)}>> has <y<{norm(self.item)}>>"

    def to_spoiler_log_text(self, norm) -> str:
        return f"{norm(self.location)} has {self.item} [{self.hint_type}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "nameoverride": self.location_name_override,
            "item": self.item,
            "type": self.hint_type,
        }


@dataclass
class TrialGateGossipStoneHint(LocationGossipStoneHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False, default="trial")
    trial_gate: str

    def to_text(self, norm) -> str:
        return f"They say that opening the <r<{norm(self.trial_gate)}>> will reveal <y<{norm(self.item)}>>"

    def to_spoiler_log_text(self, norm) -> str:
        return f"{self.trial_gate} has {self.item}"

    def to_spoiler_log_json(self):
        return {
            "location": self.trial_gate,
            "item": self.item,
            "type": self.hint_type,
        }


@dataclass
class ZoneItemGossipStoneHint(LocationGossipStoneHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False, default="zone_item")
    zone_override: str

    def to_text(self, norm) -> str:
        return f"<y<{norm(self.item)}>> can be found in <r<{self.zone_override}>>"

    def to_spoiler_log_text(self, norm) -> str:
        return f"{self.item} is in {self.zone_override} [zone]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "item": self.item,
            "type": self.hint_type,
            "zone": self.zone_override,
        }


@dataclass
class SotsGoalGossipStoneHint(LocationGossipStoneHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False)
    zone: str
    goal: str | None = None

    def __post_init__(self):
        self.hint_type = "sots" if self.goal is None else "goal"

    def to_text(self, norm) -> str:
        if self.goal is not None:
            return f"The servant of the goddess who wishes to vanquish <ye<{self.goal}>> shall venture to <r<{self.zone}>>"

        return f"The <b+<Spirit of the Sword>> guides the goddess' chosen hero to <r<{self.zone}>>"

    def to_spoiler_log_text(self, norm) -> str:
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


@dataclass
class CubeSotsGoalGossipStoneHint(LocationGossipStoneHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False)
    cube_zone: str
    goal: str | None = None

    def __post_init__(self):
        self.hint_type = "cube_sots" if self.goal is None else "cube_goal"

    def to_text(self, norm) -> str:
        if self.goal is not None:
            return f"The servant of the goddess who wishes to vanquish <ye<{self.goal}>> shall unite <r<{self.cube_zone}>> with the skies."

        return f"The <ye<goddess>> left a sacred gift for the hero who unites <r<{self.cube_zone}>> with the skies."

    def to_spoiler_log_text(self, norm) -> str:
        if self.goal is not None:
            return f"a cube in {self.cube_zone} is on the path to {self.goal} [{self.item}]"
        return f"{self.cube_zone} has a SotS cube [{self.item}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "item": self.item,
            "cube_zone": self.cube_zone,
            "goal": self.goal,
            "type": self.hint_type,
        }


@dataclass
class BarrenGossipStoneHint(GossipStoneHint):
    hint_type: str = field(init=False, default="barren")
    zone: str

    def to_text(self, norm) -> str:
        return f"They say that those who travel to <r<{self.zone}>> will never find anything for their quest"

    def to_spoiler_log_text(self, norm) -> str:
        return f"{self.zone} is barren"

    def to_spoiler_log_json(self):
        return {"zone": self.zone, "type": self.hint_type}


@dataclass
class EmptyGossipStoneHint(GossipStoneHint):
    hint_type: str = field(init=False, default="junk")
    text: str

    def to_text(self, norm) -> str:
        return self.text

    def to_spoiler_log_text(self, norm) -> str:
        return self.text

    def to_spoiler_log_json(self):
        return {"text": self.text, "type": self.hint_type}
