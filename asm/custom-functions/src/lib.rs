#![no_std]
#![feature(split_array)]
#![allow(unused)]

use core::{
    ffi::{c_char, c_double, c_ushort, c_void},
    ptr, slice,
};

use button::*;
use cstr::cstr;
use wchar::wchz;

use message::{text_manager_set_num_args, text_manager_set_string_arg, FlowElement};
use text_print::{write_to_screen, SimpleMenu};

mod button;
mod filemanager_gen;
mod message;
mod text_print;

#[repr(C)]
struct SpawnStruct {
    name:                   [u8; 32],
    transition_fade_frames: u16,
    room:                   u8,
    layer:                  u8,
    entrance:               u8,
    night:                  u8,
    trial:                  u8,
    transition_type:        u8,
    field8_0x28:            u8,
    field9_0x29:            u8,
    field10_0x2a:           u8,
    field11_0x2b:           u8,
}

#[repr(C)]
struct DungeonflagManager {
    should_commit: bool,
    flagindex:     c_ushort,
}

#[repr(C)]
struct ActorEventFlowMgr {
    vtable:                     u32,
    msbf_info:                  u32,
    current_flow_index:         u32,
    unk1:                       u32,
    unk2:                       u32,
    unk3:                       u32,
    result_from_previous_check: u32,
    current_text_label_name:    [u8; 32],
    unk4:                       u32,
    unk5:                       u32,
    unk6:                       u32,
    next_flow_delay_timer:      u32,
    another_flow_element:       u128,
    unk7:                       u32,
    unk8:                       u32,
}

#[repr(C)]
struct AcOBird {
    pad:   [u8; 0x144],
    speed: f32,
}

#[repr(i32)]
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
enum SpecialMinigameState {
    State0,
    BambooCutting,
    FunFunIsland,
    ThrillDigger,
    PumpkinCarry,
    InsectCaptureGame,
    PumpkinClayShooting,
    RollercoasterMinigame,
    TrialTimeAttack,
    BossRush,
    HouseCleaning,
    SpiralChargeTutorial,
    HarpPlaying,
    StateNone = -1,
}

impl SpecialMinigameState {
    pub fn get() -> Self {
        unsafe { SPECIAL_MINIGAME_STATE }
    }

    pub fn is_current(self) -> bool {
        Self::get() == self
    }
}

#[repr(C)]
struct Reloader {
    _0:                        [u8; 0x290],
    initial_speed:             f32,
    stamina_amount:            u32,
    item_to_use_on_reload:     u8,
    beedle_shop_spawn_state:   u8,
    spawn_state:               i16, // actionIndex
    last_area_type:            u32,
    type_0_pos_flag:           u8,
    unk:                       u8,
    save_prompt_flag:          u8,
    prevent_save_respawn_info: bool,
}

#[repr(C)]
struct StartInfo {
    stage:        [u8; 8],
    room:         u8,
    layer:        u8,
    entrance:     u8,
    forced_night: u8,
}

#[repr(C)]
struct ConsoleHead {
    text_buf:            u32, // u8*
    width:               u16,
    height:              u16,
    priority:            u16,
    attr:                u16,
    print_top:           u16,
    print_x_pos:         u16,
    ring_top:            u16,
    __pad_0:             u16,
    ring_top_line_count: i32,
    view_top_lin:        i32,
    view_pos_x:          u16,
    view_pos_y:          u16,
    view_lines:          u16,
    is_visible:          u8,
    __pad_1:             u8,
    writer:              u32, // TextWriteBase*
    next:                u32, // next consolehead pointer
}

#[repr(C)]
#[derive(Default)]
struct CharWriter {
    m_color_mapping:  [u32; 2],
    m_vertex_colors:  [u32; 4],
    m_text_color:     [u32; 2],
    m_text_gradation: u32,
    m_scale:          [f32; 2],
    m_cursor_pos:     [f32; 3],
    m_texture_filter: [u32; 2],
    __pad:            u16,
    m_alpha:          u8,
    m_is_width_fixed: u8,
    m_fixed_width:    f32,
    m_font_ptr:       u32,
}

