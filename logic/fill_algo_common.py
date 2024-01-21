from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Callable

from .constants import EXTENDED_ITEM_NAME


@dataclass
class RandomizationSettings:
    must_be_placed_items: Dict[EXTENDED_ITEM_NAME, None]
    may_be_placed_items: Dict[EXTENDED_ITEM_NAME, None]
    duplicable_items: Dict[str, None]
    restricted_vanilla_items: list[EXTENDED_ITEM_NAME]
    restricted_non_vanilla_items: list[EXTENDED_ITEM_NAME]


@dataclass
class UserOutput:
    GenerationFailed: Callable[[str], Exception]
    progress_callback: Callable[[str], None]
