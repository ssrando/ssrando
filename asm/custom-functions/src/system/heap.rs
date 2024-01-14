#![allow(non_snake_case)]
use core::ffi::{c_char, c_void, CStr};

#[repr(C)]
pub struct List {
    pub head:   u32,
    pub tail:   u32,
    pub count:  u16,
    pub offset: u16,
}

#[repr(C)]
pub struct Heap {
    pub vtable:       *const c_void,
    pub contain_heap: *mut Heap,
    pub link:         [u32; 2], // node
    pub heap_handle:  u32,      // MEMiHeapHead*
    pub parent_block: *mut c_void,
    pub flag:         u16,
    pub __pad:        u16,
    pub node:         [u32; 2], // node
    pub children:     List,
    pub name:         *const c_char,
}

impl Heap {
    pub fn get_name(&self) -> &CStr {
        unsafe { CStr::from_ptr(self.name) }
    }
}

extern "C" {
    static mut CURRENT_HEAP: *mut Heap;
    static HEAP_MEM1: *mut Heap;
    static HEAP_MEM2: *mut Heap;
    fn Heap__alloc(size: u32, align: u32, heap: *const Heap) -> *mut c_void;
}

pub fn get_root_heap_mem1() -> *mut Heap {
    unsafe { HEAP_MEM1 }
}

pub fn get_root_heap_mem2() -> *mut Heap {
    unsafe { HEAP_MEM2 }
}
