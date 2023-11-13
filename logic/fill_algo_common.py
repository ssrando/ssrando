from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Callable

from .constants import EXTENDED_ITEM_NAME
from .inventory import Inventory


@dataclass
class RandomizationSettings:
    must_be_placed_items: Dict[EXTENDED_ITEM_NAME, None]
    may_be_placed_items: Dict[EXTENDED_ITEM_NAME, None]
    duplicable_items: Dict[str, None]
    check_bits: Inventory


@dataclass
class UserOutput:
    GenerationFailed: Callable[[str], Exception]
    progress_callback: Callable[[str], None]