#[repr(C)]
#[derive(Default)]
struct TextWriterBase {
    m_char_writer:   CharWriter,
    m_width_limit:   f32,
    m_char_space:    f32,
    m_line_space:    f32,
    m_tab_width:     i32,
    m_draw_flag:     u32,
    m_tag_processor: u32, // pointer to TagProcessor
}

#[repr(C)]
struct Matrix {
    mtx: [[f32; 4]; 3],
}

#[repr(C)]
struct MTX44 {
    mtx: [f32; 16],
}
#[repr(C)]
struct ActorLink {
    base_base:      [u8; 0x60 - 0x00],
    vtable:         u32,
    obj_base_pad0:  [u8; 0x5C],
    pos_x:          f32,
    pos_y:          f32,
    pos_z:          f32,
    obj_base_pad:   [u8; 0x330 - (0x64 + 0x5C + 0xC)],
    pad01:          [u8; 0x4498 - 0x330],
    stamina_amount: u32,
    // More after
}

#[repr(C)]
struct List {
    head:   u32,
    tail:   u32,
    count:  u16,
    offset: u16,
}

#[repr(C)]
struct Heap {
    vtable:         *const c_void,
    m_contain_heap: *mut Heap,
    m_link:         [u32; 2], // node
    m_heap_handle:  u32,      // MEMiHeapHead*
    m_parent_block: *mut c_void,
    m_flag:         u16,
    __pad:          u16,
    m_node:         [u32; 2], // node
    m_children:     List,
    n_name:         *const c_char,
}

extern "C" {

    fn swprintf(out: *mut u16, len: u32, fmt: *const u16, ...) -> i32;
    fn wcslen(string: *const u16) -> u32;
    fn printf(string: *const c_char, ...);
    static mut CURRENT_HEAP: *mut Heap;
    static mut GAME_FRAME: u32;
    fn Heap__alloc(size: u32, align: u32, heap: *const Heap) -> *mut c_void;
    static mut SPAWN_SLAVE: SpawnStruct;
    static LINK_PTR: *mut ActorLink;
    fn setStoryflagToValue(flag: u16, value: u16);
    static SCENEFLAG_MANAGER: *mut c_void;
    fn SceneflagManager__setFlagGlobal(mgr: *mut c_void, scene_index: u16, flag: u16);
    fn SceneflagManager__unsetFlagGlobal(mgr: *mut c_void, scene_index: u16, flag: u16);
    fn SceneflagManager__checkFlagGlobal(mgr: *mut c_void, scene_index: u16, flag: u16) -> bool;
    static FILE_MANAGER: *mut filemanager_gen::FileManager;
    fn FileManager__getDungeonFlags(
        mgr: *mut filemanager_gen::FileManager,
    ) -> *mut [[c_ushort; 8usize]; 22usize];
    fn FlagManager__setFlagTo1(mgr: *mut c_void, flag: u16);
    fn FlagManager__getFlagOrCounter(mgr: *mut c_void, flag: u16) -> u16;
    fn FlagManager__setFlagOrCounter(mgr: *mut c_void, flag: u16, value: u16);
    static ITEMFLAG_MANAGER: *mut c_void;
    static mut STATIC_ITEMFLAGS: [c_ushort; 0x40];
    fn ItemflagManager__doCommit(mgr: *mut c_void);
    static STORYFLAG_MANAGER: *mut c_void;
    static mut STATIC_STORYFLAGS: [c_ushort; 0x80];
    fn StoryflagManager__doCommit(mgr: *mut c_void);
    static mut STATIC_DUNGEON_FLAGS: [c_ushort; 8usize];
    static DUNGEONFLAG_MANAGER: *mut DungeonflagManager;
    fn checkStoryflagIsSet(p: *const c_void, flag: u16) -> bool;
    fn checkItemFlag(flag: u16) -> bool;
    fn getKeyPieceCount() -> u16;
    fn increaseCounter(counterId: u16, count: u16);
    fn setFlagForItem(itemflag: u16);
    fn getModelDataFromOarc(oarc_mgr: *const c_void, oarc_str: *const c_char) -> *const c_void;
    static INPUT_BUFFER: u32;
    fn findActorByActorType(actor_type: i32, start_actor: *const c_void) -> *mut c_void;
    fn checkXZDistanceFromLink(actor: *const c_void, distance: f32) -> bool;
    static mut SPECIAL_MINIGAME_STATE: SpecialMinigameState;
    static mut ITEM_GET_BOTTLE_POUCH_SLOT: u32;
    static mut NUMBER_OF_ITEMS: u32;
    fn AcItem__setupItemParams(
        item_id: u16,
        subtype: u32,
        unk1: u32,
        sceneflag: u32,
        unk2: u32,
        unk3: u32,
    ) -> u32;
    fn AcItem__spawnItem(
        room: u32,
        item_params: u32,
        pos: u32,   // actually Vec3f
        rot: u32,   // actually Vec3s
        scale: u32, // actually Vec3f
        params2: u32,
        unk: u32,
    ) -> *mut c_void;
    fn actuallyTriggerEntrance(
        stage_name: *const u8,
        room: u8,
        layer: u8,
        entrance: u8,
        forced_night: u8,
        forced_trial: u8,
        transition_type: u8,
        transition_fade_frames: u8,
        param_9: u8,
    );
    static mut RELOADER_PTR: *mut Reloader;
    fn RoomManager__getRoomByIndex(room_mgr: *mut c_void, room_number: u32);
    fn Reloader__setReloadTrigger(reloader: *mut Reloader, trigger: u8);
    fn getCurrentHealth(mgr: *mut filemanager_gen::FileManager) -> u16;

}

