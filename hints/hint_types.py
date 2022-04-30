from dataclasses import dataclass
from re import S
from typing import List

from logic.logic import Logic


@dataclass
class GossipStoneHint:
    location: str
    item: str
    needs_logic: bool

    def to_gossip_stone_text(self) -> List[str]:
        """each string in the list appear in a separate textbox and will be line broken"""
        raise NotImplementedError("abstract")

    def to_spoiler_log_text(self) -> str:
        raise NotImplementedError("abstract")

    def to_spoiler_log_json(self):
        raise NotImplementedError("abstract")

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class GossipStoneHintWrapper:
    primary_hint: GossipStoneHint
    secondary_hint: GossipStoneHint

    def to_gossip_stone_text(self) -> List[str]:
        primary_text = self.primary_hint.to_gossip_stone_text()
        secondary_text = self.secondary_hint.to_gossip_stone_text()
        return [*primary_text, *secondary_text]

    def to_spoiler_log_text(self) -> str:
        return f"{self.primary_hint.to_spoiler_log_text()} / {self.secondary_hint.to_spoiler_log_text()}"

    def to_spoiler_log_json(self):
        return [
            self.primary_hint.to_spoiler_log_json(),
            self.secondary_hint.to_spoiler_log_json(),
        ]


@dataclass
class TrialGateGossipStoneHint(GossipStoneHint):
    trial_gate: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"They say that opening the <r<{self.trial_gate}>> will reveal <y<{self.item}>>"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.trial_gate} has {self.item}"

    def to_spoiler_log_json(self):
        return {"location": self.trial_gate, "item": self.item, "type": "trial"}

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class LocationGossipStoneHint(GossipStoneHint):
    location_string: str

    def to_gossip_stone_text(self) -> List[str]:
        return [f"They say that {self.location_string} <y<{self.item}>>"]

    def to_spoiler_log_text(self) -> str:
        return f"{self.location_string} {self.item}"

    def to_spoiler_log_json(self):
        return {"location": self.location, "item": self.item, "type": "location"}

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class ItemGossipStoneHint(GossipStoneHint):
    def to_gossip_stone_text(self) -> List[str]:
        zone, specific_loc = Logic.split_location_name_by_zone(self.location)
        return [f"<y<{self.item}>> can be found at <r<{zone}: {specific_loc}>>"]

    def to_spoiler_log_text(self) -> str:
        return f"{self.item} is on {self.location}"

    def to_spoiler_log_json(self):
        return {"location": self.location, "item": self.item, "type": "item"}

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class SpiritOfTheSwordGossipStoneHint(GossipStoneHint):
    zone: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"The <b+<Spirit of the Sword>> guides the goddess' chosen hero to <r<{self.zone}>>"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is SotS"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "item": self.item,
            "zone": self.zone,
            "type": "sots",
        }

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class CubeSotSGossipStoneHint(GossipStoneHint):
    cube_zone: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"The <ye<goddess>> left a sacred gift for the hero who unites <r<{self.cube_zone}>> with the skies."
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.cube_zone} has a SotS cube"

    def to_spoiler_log_json(self):
        return {
            "location": self.location,
            "item": self.item,
            "cube_zone": self.cube_zone,
            "type": "cube_sots",
        }

    def __hash__(self):
        return hash(self.location + self.item)


@dataclass
class BarrenGossipStoneHint(GossipStoneHint):
    zone: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"They say that those who travel to <r<{self.zone}>> will never find anything for their quest"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is barren"

    def to_spoiler_log_json(self):
        return {"zone": self.zone, "type": "barren"}

    def __hash__(self):
        return hash(self.zone)


@dataclass
class EmptyGossipStoneHint(GossipStoneHint):
    text: str

    def to_gossip_stone_text(self) -> List[str]:
        return [f"<blk<{self.text}>>"]

    def to_spoiler_log_text(self) -> str:
        return self.text

    def to_spoiler_log_json(self):
        return {"text": self.text, "type": "junk"}

    def __hash__(self):
        return hash(self.text)
