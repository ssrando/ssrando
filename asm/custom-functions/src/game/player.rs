use core::ffi::c_void;

#[repr(C)]
pub struct ActorLink {
    pub base_base:      [u8; 0x60 - 0x00],
    pub vtable:         u32,
    pub obj_base_pad0:  [u8; 0x5C],
    pub pos_x:          f32,
    pub pos_y:          f32,
    pub pos_z:          f32,
    pub obj_base_pad:   [u8; 0x330 - (0x64 + 0x5C + 0xC)],
    pub pad01:          [u8; 0x4498 - 0x330],
    pub stamina_amount: u32,
    // More after
}
extern "C" {
    static LINK_PTR: *mut ActorLink;
    fn checkXZDistanceFromLink(actor: *const c_void, distance: f32) -> bool;
}

pub fn get_ptr() -> *mut ActorLink {
    unsafe { LINK_PTR }
}

pub fn check_distance_from(actor: *const c_void, distance: f32) -> bool {
    unsafe { checkXZDistanceFromLink(actor, distance) }
}
