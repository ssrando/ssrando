use core::ffi::{c_char, c_void};

extern "C" {
    fn getModelDataFromOarc(oarc_mgr: *const c_void, oarc_str: *const c_char) -> *const c_void;
}

pub fn get_model_data(oarc_mgr: *const c_void, oarc_str: *const c_char) -> *const c_void {
    unsafe { getModelDataFromOarc(oarc_mgr, oarc_str) }
}
