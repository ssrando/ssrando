from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from logic.constants import EXTENDED_ITEM_NAME


@dataclass
class Hint:
    hint_type: str

    def __init__(self) -> None:
        raise NotImplementedError("abstract")

    def to_ingame_text(self, norm) -> List[str]:
        """each string in the list appear in a separate textbox and will be line broken"""
        raise NotImplementedError("abstract")

    def to_ingame_stone_text(self, norm) -> List[str]:
        """each string in the list appear in a separate textbox and will be line broken"""
        raise NotImplementedError("abstract")

    def to_ingame_fi_text(self, norm) -> List[str]:
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
    importance: Enum

    base_type: str = field(init=False)
    raw_texts: dict[Enum, str] = field(init=False)

    def __init__(self):
        raise NotImplementedError("abstract")

    def __post_init__(self):
        self.hint_type = f"{self.base_type}-{hint_types[self.hint_mode]}"

    def to_text(self, norm, include_color=False) -> str:
        if self.hint_mode == HINT_MODES.Direct:
            return self.raw_texts[self.hint_mode].format(
                norm(self.item), format_importance(self.importance, include_color)
            )
        return self.raw_texts[self.hint_mode]

    def to_ingame_text(self, norm) -> List[str]:
        return [self.to_text(norm, True)]

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
        HINT_MODES.Direct: "This trial holds {}{}.",
        HINT_MODES.Useless: "Its reward is probably not too important...",
        HINT_MODES.Useful: "You might need its reward...",
        HINT_MODES.Required: "Your spirit will grow by completing this trial.",
    }


@dataclass
class RegularHint(Hint):
    hint_type: str

    def to_stone_text(self, norm) -> str:
        raise NotImplementedError("abstract")

    def to_fi_text(self, norm) -> str:
        raise NotImplementedError("abstract")

    def to_ingame_stone_text(self, norm) -> List[str]:
        return [self.to_stone_text(norm)]

    def to_ingame_fi_text(self, norm) -> List[str]:
        return [self.to_fi_text(norm)]


@dataclass
class GossipStoneHintWrapper:
    hints: List[RegularHint]

    def to_ingame_text(self, norm) -> List[str]:
        return [
            hint_txt
            for hint in self.hints
            for hint_txt in hint.to_ingame_stone_text(norm)
        ]

    def to_spoiler_log_json(self):
        return [hint.to_spoiler_log_json() for hint in self.hints]


@dataclass
class LocationHint(RegularHint):
    location: EXTENDED_ITEM_NAME
    item: EXTENDED_ITEM_NAME
    importance: Enum
    location_name_override: Optional[str] = None

    def to_stone_text(self, norm) -> str:
        if override := self.location_name_override:
            return f"They say that {override} <y<{norm(self.item)}>>{format_importance(self.importance, True)}."

        return f"They say that <r<{norm(self.location)}>> has <y<{norm(self.item)}>>{format_importance(self.importance, True)}."

    def to_fi_text(self, norm) -> str:
        if override := self.location_name_override:
            return f"My readings suggest that {override} <y<{norm(self.item)}>>{format_importance(self.importance, True)}."

        return f"My readings suggest that <r<{norm(self.location)}>> has <y<{norm(self.item)}>>."

    def to_spoiler_log_text(self, norm) -> str:
        return f"{norm(self.location)} has {self.item}{format_importance(self.importance)} [{self.hint_type}]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "nameoverride": self.location_name_override,
            "item": self.item,
            "type": self.hint_type,
        }


@dataclass
class TrialGateHint(LocationHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False, default="trial")
    trial_gate: str

    def to_stone_text(self, norm) -> str:
        return f"They say that opening the <r<{norm(self.trial_gate)}>> will reveal <y<{norm(self.item)}>>{format_importance(self.importance, True)}."

    def to_fi_text(self, norm) -> str:
        return f"My readings indicate that opening the <r<{norm(self.trial_gate)}>> will reveal <y<{norm(self.item)}>>{format_importance(self.importance, True)}."

    def to_spoiler_log_text(self, norm) -> str:
        return f"{self.trial_gate} has {self.item}{format_importance(self.importance)}"

    def to_spoiler_log_json(self):
        return {
            "location": self.trial_gate,
            "item": self.item,
            "type": self.hint_type,
        }


