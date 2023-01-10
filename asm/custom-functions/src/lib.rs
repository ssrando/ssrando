#![no_std]
#![feature(split_array)]

use core::{
    ffi::{c_uint, c_ushort, c_void},
    ptr::slice_from_raw_parts,
};

mod filemanager_gen;

#[repr(C)]
struct SpawnStruct {
    name: [u8; 32],
    transition_fade_frames: u16,
    room: u8,
    layer: u8,
    entrance: u8,
    night: u8,
    trial: u8,
    transition_type: u8,
    field8_0x28: u8,
    field9_0x29: u8,
    field10_0x2a: u8,
    field11_0x2b: u8,
}

#[repr(C)]
struct DungeonflagManager {
    should_commit: bool,
    flagindex: c_ushort,
}

extern "C" {
    static SPAWN_SLAVE: *mut SpawnStruct;
    fn setStoryflagToValue(flag: u16, value: u16);
    static SCENEFLAG_MANAGER: *mut c_void;
    fn SceneflagManager__setFlagGlobal(mgr: *mut c_void, scene_index: u16, flag: u16);
    static FILE_MANAGER: *mut filemanager_gen::FileManager;
    fn FileManager__getDungeonFlags(
        mgr: *mut filemanager_gen::FileManager,
    ) -> *mut [[c_ushort; 8usize]; 22usize];
    fn FlagManager__setFlagTo1(mgr: *mut c_void, flag: u16);
    fn FlagManager__setFlagOrCounter(mgr: *mut c_void, flag: u16, value: u16);
    static ITEMFLAG_MANAGER: *mut c_void;
    static STORYFLAG_MANAGER: *mut c_void;
    static mut STATIC_DUNGEON_FLAGS: [c_ushort; 8usize];
    static DUNGEONFLAG_MANAGER: *mut DungeonflagManager;
    fn checkButtonAPressed() -> bool;
    fn checkButtonBHeld() -> bool;
}

fn sceneflag_set_global(scene_index: u16, flag: u16) {
    unsafe { SceneflagManager__setFlagGlobal(SCENEFLAG_MANAGER, scene_index, flag) };
}

/// returns the pointer to the static dungeonflags, those for the current sceneflagindex
fn dungeonflag_local() -> *mut [c_ushort; 8usize] {
    unsafe { &mut STATIC_DUNGEON_FLAGS }
}

/// returns the pointer to the saved dungeonflags, for the specified sceneflagindex
fn dungeonflag_global(scene_index: u16) -> *mut [u16; 8] {
    unsafe {
        (*FileManager__getDungeonFlags(FILE_MANAGER))
            .as_mut_ptr()
            .add(scene_index as usize)
    }
}

fn storyflag_set_to_value(flag: u16, value: u16) {
    unsafe { FlagManager__setFlagOrCounter(STORYFLAG_MANAGER, flag, value) };
}

fn storyflag_set_to_1(flag: u16) {
    unsafe { FlagManager__setFlagTo1(STORYFLAG_MANAGER, flag) };
}

fn itemflag_set_to_value(flag: u16, value: u16) {
    unsafe { FlagManager__setFlagOrCounter(ITEMFLAG_MANAGER, flag, value) };
}

/// A basic iterator over some borrowed memory
/// useful to read consecutive halfwords
struct MemItr<'a>(&'a [u8]);

impl<'a> MemItr<'a> {
    fn next_u8(&mut self) -> Option<u8> {
        let val;
        (val, self.0) = self.0.split_first()?;
        Some(*val)
    }

    fn next_u16(&mut self) -> Option<u16> {
        if self.0.len() < 2 {
            return None;
        }
        let val;
        (val, self.0) = self.0.split_array_ref();
        Some(u16::from_be_bytes(*val))
    }

    fn get_dungeonflags(&mut self) -> Option<&[u8; 8]> {
        if self.0.len() < 8 {
            return None;
        }
        let val;
        (val, self.0) = self.0.split_array_ref();
        Some(val)
    }
}