// Example Function on writing text to screen
fn write_text_on_screen() {
    if unsafe { !LINK_PTR.is_null() } {
        let (x, y, z) = unsafe { ((*LINK_PTR).pos_x, (*LINK_PTR).pos_y, (*LINK_PTR).pos_z) };
        write_to_screen(format_args!("pos:\n{x:.3}\n{y:.3}\n{z:.3}"), 10, 20);
    }
}

fn storyflag_check(flag: u16) -> bool {
    unsafe { checkStoryflagIsSet(core::ptr::null(), flag) }
}

fn itemflag_check(flag: u16) -> bool {
    unsafe { checkItemFlag(flag) }
}

fn sceneflag_set_global(scene_index: u16, flag: u16) {
    unsafe { SceneflagManager__setFlagGlobal(SCENEFLAG_MANAGER, scene_index, flag) };
}

fn sceneflag_unset_global(scene_index: u16, flag: u16) {
    unsafe { SceneflagManager__unsetFlagGlobal(SCENEFLAG_MANAGER, scene_index, flag) };
}

fn sceneflag_check_global(scene_index: u16, flag: u16) -> bool {
    unsafe { SceneflagManager__checkFlagGlobal(SCENEFLAG_MANAGER, scene_index, flag) }
}

/// returns the pointer to the static dungeonflags, those for the current
/// sceneflagindex
fn dungeonflag_local() -> *mut [c_ushort; 8usize] {
    unsafe { &mut STATIC_DUNGEON_FLAGS }
}

/// returns the pointer to the saved dungeonflags, for the specified
/// sceneflagindex
fn dungeonflag_global(scene_index: u16) -> *mut [u16; 8] {
    unsafe {
        (*FileManager__getDungeonFlags(FILE_MANAGER))
            .as_mut_ptr()
            .add(scene_index as usize)
    }
}

fn dungeon_global_key_count(scene_index: u16) -> u16 {
    unsafe { (*dungeonflag_global(scene_index))[1] & 0xF }
}

