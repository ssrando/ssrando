import os
import yaml
import re

from sslib.fs_helpers import *
from sslib.rel import REL, RELSection, RELRelocation, RELRelocationType

ORIGINAL_FREE_SPACE_RAM_ADDRESS = 0x806782C0
ORIGINAL_DOL_SIZE = 0x57A680


def split_pointer_into_high_and_low_half_for_hardcoding(pointer):
    high_halfword = (pointer & 0xFFFF0000) >> 16
    low_halfword = pointer & 0xFFFF

    if low_halfword >= 0x8000:
        # If the low halfword has the highest bit set, it will be considered a negative number.
        # Therefore we need to add 1 to the high halfword (equivalent to adding 0x10000) to compensate for the low halfword being negated.
        high_halfword = high_halfword + 1

    return high_halfword, low_halfword


def apply_dol_patch(self, dol, patch):
    for org_address, patchlet in patch.items():
        new_bytes = patchlet["Data"]

        free_space_start = self.free_space_start_offsets["main.dol"]

        if org_address >= free_space_start:
            add_free_space_section_to_main_dol(dol, new_bytes)
        else:
            dol.write_data(
                write_and_pack_bytes, org_address, new_bytes, "B" * len(new_bytes)
            )


def apply_rel_patch(self, rel, rel_name, patches):
    assert rel_name.endswith(".rel")
    free_space_start = self.free_space_start_offsets[rel_name]
    for org_address, patchlet in patches.items():
        new_bytes = patchlet["Data"]
        offset = org_address
        relocations = patchlet.get("Relocations", [])

        if offset >= free_space_start:
            apply_free_space_patchlet_to_rel(
                self, rel, rel_name, offset, new_bytes, relocations
            )
        else:
            rel.write_data(
                write_and_pack_bytes, offset, new_bytes, "B" * len(new_bytes)
            )

            rel.delete_relocation_in_range(offset, len(new_bytes))

            if relocations:
                (
                    rel_section_index,
                    offset_into_section,
                ) = rel.convert_rel_offset_to_section_index_and_relative_offset(offset)
                add_relocations_to_rel(
                    self,
                    rel,
                    rel_name,
                    rel_section_index,
                    offset_into_section,
                    relocations,
                )


def add_free_space_section_to_main_dol(main_dol, new_bytes):
    dol_section = main_dol.sections[2]
    patch_length = len(new_bytes)

    if dol_section.size != 0:
        raise Exception(
            "Having multiple separate free space directives for main.dol is not currently supported."
        )

    # First add a new text section to the dol (Text2).
    dol_section.offset = ORIGINAL_DOL_SIZE  # Set the file offset of new Text2 section (which will be the original end of the file, where we put the patch)
    dol_section.address = ORIGINAL_FREE_SPACE_RAM_ADDRESS  # Write loading address of the new Text2 section
    dol_section.size = patch_length  # Write length of the new Text2 section

    # Next write our custom code to the end of the dol file.
    main_dol.write_data(
        write_and_pack_bytes,
        ORIGINAL_FREE_SPACE_RAM_ADDRESS,
        new_bytes,
        "B" * len(new_bytes),
    )

    # Next we need to change a hardcoded pointer to where free space begins. Otherwise the game will overwrite the custom code.
    padded_patch_length = (
        patch_length + 3
    ) & ~3  # Pad length of patch to next 4 just in case
    new_start_pointer_for_default_thread = (
        ORIGINAL_FREE_SPACE_RAM_ADDRESS + padded_patch_length
    )  # New free space pointer after our custom code
    high_halfword, low_halfword = split_pointer_into_high_and_low_half_for_hardcoding(
        new_start_pointer_for_default_thread
    )
    # Now update the asm instructions that load this hardcoded pointer.
    main_dol.write_data(write_u32, 0x803AC480, 0x3CA00000 | high_halfword)
    main_dol.write_data(write_u32, 0x803AC48C, 0x38A50000 | low_halfword)
    # more hardcoded pointers that come later
    new_end_pointer_for_default_thread = new_start_pointer_for_default_thread + 0x10000
    high_halfword, low_halfword = split_pointer_into_high_and_low_half_for_hardcoding(
        new_end_pointer_for_default_thread
    )
    main_dol.write_data(write_u32, 0x803AC47C, 0x3C600000 | high_halfword)
    main_dol.write_data(write_u32, 0x803AC484, 0x38630000 | low_halfword)
    main_dol.write_data(write_u32, 0x803A2988, 0x3C600000 | high_halfword)
    main_dol.write_data(write_u32, 0x803A2990, 0x38630000 | low_halfword)
    main_dol.write_data(write_u32, 0x803A2AF0, 0x3C600000 | high_halfword)
    main_dol.write_data(write_u32, 0x803A2AF4, 0x38630000 | low_halfword)
    high_halfword = (new_end_pointer_for_default_thread & 0xFFFF0000) >> 16
    low_halfword = new_end_pointer_for_default_thread & 0xFFFF
    # default stack pointer
    main_dol.write_data(write_u32, 0x80004284, 0x3C200000 | high_halfword)
    main_dol.write_data(write_u32, 0x80004288, 0x60210000 | low_halfword)

    # Original thread start pointer: 803FCFA8 (must be updated)
    # Original stack end pointer (r1): 8040CFA8 (must be updated)
    # Original rtoc pointer (r2): 803FFD00 (must NOT be updated)
    # Original read-write small data area pointer (r13): 803FE0E0 (must NOT be updated)


