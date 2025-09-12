use core::ffi::c_void;

use crate::game::flag_managers::Itemflag;
use crate::system::math::*;

extern "C" {
    static mut ITEM_GET_BOTTLE_POUCH_SLOT: u32;
    static mut NUMBER_OF_ITEMS: u32;

    fn getKeyPieceCount() -> u16;
    fn AcItem__setFlagForItem(itemflag: u16);
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
    pub fn spawnDrop(itemid: Itemflag, roomid: u32, pos: *mut Vec3f, rot: *mut Vec3s);
    pub fn setItemFlag(itemid: Itemflag);
}

pub fn get_bottle_pouch_slot() -> u32 {
    unsafe { ITEM_GET_BOTTLE_POUCH_SLOT }
}

pub fn set_bottle_pouch_slot(val: u32) {
    unsafe { ITEM_GET_BOTTLE_POUCH_SLOT = val };
}

pub fn get_number_of_items() -> u32 {
    unsafe { NUMBER_OF_ITEMS }
}

pub fn set_number_of_items(val: u32) {
    unsafe { NUMBER_OF_ITEMS = val };
}

pub fn get_key_piece_count() -> u16 {
    unsafe { getKeyPieceCount() }
}

pub fn spawn_item(
    room: u32,
    item_params: u32,
    pos: u32,   // actually Vec3f
    rot: u32,   // actually Vec3s
    scale: u32, // actually Vec3f
    params2: u32,
    unk: u32,
) -> *mut c_void {
    unsafe { AcItem__spawnItem(room, item_params, pos, rot, scale, params2, unk) }
}

pub fn setup_item_params(
    item_id: u16,
    subtype: u32,
    unk1: u32,
    sceneflag: u32,
    unk2: u32,
    unk3: u32,
) -> u32 {
    unsafe { AcItem__setupItemParams(item_id, subtype, unk1, sceneflag, unk2, unk3) }
}

pub fn set_flag_for_item(itemflag: u16) {
    unsafe { AcItem__setFlagForItem(itemflag) };
}

pub fn set_item_flag(itemid: Itemflag) {
    unsafe { setItemFlag(itemid) };
}
