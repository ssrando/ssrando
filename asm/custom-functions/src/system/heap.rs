#![allow(non_snake_case)]
use core::{
    alloc::{Allocator, GlobalAlloc},
    ffi::{c_char, c_int, c_uint, c_void, CStr},
    ptr::{null_mut, NonNull},
};

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
    fn Heap__alloc(size: c_uint, align: c_int, heap: *mut Heap) -> *mut c_void;
    fn Heap__free(ptr: *const c_void, heap: *mut Heap);
}

pub fn get_root_heap_mem1() -> *mut Heap {
    unsafe { HEAP_MEM1 }
}

pub fn get_root_heap_mem2() -> *mut Heap {
    unsafe { HEAP_MEM2 }
}

pub struct WiiHeapAllocator(*mut Heap);

unsafe impl Allocator for WiiHeapAllocator {
    fn allocate(
        &self,
        layout: core::alloc::Layout,
    ) -> Result<core::ptr::NonNull<[u8]>, core::alloc::AllocError> {
        let ptr =
            unsafe { Heap__alloc(layout.size() as c_uint, layout.align() as c_int, self.0).cast() };
        let ret = core::ptr::NonNull::new(ptr).ok_or(core::alloc::AllocError)?;
        Ok(NonNull::slice_from_raw_parts(ret, layout.size()))
    }

    unsafe fn deallocate(&self, ptr: core::ptr::NonNull<u8>, _layout: core::alloc::Layout) {
        Heap__free(ptr.as_ptr().cast(), self.0);
    }

    fn allocate_zeroed(
        &self,
        layout: core::alloc::Layout,
    ) -> Result<NonNull<[u8]>, core::alloc::AllocError> {
        // the default is already zero allocating
        // TODO: is that actually true for all heaps?
        self.allocate(layout)
    }
}

pub struct DefaultGlobalAllocator;

unsafe impl GlobalAlloc for DefaultGlobalAllocator {
    unsafe fn alloc(&self, layout: core::alloc::Layout) -> *mut u8 {
        Heap__alloc(layout.size() as c_uint, layout.align() as c_int, null_mut()).cast()
    }

    unsafe fn dealloc(&self, ptr: *mut u8, _layout: core::alloc::Layout) {
        Heap__free(ptr.cast(), null_mut())
    }
}