def apply_free_space_patchlet_to_rel(
    self, rel, file_path, offset, new_bytes, relocations
):
    # We add a new section to the REL to hold our custom code.

    # Use REL section 7 for any custom code we add into RELs.
    # REL sections 7-0x10 were present in all RELs in the original game, but always uninitialized, so we can use them freely.
    # (REL section 0 was also present in all RELs but uninitialized, but that one seems to be necessary for some reason.)
    rel_section_index = 7
    rel_section = rel.sections[rel_section_index]
    if rel_section.is_uninitialized:
        # This is the first free space patchlet we're applying to this REL, so initialize the section.
        add_free_space_section_to_rel(self, rel, file_path)

    section_relative_offset = offset - rel_section.offset
    write_and_pack_bytes(
        rel_section.data, section_relative_offset, new_bytes, "B" * len(new_bytes)
    )

    if relocations:
        add_relocations_to_rel(
            self,
            rel,
            file_path,
            rel_section_index,
            section_relative_offset,
            relocations,
        )


def add_free_space_section_to_rel(self, rel, file_path):
    rel_section_index = 7
    rel_section = rel.sections[rel_section_index]

    assert not rel_section.is_bss
    rel_section.is_uninitialized = False
    rel_section.is_executable = True
    rel_section.data = BytesIO()

    # We could leave it to the REL implementation's saving logic to decide where to place the free space, but to be on the safe side, instead use the free space offset from free_space_start_offsets.txt, because that's the offset that was used for linking the code.
    rel_section.offset = self.free_space_start_offsets[file_path]


def add_relocations_to_rel(
    self, rel, file_path, rel_section_index, offset_into_section, relocations
):
    # Create the new REL relocations.

    free_space_start = self.free_space_start_offsets[file_path]

    for relocation_dict in relocations:
        symbol_name = relocation_dict["SymbolName"]
        relocation_offset = relocation_dict["Offset"]
        relocation_type = relocation_dict["Type"]

        relocation_offset += offset_into_section

        rel_relocation = RELRelocation()
        rel_relocation.relocation_type = RELRelocationType[relocation_type]

        branch_label_match = re.search(
            r"^branch_label_([0-9A-F]+)$", symbol_name, re.IGNORECASE
        )
        if (
            symbol_name in self.main_custom_symbols
            or symbol_name in self.main_original_symbols
        ):
            # Custom symbol located in main.dol.
            module_num = 0

            rel_relocation.symbol_address = (
                self.main_custom_symbols.get(symbol_name, None)
                or self.main_original_symbols[symbol_name]
            )

            # I don't think this value is used for dol relocations.
            # In vanilla, this was written as 4 for some reason?
            rel_relocation.section_num_to_relocate_against = 0
        elif symbol_name in self.custom_symbols.get(
            file_path, {}
        ) or symbol_name in self.original_symbols.get(file_path, {}):
            # Custom symbol located in the current REL.
            custom_symbol_offset = (
                self.custom_symbols.get(file_path, {}).get(symbol_name, None)
                or self.original_symbols[file_path][symbol_name]
            )
            module_num = rel.id

            if custom_symbol_offset >= free_space_start:
                # In our custom free space section.
                other_rel_section_index = 7
                relative_offset = custom_symbol_offset - free_space_start
            else:
                (
                    other_rel_section_index,
                    relative_offset,
                ) = rel.convert_rel_offset_to_section_index_and_relative_offset(
                    custom_symbol_offset
                )

            rel_relocation.section_num_to_relocate_against = other_rel_section_index
            rel_relocation.symbol_address = relative_offset
        elif branch_label_match:
            # Relative branch. The destination must be in the current REL.
            branch_dest_offset = int(branch_label_match.group(1), 16)

            module_num = rel.id

            (
                other_rel_section_index,
                relative_offset,
            ) = rel.convert_rel_offset_to_section_index_and_relative_offset(
                branch_dest_offset
            )
            rel_relocation.section_num_to_relocate_against = other_rel_section_index
            rel_relocation.symbol_address = relative_offset
        else:
            raise Exception("Could not find symbol name: %s" % symbol_name)

        rel_relocation.relocation_offset = relocation_offset
        rel_relocation.curr_section_num = rel_section_index

        if module_num not in rel.relocation_entries_for_module:
            rel.relocation_entries_for_module[module_num] = []
        rel.relocation_entries_for_module[module_num].append(rel_relocation)
