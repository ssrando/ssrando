use core::{
    ffi::{c_char, c_void, CStr},
    fmt::Debug,
};

use arrayvec::ArrayVec;

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
    static ITEM_TO_MODEL_INDEX: [u16; 512];
    static ITEM_MODEL_INDEX: [u8; 168];
    static ITEM_MODEL_DEFS: [ItemModelDef; 106];
    static MODEL_ID_TO_PUT_ITEM_MODEL_IDX: [u8; 168];
    static PUT_ITEM_MODEL_NAMES: [PutItemModelNameDef; 10];
    static GET_SHIELD_MODEL_INDEX: [u8; 168];
    static GET_SHIELD_MODEL_NAMES: [GetShieldStruct; 9];
    static GET_BOTTLE_MODEL_INDEX: [u8; 168];
    static GET_BOTTLE_MODEL_NAMES: [GetBottleNameDef; 8];
    static GET_POTION_BOTTLE_MODEL_INDEX: [u8; 168];
    static GET_POTION_BOTTLE_DEFS: [GetPotionBottleNameDef; 4];
}

#[repr(C)]
pub struct ItemModelDef {
    pub arc_name:   *const c_char,
    pub model_name: *const c_char,
}

#[repr(C)]
pub struct PutItemModelNameDef {
    pub put_arc_name:   *const c_char,
    pub put_model_name: *const c_char,
    pub get_arc_name:   *const c_char,
    pub get_model_name: *const c_char,
}

#[repr(C)]
pub struct GetShieldStruct {
    pub unk:        f32,
    pub arc_name:   *const c_char,
    pub model_name: *const c_char,
    pub equip_name: *const c_char,
}

#[repr(C)]
pub struct GetBottleNameDef {
    pub arc_name:   *const c_char,
    pub model_name: *const c_char,
    pub equip_name: *const c_char,
}

#[repr(C)]
pub struct GetPotionBottleNameDef {
    pub name1: *const c_char,
    pub name2: *const c_char,
    pub name3: *const c_char,
    pub name4: *const c_char,
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

pub fn get_item_model_def_for_item(item_id: u16) -> Option<&'static ItemModelDef> {
    unsafe {
        ITEM_TO_MODEL_INDEX
            .get(item_id as usize)
            .and_then(|model| ITEM_MODEL_INDEX.get(*model as usize))
            .and_then(|model| ITEM_MODEL_DEFS.get(*model as usize))
    }
}
pub enum ArcNames {
    None,
    One([*const c_char; 1]),
    Two([*const c_char; 2]),
}

impl ArcNames {
    pub fn slice(&self) -> &[*const c_char] {
        match self {
            ArcNames::None => &[],
            ArcNames::One(x) => x,
            ArcNames::Two(x) => x,
        }
    }
}

impl Debug for ArcNames {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        match self {
            ArcNames::None => f.write_str("None"),
            ArcNames::One([name]) => {
                let s = unsafe { CStr::from_ptr(*name).to_str().unwrap_unchecked() };
                f.write_fmt(format_args!("One({s})"))
            },
            ArcNames::Two([name1, name2]) => {
                let s1 = unsafe { CStr::from_ptr(*name1).to_str().unwrap_unchecked() };
                let s2 = unsafe { CStr::from_ptr(*name2).to_str().unwrap_unchecked() };
                f.write_fmt(format_args!("Two({s1}, {s2})"))
            },
        }
    }
}

pub fn get_item_arc_names_for_item(item_id: u16) -> ArrayVec<*const c_char, 2> {
    fn single_arrayvec(s: *const c_char) -> ArrayVec<*const c_char, 2> {
        let mut v = ArrayVec::new();
        v.push(s);
        v
    }
    // custom rando models
    match item_id {
        214 => return single_arrayvec(cstr::cstr!("Onp").as_ptr()), // tadtone
        215 => return single_arrayvec(cstr::cstr!("DesertRobot").as_ptr()), // scrapper
        _ => (),
    }
    unsafe {
        if let Some(model_idx) = ITEM_TO_MODEL_INDEX.get(item_id as usize).copied() {
            // dummy entry
            if model_idx == 0xA7 {
                return ArrayVec::new();
            }
            if let Some(item_model_def) = ITEM_MODEL_INDEX
                .get(model_idx as usize)
                .and_then(|model| ITEM_MODEL_DEFS.get(*model as usize))
            {
                return single_arrayvec(item_model_def.arc_name);
            }
            if let Some(put_model_def) = MODEL_ID_TO_PUT_ITEM_MODEL_IDX
                .get(model_idx as usize)
                .and_then(|model| PUT_ITEM_MODEL_NAMES.get(*model as usize))
            {
                return ArrayVec::from([put_model_def.put_arc_name, put_model_def.get_arc_name]);
            }
            if let Some(shield_model_def) = GET_SHIELD_MODEL_INDEX
                .get(model_idx as usize)
                .and_then(|model| GET_SHIELD_MODEL_NAMES.get(*model as usize))
            {
                return single_arrayvec(shield_model_def.arc_name);
            }
            if let Some(bottle_model_def) = GET_BOTTLE_MODEL_INDEX
                .get(model_idx as usize)
                .and_then(|model| GET_BOTTLE_MODEL_NAMES.get(*model as usize))
            {
                return single_arrayvec(bottle_model_def.arc_name);
            }
            if let Some(potion_model_def) = GET_POTION_BOTTLE_MODEL_INDEX
                .get(model_idx as usize)
                .and_then(|model| GET_POTION_BOTTLE_DEFS.get(*model as usize))
            {
                return single_arrayvec(potion_model_def.name1);
            }
        }
    }
    ArrayVec::new()
}