fn storyflag_get_value(flag: u16) -> u16 {
    return unsafe { FlagManager__getFlagOrCounter(STORYFLAG_MANAGER, flag) };
}

fn storyflag_set_to_value(flag: u16, value: u16) {
    unsafe { FlagManager__setFlagOrCounter(STORYFLAG_MANAGER, flag, value) };
}

fn itemflag_set_to_value(flag: u16, value: u16) {
    unsafe { FlagManager__setFlagOrCounter(ITEMFLAG_MANAGER, flag, value) };
}

#[link_section = "data"]
static mut IS_FILE_START: bool = false;

#[link_section = "data"]
#[no_mangle]
static mut FORCE_MOGMA_CAVE_DIVE: bool = false;

// IMPORTANT: when adding functions here that need to get called from the game,
// add `#[no_mangle]` and add a .global *symbolname* to custom_funcs.asm
#[no_mangle]
pub fn process_startflags() {
    unsafe { (*FILE_MANAGER).anticommit_flag = 1 };
    #[repr(C)]
    struct StartflagInfo {
        storyflags:    [u16; 0x80],
        itemflags:     [u16; 0x40],
        dungeonflags:  [u8; 8],
        full_hearts:   u8,
        pouch_options: u8,
        // this is just the max amount of possible flags, not the actual amount
        sceneflags:    [u8; 118],
    }
    let startflag_info = unsafe { &*(0x804EE1B8 as *const StartflagInfo) };
    unsafe {
        // storyflags
        STATIC_STORYFLAGS = startflag_info.storyflags;
        // itemflags
        STATIC_ITEMFLAGS = startflag_info.itemflags;
    }
    // sceneflags
    let mut scene_idx = 0;
    for flag in startflag_info.sceneflags.iter() {
        if *flag == 0xFF {
            break;
        } else if *flag >= 0x80 {
            scene_idx = flag & 0x7F;
        } else {
            sceneflag_set_global(scene_idx.into(), (*flag).into());
        }
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
    for (&dungeon_startflag, &flagindex) in startflag_info
        .dungeonflags
        .iter()
        .zip(DUNGEONFLAG_INDICES.iter())
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

    // Starting heart capacity.
    let health_capatity = startflag_info.full_hearts * 4;
    unsafe { (*FILE_MANAGER).FA.health_capacity = health_capatity.into() };
    unsafe { (*FILE_MANAGER).FA.current_health = health_capatity.into() };

    let mut pouch_slot_iter = unsafe { (*FILE_MANAGER).FA.pouch_items.iter_mut() };

    // Starting Hylian Shield.
    // 4th bit.
    if startflag_info.pouch_options >> 3 & 0x1 == 1 {
        // ID for Hylian Shield + durability
        *pouch_slot_iter.next().unwrap() = 125 | 0x30 << 0x10;
    }

    // Starting Bottles.
    // Last bit.
    let bottle_count = startflag_info.pouch_options & 0x7;
    for slot in pouch_slot_iter.take(bottle_count.into()) {
        *slot = 153; // ID for bottles
    }

    // Should set respawn info after new file start
    unsafe { IS_FILE_START = true };

    // Commit global flag managers.
    unsafe {
        ItemflagManager__doCommit(ITEMFLAG_MANAGER);
        StoryflagManager__doCommit(STORYFLAG_MANAGER);
    }

    unsafe { (*FILE_MANAGER).anticommit_flag = 0 };
}

#[no_mangle]
pub fn handle_bk_map_dungeonflag(item: c_ushort) {
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

const OBTAINED_TEXT: &[u8; 18] = b"\0O\0b\0t\0a\0i\0n\0e\0d\0\0";
const UNOBTAINED_TEXT: &[u8; 22] = b"\0U\0n\0o\0b\0t\0a\0i\0n\0e\0d\0\0";
const COMPLETE_TEXT: &[u8; 42] = b"\0\x0e\0\x00\0\x03\0\x02\0\x08\0 \0C\0o\0m\0p\0l\0e\0t\0e\0 \0\x0e\0\x00\0\x03\0\x02\xFF\xFF\0\0";
const INCOMPLETE_TEXT: &[u8; 46] = b"\0\x0e\0\x00\0\x03\0\x02\0\x09\0 \0I\0n\0c\0o\0m\0p\0l\0e\0t\0e\0 \0\x0e\0\x00\0\x03\0\x02\xFF\xFF\0\0";
const UNREQUIRED_TEXT: &[u8; 46] = b"\0\x0e\0\x00\0\x03\0\x02\0\x0C\0 \0U\0n\0r\0e\0q\0u\0i\0r\0e\0d\0 \0\x0e\0\x00\0\x03\0\x02\xFF\xFF\0\0";

#[no_mangle]
fn rando_text_command_handler(
    _event_flow_mgr: *mut ActorEventFlowMgr,
    p_flow_element: *const FlowElement,
) {
    let flow_element = unsafe { &*p_flow_element };
    match flow_element.param3 {
        71 => {
            let dungeon_index = flow_element.param1;
            let completion_storyflag = flow_element.param2;
            let key_count = if dungeon_index == 14
            // ET
            {
                unsafe { getKeyPieceCount() }
            } else {
                dungeon_global_key_count(dungeon_index)
            };
            text_manager_set_num_args(&[key_count as u32]);
            let map_and_bk = unsafe { (*dungeonflag_global(dungeon_index))[0] };
            let bk_text = match map_and_bk & 0x82 {
                0x80 => OBTAINED_TEXT.as_ptr(),
                0x82 => OBTAINED_TEXT.as_ptr(),
                _ => UNOBTAINED_TEXT.as_ptr(),
            };
            let map_text = match map_and_bk & 0x82 {
                0x02 => OBTAINED_TEXT.as_ptr(),
                0x82 => OBTAINED_TEXT.as_ptr(),
                _ => UNOBTAINED_TEXT.as_ptr(),
            };
            text_manager_set_string_arg(bk_text as *const c_void, 0);
            text_manager_set_string_arg(map_text as *const c_void, 1);

            let completed_text = if completion_storyflag == 0xFFFF {
                UNREQUIRED_TEXT.as_ptr()
            } else if storyflag_check(completion_storyflag) {
                COMPLETE_TEXT.as_ptr()
            } else {
                INCOMPLETE_TEXT.as_ptr()
            };
            text_manager_set_string_arg(completed_text as *const c_void, 2);
        },
        72 => {
            let caves_key = dungeon_global_key_count(9);
            let caves_key_text = if caves_key == 1 {
                OBTAINED_TEXT.as_ptr()
            } else {
                UNOBTAINED_TEXT.as_ptr()
            };
            text_manager_set_string_arg(caves_key_text as *const c_void, 0);

            let spiral_charge_obtained = 364; // story flag for spiral charge
            let spiral_charge_text = if storyflag_check(spiral_charge_obtained) {
                OBTAINED_TEXT.as_ptr()
            } else {
                UNOBTAINED_TEXT.as_ptr()
            };
            text_manager_set_string_arg(spiral_charge_text as *const c_void, 1);

            let life_tree_fruit_obtained = 198; // item flag for life tree fruit
            let life_tree_fruit_text = if itemflag_check(life_tree_fruit_obtained) {
                OBTAINED_TEXT.as_ptr()
            } else {
                UNOBTAINED_TEXT.as_ptr()
            };
            text_manager_set_string_arg(life_tree_fruit_text as *const c_void, 2);

            // Tadtones obtained.
            text_manager_set_num_args(&[storyflag_get_value(953) as u32]);
        },
        73 => send_to_start(),
        74 => {
            // Increment storyflag counter
            let flag = flow_element.param1;
            let increment = flow_element.param2;

            storyflag_set_to_value(flag, storyflag_get_value(flag) + increment);
        },
        75 => {
            // Have collected all tadtone groups?
            let tadtone_groups_left: u32 = 17_u16.saturating_sub(storyflag_get_value(953)).into();
            text_manager_set_num_args(&[tadtone_groups_left]);
            unsafe {
                (*_event_flow_mgr).result_from_previous_check = tadtone_groups_left;
            }
        },
        _ => (),
    }
}

#[no_mangle]
fn textbox_a_pressed_or_b_held() -> bool {
    if is_pressed(A) || is_down(B) {
        return true;
    }
    return false;
}

#[no_mangle]
fn set_goddess_sword_pulled_scene_flag() {
    // Set story flag 951 (Raised Goddess Sword in Goddess Statue).
    storyflag_set_to_1(951);
}

fn simple_rng(rng: &mut u32) -> u32 {
    *rng = rng.wrapping_mul(1664525).wrapping_add(1013904223);
    *rng
}

#[no_mangle]
fn randomize_boss_key_start_pos(ptr: *mut u16, mut seed: u32) {
    // 6 dungeons, each having a Vec3s which is just 3 u16 (or rather i16)
    let angles = unsafe { slice::from_raw_parts_mut(ptr, 3 * 6) };
    for angle in angles.iter_mut() {
        *angle = simple_rng(&mut seed) as u16;
    }
}

#[no_mangle]
fn get_item_arc_name(
    oarc_mgr: *const c_void,
    vanilla_item_str: *const c_char,
    item_id: u32,
) -> *const c_void {
    let mut oarc_name;

    match item_id {
        214 => oarc_name = cstr!("Onp").as_ptr(),         // tadtone
        215 => oarc_name = cstr!("DesertRobot").as_ptr(), // scrapper
        _ => oarc_name = vanilla_item_str,
    }

    return unsafe { getModelDataFromOarc(oarc_mgr, oarc_name) };
}

#[no_mangle]
fn get_item_model_name_ptr(item_id: u32) -> *const c_char {
    match item_id {
        214 => return cstr!("OnpB").as_ptr(),        // tadtone
        215 => return cstr!("DesertRobot").as_ptr(), // scrapper
        _ => return core::ptr::null(),
    }
}

#[no_mangle]
fn enforce_loftwing_speed_cap(loftwing_ptr: *mut AcOBird) {
    let loftwing = unsafe { &mut *loftwing_ptr };
    let mut is_in_levias_fight = false;
    if unsafe { &SPAWN_SLAVE.name[..4] } == b"F023"
        && storyflag_check(368 /* Pumpkin soup delivered */)
        && !storyflag_check(200 /* Levias explains SotH quest */)
    {
        let levias_ptr = unsafe {
            findActorByActorType(184 /* NusiB */, ptr::null())
        };
        if !levias_ptr.is_null() {
            if unsafe { checkXZDistanceFromLink(levias_ptr, 20_000f32) } {
                is_in_levias_fight = true;
            }
        }
    }
    let in_spiral_charge_training = SpecialMinigameState::SpiralChargeTutorial.is_current();
    let b_held = unsafe { INPUT_BUFFER } & 0x0400_0000 != 0;
    let cap = if is_in_levias_fight || in_spiral_charge_training || b_held {
        80f32
    } else {
        350f32
    };
    if loftwing.speed > cap {
        loftwing.speed = cap;
    }
}

// The same as give_item only you can control the sceneflag of the item given.
#[no_mangle]
fn give_item_with_sceneflag(
    item_id: u16,
    bottle_pouch_slot: u32,
    number: u32,
    sceneflag: u32,
) -> *mut c_void {
    unsafe {
        ITEM_GET_BOTTLE_POUCH_SLOT = bottle_pouch_slot;
        NUMBER_OF_ITEMS = number;
        // Same as the vanilla setupItemParams function only with extra control over
        // the sceneflag
        let item_params = AcItem__setupItemParams(item_id, 5, 0, sceneflag, 1, 0xFF);

        let item = AcItem__spawnItem(u32::MAX, item_params, 0, 0, 0, u32::MAX, 1);
        ITEM_GET_BOTTLE_POUCH_SLOT = u32::MAX;
        NUMBER_OF_ITEMS = 0;
        return item;
    }
}

#[no_mangle]
fn storyflag_set_to_1(flag: u16) {
    unsafe { FlagManager__setFlagTo1(STORYFLAG_MANAGER, flag) };
}

#[no_mangle]
fn get_start_info() -> *const StartInfo {
    // this is where the start entrance info is patched
    return unsafe { &*(0x802DA0E0 as *const StartInfo) };
}

#[no_mangle]
pub fn send_to_start() {
    let start_info = get_start_info();

    // we can't use the normal triggerEntrance function, because that doesn't work
    // properly when going from title screen to normal gameplay while keeping
    // the stage
    unsafe {
        actuallyTriggerEntrance(
            (*start_info).stage.as_ptr(),
            (*start_info).room,
            (*start_info).layer,
            (*start_info).entrance,
            (*start_info).forced_night,
            0,
            0,
            0xF,
            0xFF,
        );
        Reloader__setReloadTrigger(RELOADER_PTR, 5);
    }
}

#[no_mangle]
// args only used by replaced function call
pub fn do_er_fixes(room_mgr: *mut c_void, room_number: u32) {
    unsafe {
        if (*RELOADER_PTR).initial_speed > 30f32 {
            (*RELOADER_PTR).initial_speed = 30f32;
        }
    }
    let spawn = unsafe { &mut SPAWN_SLAVE };
    if spawn.name.starts_with(b"F000") && spawn.entrance == 53 && !storyflag_check(22) {
        // Skyloft from Sky Keep
        spawn.entrance = 52;
    } else if spawn.name.starts_with(b"F300\0") && spawn.entrance == 5 && !storyflag_check(8) {
        // Lanayru Desert from LMF - only if LMF isn't raised (storyflag 8)
        spawn.entrance = 19;
    } else if (spawn.name.starts_with(b"F300\0") && spawn.entrance == 2)
        || (spawn.name.starts_with(b"F300_1") && spawn.entrance == 1)
    {
        // desert from mines and mines from desert
        // there are 2 timeshift stones that are fine
        // 7 is sceneflagindex for desert
        if !(sceneflag_check_global(7, 113) || sceneflag_check_global(7, 114)) {
            for flag in (115..=124).chain([108, 111]) {
                sceneflag_unset_global(7, flag);
            }
            // last timeshift stone in mines
            sceneflag_set_global(7, 113);
        }
    }

    if unsafe { FORCE_MOGMA_CAVE_DIVE } && spawn.name.starts_with(b"F210") && spawn.entrance == 0 {
        unsafe {
            (*RELOADER_PTR).spawn_state = 0x13; // diving
        }
    }

    // replaced function call
    unsafe {
        RoomManager__getRoomByIndex(room_mgr, room_number);
    }
}

#[no_mangle]
fn allow_set_respawn_info() -> *mut Reloader {
    unsafe {
        if IS_FILE_START {
            (*RELOADER_PTR).prevent_save_respawn_info = false;
            IS_FILE_START = false;
        }

        return RELOADER_PTR;
    }
}

#[no_mangle]
fn get_glow_color(item_id: u32) -> u32 {
    let stage = unsafe { &SPAWN_SLAVE.name[..4] };
    // only proceed if in a silent realm
    if stage[0] == b'S' {
        // exclude stamina fruit, light fruit, and dusk relics
        if (item_id != 42) && (item_id != 47) && (item_id != 168) {
            if (item_id > 42) && (item_id < 47) {
                // item is a tear; keep the correct id
                // skyloft is subtype 3, faron 0, eldin 1, lanayru 2
                return ((stage[1] as u32) + 3) & 3;
            }
            // offset the color by 2 so items look distinct from tears
            return ((stage[1] as u32) + 1) & 3;
        }
    }
    4
}

// // Below is Code i Used to test menus (Not what is going to be final at all)
// struct MenuCursors {
//     sample_menu:     u32,
//     sample_sub_menu: u32,
// }

// #[derive(Clone, Copy, PartialEq, Eq)]
// enum MenuActive {
//     MenuNone,
//     MenuSample,
//     MenuSampleSub,
// }
// #[link_section = "data"]
// #[no_mangle]
// static mut MENU_CURSORS: MenuCursors = MenuCursors {
//     sample_menu:     0,
//     sample_sub_menu: 0,
// };
// #[link_section = "data"]
// #[no_mangle]
// static mut MENU_ACTIVE: MenuActive = MenuActive::MenuNone;

// fn check_menu_input() {
//     let up_pressed = is_pressed(DPAD_UP);
//     let down_pressed = is_pressed(DPAD_DOWN);
//     let right_held = is_down(DPAD_RIGHT);
//     let b_pressed = is_pressed(B);
//     let a_pressed = is_pressed(A);
//     let c_held = is_down(C);
//     let b1_held = is_down(ONE);
//     let b2_held = is_down(TWO);

//     let mut next_menu = unsafe { MENU_ACTIVE };

//     match unsafe { MENU_ACTIVE } {
//         MenuActive::MenuNone => {
//             if b2_held && right_held {
//                 next_menu = MenuActive::MenuSample;
//             }
//         },
//         MenuActive::MenuSample => {
//             if b_pressed {
//                 next_menu = MenuActive::MenuNone;
//             } else if a_pressed {
//                 match unsafe { MENU_CURSORS.sample_menu } {
//                     3 => next_menu = MenuActive::MenuSampleSub,
//                     _ => {},
//                 }
//             } else if up_pressed {
//                 unsafe {
//                     MENU_CURSORS.sample_menu = (MENU_CURSORS.sample_menu +
// 3) % 4;                 } } else if down_pressed { unsafe {
//    MENU_CURSORS.sample_menu = (MENU_CURSORS.sample_menu +
// 1) % 4;                 } } }, MenuActive::MenuSampleSub => { if b_pressed {
//    next_menu = MenuActive::MenuSample; } else if a_pressed { match unsafe {
//    MENU_CURSORS.sample_sub_menu } { 0 => { send_to_start(); next_menu =
//    MenuActive::MenuNone; }, _ => {}, } } }, } unsafe { if MENU_ACTIVE !=
//    next_menu { MENU_ACTIVE = next_menu; } }
// }
// fn display_menus() {
//     match unsafe { MENU_ACTIVE } {
//         MenuActive::MenuNone => {},
//         MenuActive::MenuSample => {
//             let mut menu = SimpleMenu::<10, 20>::new(10, 10, 10, "Sample
// Menu\n");             menu.current_line = unsafe { MENU_CURSORS.sample_menu
// };             menu.add_entry("Option 1\n");
//             menu.add_entry("Option 2\n");
//             menu.add_entry("Option 3\n");
//             menu.add_entry("Load\n");
//             menu.draw();
//         },
//         MenuActive::MenuSampleSub => {
//             let mut menu = SimpleMenu::<10, 20>::new(10, 10, 10, "Sample Sub
// Menu\n");             menu.current_line = unsafe {
// MENU_CURSORS.sample_sub_menu };             menu.add_entry("Warp To
// Start\n");             menu.draw();
//         },
//     }
// }

// A Common Place where Custom code can be injected to run once per frame
// Returns whether or not to stop (0 == continue)
// Its current by changing r31 we can stop the game :D
#[no_mangle]
fn custom_main_additions(in_r31: u32) -> u32 {
    // if in_r31 == 0 {
    //     check_menu_input();
    //     display_menus();
    // }
    // match unsafe { MENU_ACTIVE } {
    //     MenuActive::MenuNone => in_r31,
    // _ => 1,
    // }
    // write_text_on_screen(); // Example Function
    return in_r31;
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
