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
pub struct HeapVtable {
    pub rtti:                 [u32; 2],
    pub dtor:                 u32,
    pub get_heap_kind:        extern "C" fn(*const Heap) -> u32,
    pub init_allocator:       u32,
    pub alloc:
        extern "C" fn(*const Heap, c_uint /* size */, c_int /* align */) -> *mut c_void,
    pub free:                 extern "C" fn(*const Heap, *const c_void),
    pub destroy:              extern "C" fn(*const Heap),
    pub resize_for_m_block:
        extern "C" fn(*const Heap, *const c_void, c_uint /* size */) -> u32,
    pub get_total_free_size:  extern "C" fn(*const Heap) -> u32,
    pub get_allocatable_size: extern "C" fn(*const Heap, c_int /* align */) -> u32,
    pub adjust:               extern "C" fn(*const Heap) -> u32,
}

#[repr(C)]
pub struct Heap {
    pub vtable:       *const HeapVtable,
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

    pub fn get_heap_kind(&self) -> u32 {
        unsafe { ((*self.vtable).get_heap_kind)(self as *const Heap) }
    }

    pub fn alloc(&self, size: c_uint, align: c_int) -> *mut c_void {
        unsafe { ((*self.vtable).alloc)(self as *const Heap, size, align) }
    }

    pub fn free(&self, ptr: *const c_void) {
        unsafe { ((*self.vtable).free)(self as *const Heap, ptr) }
    }

    pub fn resize_for_m_block(&self, ptr: *const c_void, size: c_uint) -> u32 {
        unsafe { ((*self.vtable).resize_for_m_block)(self as *const Heap, ptr, size) }
    }

    pub fn get_total_free_size(&self) -> u32 {
        unsafe { ((*self.vtable).get_total_free_size)(self as *const Heap) }
    }

    pub fn get_allocatable_size(&self, align: c_int) -> u32 {
        unsafe { ((*self.vtable).get_allocatable_size)(self as *const Heap, align) }
    }

    pub fn adjust(&self) -> u32 {
        unsafe { ((*self.vtable).adjust)(self as *const Heap) }
    }
}

extern "C" {
    static mut CURRENT_HEAP: *mut Heap;
    static HEAP_MEM1: *mut Heap;
    static HEAP_MEM2: *mut Heap;

    static HEAP_WORK1: *mut Heap;
    static HEAP_WORK2: *mut Heap;
    static HEAP_WORK_EX: *mut Heap;
    static HEAP_LAYOUT: *mut Heap;
    static HEAP_LAYOUT_EX: *mut Heap;
    static HEAP_LAYOUT_EX2: *mut Heap;
    static HEAP_LAYOUT_RES: *mut Heap;
    static HEAP_FONT: *mut Heap;
    static HEAP_HBM: *mut Heap;
    static HEAP_ACTORS: [*mut Heap; 4];
    fn Heap__alloc(size: c_uint, align: c_int, heap: *mut Heap) -> *mut c_void;
    fn Heap__free(ptr: *const c_void, heap: *mut Heap);
}

pub fn get_root_heap_mem1() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_MEM1) }
}

pub fn get_root_heap_mem2() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_MEM2) }
}

pub fn get_work1_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_WORK1) }
}

pub fn get_work2_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_WORK2) }
}

pub fn get_work_ex_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_WORK_EX) }
}

pub fn get_layout_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_LAYOUT) }
}

pub fn get_layout_ex_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_LAYOUT_EX) }
}

pub fn get_layout_ex2_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_LAYOUT_EX2) }
}

pub fn get_layout_res_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_LAYOUT_RES) }
}

pub fn get_font_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_FONT) }
}

pub fn get_hbm_heap() -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_HBM) }
}

pub fn get_actor_heap(index: usize) -> WiiHeapAllocator {
    unsafe { WiiHeapAllocator(HEAP_ACTORS[index]) }
}

#[derive(Clone, Copy)]
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

    unsafe fn grow(
        &self,
        ptr: NonNull<u8>,
        old_layout: core::alloc::Layout,
        new_layout: core::alloc::Layout,
    ) -> Result<NonNull<[u8]>, core::alloc::AllocError> {
        // this doesn't move the pointer, if the allocation doesn't fit
        // it returns 0
        let new_size =
            unsafe { (*self.0).resize_for_m_block(ptr.as_ptr().cast(), new_layout.size() as u32) };
        if new_size as usize >= new_layout.size() {
            return Ok(NonNull::slice_from_raw_parts(ptr, new_layout.size()));
        }
        // alloc, copy then dealloc
        let new_ptr = self.allocate(new_layout)?;

        unsafe {
            core::ptr::copy_nonoverlapping(ptr.as_ptr(), new_ptr.as_mut_ptr(), old_layout.size());
            self.deallocate(ptr, old_layout);
        }

        Ok(new_ptr)
    }

    unsafe fn shrink(
        &self,
        ptr: NonNull<u8>,
        _old_layout: core::alloc::Layout,
        new_layout: core::alloc::Layout,
    ) -> Result<NonNull<[u8]>, core::alloc::AllocError> {
        // this never moves the pointer and should always work since we're shrinking
        let _new_size =
            unsafe { (*self.0).resize_for_m_block(ptr.as_ptr().cast(), new_layout.size() as u32) };
        Ok(NonNull::slice_from_raw_parts(ptr, new_layout.size()))
    }
}

impl WiiHeapAllocator {
    pub fn name(&self) -> &CStr {
        unsafe { (*self.0).get_name() }
    }

    pub fn get_heap_kind(&self) -> u32 {
        unsafe { (*self.0).get_heap_kind() }
    }

    pub fn get_total_free_size(&self) -> u32 {
        unsafe { (*self.0).get_total_free_size() }
    }

    pub fn get_allocatable_size(&self, align: c_int) -> u32 {
        unsafe { (*self.0).get_allocatable_size(align) }
    }

    pub fn get_flag(&self) -> u16 {
        unsafe { (*self.0).flag }
    }
}

#[global_allocator]
static DEFAULT_ALLOC: DefaultGlobalAllocator = DefaultGlobalAllocator;

pub struct DefaultGlobalAllocator;

unsafe impl GlobalAlloc for DefaultGlobalAllocator {
    unsafe fn alloc(&self, layout: core::alloc::Layout) -> *mut u8 {
        Heap__alloc(layout.size() as c_uint, layout.align() as c_int, null_mut()).cast()
    }

    unsafe fn dealloc(&self, ptr: *mut u8, _layout: core::alloc::Layout) {
        Heap__free(ptr.cast(), null_mut())
    }
}
