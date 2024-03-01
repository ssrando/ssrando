#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]

use crate::system::math::Vec3f;
use core::ffi::{c_char, c_int, c_short, c_uchar, c_uint, c_ushort};

#[repr(C)]
#[derive(Copy, Clone)]
pub struct SaveFile {
    pub field_0x0:               [u8; 8usize],
    pub savedTimeHi:             c_int,
    pub savedTimeLo:             c_int,
    pub pos_t1:                  Vec3f,
    pub pos_t2:                  Vec3f,
    pub pos_t3:                  Vec3f,
    pub beaconPositions:         [[Vec3f; 5usize]; 32usize],
    pub beedleShopPathSegment:   c_int,
    pub beedleShopPathSegFrac:   f32,
    pub field_0x7bc:             [u8; 4usize],
    pub pouch_items:             [c_int; 8usize],
    pub item_check_items:        [c_int; 60usize],
    pub file_area_index:         c_int,
    pub file_hero_name:          [c_ushort; 8usize],
    pub storyFlags:              [c_ushort; 128usize],
    pub item_flags:              [c_ushort; 64usize],
    pub dungeon_flags:           [[c_ushort; 22usize]; 8usize],
    pub field_0xbc4:             [u8; 3744usize],
    pub scene_flags:             [c_ushort; 208usize],
    pub field_0x1c04:            [u8; 3680usize],
    pub tboxFlags:               u8,
    pub field_0x2a65:            [u8; 1279usize],
    pub enemyKillCounters:       [c_ushort; 100usize],
    pub field8733_0x302c:        [c_ushort; 100usize],
    pub temp_flags:              [c_ushort; 4usize],
    pub zone_flags:              [c_ushort; 252usize],
    pub field_0x32f4:            [u8; 8192usize],
    pub airPotionTimer:          c_short,
    pub airPotionPlusTimer:      c_short,
    pub staminaPotionTimer:      c_short,
    pub staminaPotionPlusTimer:  c_short,
    pub guardianPotionTimer:     c_short,
    pub guardianPotionPlusTimer: c_short,
    pub field_0x5300:            [u8; 2usize],
    pub health_capacity:         c_ushort,
    pub unusedHeartRelated:      u16,
    pub current_health:          c_ushort,
    pub load_room_t1:            u16,
    pub field_0x530a:            [u8; 2usize],
    pub room_load_t3:            c_short,
    pub angle_t1:                c_short,
    pub angle_t2:                c_short,
    pub angle_t3:                c_short,
    pub beedleShopRotation:      c_short,
    pub field_0x5316:            [u8; 2usize],
    pub sceneflag_index:         c_short,
    pub field_0x531a:            [u8; 2usize],
    pub area_t1:                 [c_char; 32usize],
    pub area_t2:                 [c_char; 32usize],
    pub area_t3:                 [c_char; 32usize],
    pub placedBeaconFlags:       [u8; 32usize],
    pub skykeep_puzzle:          [u8; 9usize],
    pub forced_layer_t1:         u8,
    pub forced_layer_t2:         u8,
    pub forced_layer_t3:         u8,
    pub entrance_t1:             u8,
    pub entrance_t1_load_flag:   u8,
    pub entrance_t2:             u8,
    pub entrance_t3:             u8,
    pub field_0x53ac:            [u8; 1usize],
    pub new_file:                u8,
    pub equipped_b_item:         u8,
    pub field_0x53af:            [u8; 1usize],
    pub lastUsedPouchItemSlot:   u8,
    pub shield_pouch_slot:       u8,
    pub selectedDowsingSlot:     DowsingSlotIndex,
    pub night_t1:                u8,
    pub night_t3:                u8,
    pub field_0x53b5:            [u8; 7usize],
    pub checksum:                u32,
}

#[repr(C)]
#[derive(Copy, Clone)]
pub struct SavedSaveFiles {
    pub field_0x0: [u8; 32usize],
    pub saveFiles: [SaveFile; 3usize],
}

#[repr(u8)] // bindgen got this wrong
#[derive(Copy, Clone, Hash, PartialEq, Eq)]
pub enum DowsingSlotIndex {
    STORY_EVENT_DOWSING = 0,
    RUPEE_DOWSING       = 1,
    QUEST_DOWSING       = 2,
    CRYSTAL_DOWSING     = 3,
    HEART_DOWSING       = 4,
    CUBE_DOWSING        = 5,
    LOOK                = 6,
    TREASURE_DOWSING    = 7,
    NO_DOWSING          = 8,
}
