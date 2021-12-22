from dataclasses import dataclass
from typing import List


class GossipStoneHint:
    def to_gossip_stone_text(self) -> List[str]:
        """each string in the list appear in a separate textbox and will be line broken"""
        raise NotImplementedError("abstract")

    def to_spoiler_log_text(self) -> str:
        raise NotImplementedError("abstract")


@dataclass
class GossipStoneHintWrapper(GossipStoneHint):
    primary_hint: GossipStoneHint
    secondary_hint: GossipStoneHint

    def to_gossip_stone_text(self) -> List[str]:
        primary_text = self.primary_hint.to_gossip_stone_text()
        secondary_text = self.secondary_hint.to_gossip_stone_text()
        return [*primary_text, *secondary_text]

    def to_spoiler_log_text(self) -> str:
        return f"{self.primary_hint.to_spoiler_log_text()} / {self.secondary_hint.to_spoiler_log_text()}"


@dataclass
class TrialGateGossipStoneHint(GossipStoneHint):
    trial_gate: str
    trial_item: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"They say that opening the <r<{self.trial_gate}>> will reveal <y<{self.trial_item}>>"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.trial_gate} has {self.trial_item}"


@dataclass
class LocationGossipStoneHint(GossipStoneHint):
    location_string: str
    item: str

    def to_gossip_stone_text(self) -> List[str]:
        return [f"They say that {self.location_string} <y<{self.item}>>"]

    def to_spoiler_log_text(self) -> str:
        return f"{self.location_string} has {self.item}"


@dataclass
class ItemGossipStoneHint(GossipStoneHint):
    location_name: str
    item: str

    def to_gossip_stone_text(self) -> List[str]:
        zone, specific_loc = Logic.split_location_name_by_zone(self.location_name)
        return [f"<y<{self.item}>> can be found at <r<{zone}: {specific_loc}>>"]

    def to_spoiler_log_text(self) -> str:
        return f"{self.item} is on {self.location_name}"


@dataclass
class WayOfTheHeroGossipStoneHint(GossipStoneHint):
    zone: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"The <b+<Spirit of the Sword>> guides the goddess' chosen hero to <r<{self.zone}>>"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is SotS"


@dataclass
class BarrenGossipStoneHint(GossipStoneHint):
    zone: str

    def to_gossip_stone_text(self) -> List[str]:
        return [
            f"They say that those who travel to <r<{self.zone}>> will never find anything for their quest"
        ]

    def to_spoiler_log_text(self) -> str:
        return f"{self.zone} is barren"


@dataclass
class EmptyGossipStoneHint(GossipStoneHint):
    text: str

    def to_gossip_stone_text(self) -> List[str]:
        return [self.text]

    def to_spoiler_log_text(self) -> str:
        return self.text
