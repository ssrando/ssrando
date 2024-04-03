use arrayvec::ArrayVec;

use crate::game::{arc::OarcManager, item::get_item_arc_names_for_item};

#[link_section = "data"]
// it's always sorted, can have duplicates
static mut DYNAMIC_LOADED_ITEM_ID_ARCS: ArrayVec<u16, 0x20> = ArrayVec::new_const();

pub fn load_arcs_for_item(item_id: u16) {
    let arc_names = get_item_arc_names_for_item(item_id);
    if !arc_names.is_empty() {
        let dynamic_loaded_item_id_arcs = unsafe { &mut DYNAMIC_LOADED_ITEM_ID_ARCS };
        let search = dynamic_loaded_item_id_arcs.binary_search(&item_id);
        let pos = match search {
            Ok(x) => x,
            Err(x) => x,
        };
        dynamic_loaded_item_id_arcs.insert(pos, item_id);
        // increment ref count either way
        for arc in &arc_names {
            OarcManager.load_object_arc_from_disc(*arc);
        }
    }
}

#[no_mangle]
pub extern "C" fn check_arcs_loaded(item_id: u16) -> bool {
    get_item_arc_names_for_item(item_id)
        .iter()
        .all(|arc| OarcManager.ensure_loaded(*arc) == 0)
}

pub fn unload_arcs_for_item(item_id: u16) {
    let dynamic_loaded_item_id_arcs = unsafe { &mut DYNAMIC_LOADED_ITEM_ID_ARCS };
    if let Ok(idx) = dynamic_loaded_item_id_arcs.binary_search(&item_id) {
        dynamic_loaded_item_id_arcs.remove(idx);
        for arc in &get_item_arc_names_for_item(item_id) {
            OarcManager.decement_ref_count(*arc);
        }
    }
}

#[no_mangle]
pub extern "C" fn unload_all_arcs() {
    let dynamic_loaded_item_id_arcs = unsafe { &mut DYNAMIC_LOADED_ITEM_ID_ARCS };
    for chest_loaded_item_id in dynamic_loaded_item_id_arcs.iter() {
        for arc in &get_item_arc_names_for_item(*chest_loaded_item_id) {
            OarcManager.decement_ref_count(*arc);
        }
    }
    dynamic_loaded_item_id_arcs.clear();
}

#[link_section = "data"]
static mut TBOX_LOADED_ITEM_ARC: Option<u16> = None;

#[no_mangle]
pub extern "C" fn load_arcs_for_tbox_item_get(item_id: u16) {
    unsafe { TBOX_LOADED_ITEM_ARC = Some(item_id) };
    load_arcs_for_item(item_id);
}

#[no_mangle]
pub extern "C" fn unload_arcs_after_tbox_item_get(item_id: u16) -> u32 {
    if let Some(tbox_item_id) = unsafe { TBOX_LOADED_ITEM_ARC } {
        if tbox_item_id == item_id {
            unload_arcs_for_item(item_id);
        }
    }
    1
}
