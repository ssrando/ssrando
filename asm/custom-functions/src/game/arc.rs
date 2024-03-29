use core::{
    ffi::{c_char, c_void},
    ptr::null,
};

use crate::system::heap::Heap;

extern "C" {
    fn getModelDataFromOarc(oarc_mgr: *const c_void, oarc_str: *const c_char) -> *const c_void;
    fn loadObjectArcFromDisk(
        oarc_mgr: *const c_void,
        oarc_name: *const c_char,
        heap: *const Heap,
    ) -> bool;
    fn ArcManager__ensureLoaded(oarc_mgr: *const c_void, oarc_name: *const c_char) -> i32;
    fn ArcManager__decrementRefCount(oarc_mgr: *const c_void, oarc_name: *const c_char) -> bool;
    fn ArcManager__findEntryData(
        oarc_mgr: *const c_void,
        oarc_name: *const c_char,
    ) -> *const c_void;
    static OARC_MANAGER: *mut c_void;
}

pub fn get_model_data(oarc_mgr: *const c_void, oarc_str: *const c_char) -> *const c_void {
    unsafe { getModelDataFromOarc(oarc_mgr, oarc_str) }
}

pub struct OarcManager;

impl OarcManager {
    fn get_ptr() -> *mut c_void {
        unsafe { OARC_MANAGER }
    }
    pub fn load_object_arc_from_disc(&self, oarc_name: *const c_char) -> bool {
        unsafe { loadObjectArcFromDisk(Self::get_ptr(), oarc_name, null()) }
    }
    pub fn ensure_loaded(&self, oarc_name: *const c_char) -> i32 {
        unsafe { ArcManager__ensureLoaded(Self::get_ptr(), oarc_name) }
    }
    pub fn decement_ref_count(&self, oarc_name: *const c_char) -> bool {
        unsafe { ArcManager__decrementRefCount(Self::get_ptr(), oarc_name) }
    }
    pub fn find_entry_data(&self, oarc_name: *const c_char) -> *const c_void {
        unsafe { ArcManager__findEntryData(Self::get_ptr(), oarc_name) }
    }
}
