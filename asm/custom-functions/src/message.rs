use core::ffi::{c_int, c_void};

#[repr(C)]
pub struct FlowElement {
    pub typ: u8,
    pub sub_type: u8,
    pub pad: u16,
    pub param1: u16,
    pub param2: u16,
    pub param3: u16,
    pub next: u16,
    pub param4: u16,
    pub param5: u16,
}

// opaque
#[repr(C)]
pub struct TextManager {
    pad: u8,
}

#[repr(C)]
pub struct LytMsgWindow {
    pad: [u8; 0x724],
    pub text_manager: *mut TextManager,
}

pub fn text_manager_set_num_args(args: &[u32]) {
    unsafe {
        TextManager__setNumericArgs(
            (*LYT_MSG_MANAGER).text_manager,
            args.as_ptr(),
            args.len() as u32,
        )
    };
}

pub fn text_manager_set_string_arg(arg: *const c_void, num: u32) {
    unsafe { TextManager__setStringArg((*LYT_MSG_MANAGER).text_manager, arg, num) };
}

extern "C" {
    static LYT_MSG_MANAGER: *mut LytMsgWindow;
    fn TextManager__setStringArg(mgr: *mut TextManager, arg: *const c_void, num: u32);
    fn TextManager__setNumericArgs(mgr: *mut TextManager, args: *const u32, count: u32);
}
