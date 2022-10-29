from __future__ import annotations
from dataclasses import dataclass
from functools import cache
from typing import List  # Only for typing purposes

from .logic import Logic, Placement, LogicSettings
from .logic_input import Areas
from .logic_expression import DNFInventory
from .inventory import (
    Inventory,
    EXTENDED_ITEM,
    EMPTY_INV,
    EVERYTHING_BIT,
    EVERYTHING_UNBANNED_BIT,
    HINT_BYPASS_BIT,
    BANNED_BIT,
)
from .constants import *
from .placements import *
from .pools import *


def shuffle_indices(self, list, indices=None):
    if indices is None:
        return self.shuffle(list)
    else:
        n = len(indices)
        for i in range(n - 1):
            j = self.randint(i, n - 1)
            ii, jj = indices[i], indices[j]
            list[ii], list[jj] = list[jj], list[ii]
        return


@dataclass
class EROptions:
    randomize_dungeons: "None" | "Required Dungeons Separately" | "All Surface Dungeons" | "All Surface Dungeons + Sky Keep"
    randomize_trials: bool
    randomize_start_entrance: "Vanilla" | "Bird Statues" | "Any Surface Region" | "Any"
    randomize_all: "Vanilla" | "All"
    required_dungeons: List[str]
    unrequired_dungeons: List[str]
    allowed_starting_provinces: List[EIN]


class EntranceRando:
    def __init__(self, areas, rng, placement, options: EROptions):
        self.areas = areas
        self.rng = rng
        self.placement = placement
        self.options = options
        self.norm = areas.short_to_full
        return

    def randomize(self):
        if self.options.randomize_all == "All":
            self.hacky_entrance_rando()
        elif self.options.randomize_all == "Vanilla":
            self.vanilla()
        else:
            raise ValueError()
        self.randomize_dungeons_trials_starting_entrances()

    def vanilla(self):
        for exit, v in self.areas.map_exits.items():
            if (
                v["type"] == "entrance"
                or v.get("disabled", False)
                or "vanilla" not in v
            ):
                continue
            entrance = self.norm(v["vanilla"])
            self.placement.map_transitions[exit] = entrance
            self.placement.reverse_map_transitions[entrance] = exit

    def reassign_entrances(
        self, exs1: list[EIN] | list[list[EIN]], exs2: list[EIN] | list[list[EIN]]
    ):
        for ex1, ex2 in zip(exs1, exs2):
            if isinstance(ex1, str):
                ex1 = [ex1]
            if isinstance(ex2, str):
                ex2 = [ex2]
            assert ex1[0] in self.placement.map_transitions
            assert ex2[0] in self.placement.map_transitions
            en1 = EIN(entrance_of_exit(ex1[0]))
            en2 = EIN(entrance_of_exit(ex2[0]))
            for exx1 in ex1:
                self.placement.map_transitions[exx1] = en2
            for exx2 in ex2:
                self.placement.map_transitions[exx2] = en1
            self.placement.reverse_map_transitions[en1] = ex2[0]
            self.placement.reverse_map_transitions[en2] = ex1[0]

    def randomize_dungeons_trials_starting_entrances(self):
        # Do this in a deliberately hacky way, this is not supposed to be how ER works
        # Dungeon Entrance Rando.
        der = self.options.randomize_dungeons
        dungeons = ALL_DUNGEONS.copy()
        entrances = [DUNGEON_OVERWORLD_ENTRANCES[dungeon] for dungeon in ALL_DUNGEONS]
        if der == "All Surface Dungeons":
            indices = list(range(len(REGULAR_DUNGEONS)))
            shuffle_indices(self.rng, dungeons, indices=indices)

        elif der == "All Surface Dungeons + Sky Keep":
            self.rng.shuffle(dungeons)

        elif der == "Required Dungeons Separately":
            req_indices = [ALL_DUNGEONS.index(d) for d in self.required_dungeons]
            unreq_indices = [ALL_DUNGEONS.index(d) for d in self.unrequired_dungeons]
            if (
                not self.options["triforce-required"]
                or self.options["triforce-shuffle"] == "Anywhere"
            ):
                unreq_indices.append(ALL_DUNGEONS.index(SK))
            else:
                req_indices.append(ALL_DUNGEONS.index(SK))
            shuffle_indices(self.rng, dungeons, indices=req_indices)
            shuffle_indices(self.rng, dungeons, indices=unreq_indices)
        else:
            assert der == "None"

        pre_LMF_index = dungeons.index(LMF)

        dungeon_entrances = [
            [self.norm(e) for e in DUNGEON_ENTRANCE_EXITS[k]] for k in entrances
        ]
        dungeons = [[self.norm(DUNGEON_MAIN_EXITS[k])] for k in dungeons]

        if ALL_DUNGEONS[pre_LMF_index] != LMF:
            dungeons[pre_LMF_index].append(self.norm(LMF_SECOND_EXIT))

        self.reassign_entrances(dungeon_entrances, dungeons)

        # Trial Gate Entrance Rando.
        ter = self.options.randomize_trials
        pool = ALL_SILENT_REALMS.copy()
        gates = [SILENT_REALM_GATES[realm] for realm in ALL_SILENT_REALMS]
        if ter:
            self.rng.shuffle(pool)

        trial_entrances = [self.norm(TRIAL_GATE_EXITS[k]) for k in gates]
        trials = [self.norm(SILENT_REALM_EXITS[k]) for k in pool]
        self.reassign_entrances(trial_entrances, trials)

        # Ugly patch for needlessly useful songs : remove the trial exits from logic
        if self.options.randomize_all == "Vanilla":
            for trial_exit in trials:
                self.placement.map_transitions[trial_exit] = EIN(
                    entrance_of_exit(trial_exit)
                )

        # Starting Entrance Rando.
        ser = self.options.randomize_start_entrance
        allowed_provinces = self.options.allowed_starting_provinces

        possible_start_entrances = [
            entrance
            for entrance, values in self.areas.map_entrances.items()
            if values.get("can-start-at", True)
            and (values.get("province") in allowed_provinces)
            and (
                (
                    ser == "Bird Statues"
                    and values.get("subtype", False)
                    and values["subtype"] == "bird-statue-entrance"
                )
                or (
                    ser == "Any Surface Region"
                    and values.get("province") in TABLET_TO_PROVINCE.values()
                )
                or (ser == "Any")
            )
        ]
        possible_start_entrances.append(
            self.norm(self.areas.map_exits[self.norm(START)]["vanilla"])
        )

        start_entrance = self.rng.choice(possible_start_entrances)
        self.placement.map_transitions[self.norm(START)] = start_entrance

    def hacky_entrance_rando(self):
        entrances = list(k for k, v in self.areas.map_entrances.items() if "stage" in v)
        exits = list(
            k
            for k, v in self.areas.map_exits.items()
            if "stage" in v
            if "vanilla" in v
            if "Pillar" not in k
        )
        self.placement.reverse_map_transitions = {}
        self.placement.map_transitions = {
            k: self.norm(v["vanilla"])
            for k, v in self.areas.map_exits.items()
            if "stage" not in v
            if "vanilla" in v or "Pillar" in k
        }
        self.rng.shuffle(entrances)

        while len(entrances) < len(exits):
            l = entrances.copy()
            self.rng.shuffle(l)
            entrances.extend(l)

        for exit, entrance in zip(exits, entrances):
            self.placement.map_transitions[exit] = entrance
            self.placement.reverse_map_transitions[entrance] = exit