@dataclass
class ZoneItemHint(LocationHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False, default="zone_item")
    zone_override: str

    def to_stone_text(self, norm) -> str:
        return f"<y<{norm(self.item)}>>{format_importance(self.importance, True)} can be found in <r<{self.zone_override}>>."

    def to_fi_text(self, norm) -> str:
        return f"I detect signals relating to <y<{norm(self.item)}>>{format_importance(self.importance, True)} in <r<{self.zone_override}>>."

    def to_spoiler_log_text(self, norm) -> str:
        return f"{self.item}{format_importance(self.importance)} is in {self.zone_override} [zone]"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "item": self.item,
            "type": self.hint_type,
            "zone": self.zone_override,
        }


@dataclass
class SotsGoalHint(LocationHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False)
    zone: str
    goal: str | None = None

    def __post_init__(self):
        self.hint_type = "sots" if self.goal is None else "goal"

    def to_stone_text(self, norm) -> str:
        if self.goal is not None:
            return f"The servant of the goddess who wishes to vanquish <ye<{self.goal}>> shall venture to <r<{self.zone}>>."

        return f"The <b+<Spirit of the Sword>> guides the goddess' chosen hero to <r<{self.zone}>>."

    def to_fi_text(self, norm) -> str:
        if self.goal is not None:
            return f"I conjecture that travelling to <r<{self.zone}>> will help you defeat <ye<{self.goal}>>."

        return (
            f"I recommend travelling to <r<{self.zone}>> to <b+<fulfill your destiny>>."
        )

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
class CubeSotsGoalHint(LocationHint):
    location_name_override: Optional[str] = field(default=None, init=False)
    hint_type: str = field(init=False)
    cube_zone: str
    goal: str | None = None

    def __post_init__(self):
        self.hint_type = "cube_sots" if self.goal is None else "cube_goal"

    def to_stone_text(self, norm) -> str:
        if self.goal is not None:
            return f"The servant of the goddess who wishes to vanquish <ye<{self.goal}>> shall unite <r<{self.cube_zone}>> with the skies."

        return f"The <ye<goddess>> left a sacred gift for the hero who unites <r<{self.cube_zone}>> with the skies."

    def to_fi_text(self, norm) -> str:
        if self.goal is not None:
            return f"I conjecture that uniting <r<{self.cube_zone}>> with the skies will help you defeat <ye<{self.goal}>>."

        return f"I recommend uniting <r<{self.cube_zone}>> with the skies to <ye<fulfill your destiny>>."

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
class BarrenHint(RegularHint):
    hint_type: str = field(init=False, default="barren")
    zone: str

    def to_stone_text(self, norm) -> str:
        return f"They say that those who travel to <r<{self.zone}>> will never find anything for their quest."

    def to_fi_text(self, norm) -> str:
        return f"I detect no significant readings in <r<{self.zone}>>."

    def to_spoiler_log_text(self, norm) -> str:
        return f"{self.zone} is barren"

    def to_spoiler_log_json(self):
        return {"zone": self.zone, "type": self.hint_type}


@dataclass
class EmptyHint(RegularHint):
    hint_type: str = field(init=False, default="junk")
    text: str

    def to_stone_text(self, norm) -> str:
        return self.text

    def to_fi_text(self, norm) -> str:
        return self.text

    def to_spoiler_log_text(self, norm) -> str:
        return self.text

    def to_spoiler_log_json(self):
        return {"text": self.text, "type": self.hint_type}


class FiHintWrapper(GossipStoneHintWrapper):
    hints: List[RegularHint]

    def __init__(self, hints):
        def hint_order(hint):
            if isinstance(hint, SotsGoalHint):
                return 0
            if isinstance(hint, CubeSotsGoalHint):
                return 1
            if isinstance(hint, BarrenHint):
                return 2
            if isinstance(hint, ZoneItemHint):
                return 3
            if isinstance(hint, LocationHint):
                if hint.hint_type == "always":
                    return 4
                if hint.hint_type == "sometimes":
                    return 5
                return 6
            return 7

        self.hints = sorted(hints, key=hint_order)

    def to_ingame_text(self, norm) -> List[str]:
        return [
            hint_txt for hint in self.hints for hint_txt in hint.to_ingame_fi_text(norm)
        ]


HINT_IMPORTANCE = Enum(
    "HINT_IMPORTANCE", ["Required", "PossiblyRequired", "NotRequired", "Null"]
)


def format_importance(importance: Enum, include_color=False) -> str:
    match importance:
        case HINT_IMPORTANCE.Required:
            if include_color:
                return " (<g+<required>>)"
            else:
                return " (required)"
        case HINT_IMPORTANCE.PossiblyRequired:
            if include_color:
                return " (<ye<possibly required>>)"
            else:
                return " (possibly required)"
        case HINT_IMPORTANCE.NotRequired:
            if include_color:
                return " (<blk<not required>>)"
            else:
                return " (not required)"
        case HINT_IMPORTANCE.Null:
            return ""