// IMPORTANT: when adding functions here that need to get called from the game, add `#[no_mangle]`
// and add a .global *symbolname* to custom_funcs.asm
#[no_mangle]
pub fn process_startflags() {
    unsafe { (*FILE_MANAGER).anticommit_flag = 1 };
    let mut flag_mem = MemItr(unsafe { &*slice_from_raw_parts(0x804ee1b8 as *const u8, 512) });
    // storyflags
    while let Some(flag) = flag_mem.next_u16() {
        if flag == 0xFFFF {
            break;
        }
        storyflag_set_to_1(flag);
    }
    // itemflags
    while let Some(flag) = flag_mem.next_u16() {
        if flag == 0xFFFF {
            break;
        }
        itemflag_set_to_value(flag & 0x1FF, flag >> 9);
    }
    // sceneflags
    while let Some(flag) = flag_mem.next_u16() {
        if flag == 0xFFFF {
            break;
        }
        sceneflag_set_global(flag >> 8, flag & 0xFF);
    }
    // dungeonflags
    // includes keys, maps, boss keys
    // each entry is a byte, the bits work as follows:
    // B0KK KKM0, B(K), M(AP), K(EY)
    // doing it this weird way to save instructions
    const DUNGEONFLAG_INDICES: [u8; 8] = [
        11, // SV
        14, // ET
        17, // LMF
        12, // AC
        18, // SS
        15, // FS
        20, // SK
        9,  // Lanayru Caves
    ];
    if let Some(dungeon_startflags) = flag_mem.get_dungeonflags() {
        for (&dungeon_startflag, &flagindex) in
            dungeon_startflags.iter().zip(DUNGEONFLAG_INDICES.iter())
        {
            let first_short = dungeon_startflag & 0x82;
            let small_keys = (dungeon_startflag >> 2) & 0x0F;
            unsafe {
                if (*DUNGEONFLAG_MANAGER).flagindex == flagindex as u16 {
                    let flags = &mut *dungeonflag_local();
                    flags[0] = first_short.into();
                    flags[1] = small_keys.into();
                }
                let flags = &mut *dungeonflag_global(flagindex as u16);
                flags[0] = first_short.into();
                flags[1] = small_keys.into();
            }
        }
    }
    itemflag_set_to_value(
        501, /* rupee counter */
        flag_mem.next_u16().unwrap_or_default(),
    );
    // heart capacity
    let health_capacity = flag_mem.next_u8().unwrap_or_default();
    unsafe { (*FILE_MANAGER).FA.health_capacity = health_capacity.into() };
    unsafe { (*FILE_MANAGER).FA.current_health = health_capacity.into() };
    unsafe { (*FILE_MANAGER).anticommit_flag = 0 };
}

#[no_mangle]
fn handle_bk_map_dungeonflag(item: c_ushort) {
    const BK_TO_FLAGINDEX: [u8; 7] = [
        // starts at 25
        12, // AC
        15, // FS
        18, // SSH
        13, // unused, shouldn't happen
        11, // SV
        14, // ET
        17, // LMF
    ];
    const MAP_TO_FLAGINDEX: [u8; 7] = [
        // starts at 207
        11, // SV
        14, // ET
        17, // LMF
        12, // AC
        15, // FS
        18, // SSH
        20, // SK
    ];

    let (flagindex, dungeonflag_mask) =
        if let Some(flagindex) = BK_TO_FLAGINDEX.get((item as usize).wrapping_sub(25)) {
            (*flagindex, 0x80)
        } else if let Some(flagindex) = MAP_TO_FLAGINDEX.get((item as usize).wrapping_sub(207)) {
            (*flagindex, 0x02)
        } else {
            return;
        };
    unsafe {
        if (*DUNGEONFLAG_MANAGER).flagindex == flagindex as u16 {
            (*dungeonflag_local())[0] |= dungeonflag_mask;
        }
        (*dungeonflag_global(flagindex as u16))[0] |= dungeonflag_mask;
    }
}

#[no_mangle]
fn textbox_a_pressed_or_b_held() -> bool {
    unsafe {
        if checkButtonAPressed() || checkButtonBHeld() {
            return true;
        }
        return false;
    }
}

#[no_mangle]
fn set_goddess_sword_pulled_scene_flag(){
    unsafe {
        // Set story flag 951 (Raised Goddess Sword in Goddess Statue).
        storyflag_set_to_1(951);
    }
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
