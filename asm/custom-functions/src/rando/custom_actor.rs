use core::{
    ffi::{c_int, c_uint, c_void},
    mem::size_of,
    ptr::drop_in_place,
};

use crate::{
    println,
    system::{
        game_frame,
        math::{Vec3f, Vec3s},
    },
};

use super::item_arc_loader::{check_arcs_loaded, load_arcs_for_item, unload_arcs_for_item};

#[repr(C)]
pub struct BaseActor {
    unique_actor_number: u32,
    params:              u32,
    _0:                  [u8; 96 - 8],
    vtable:              u32,
    base_properties:     u32,
    _1:                  [u8; 68 - 4],
    param2:              u32,
    _2:                  [u8; 84 - 72],
    rotation:            Vec3s,
    _3:                  [u8; 2],
    pos:                 Vec3f,
    scale:               Vec3f,
    actor_properties:    u32,
    _4:                  [u8; 136 - 120],
    roomid:              u8,
    _5:                  [u8; 152 - 137],
}

extern "C" {
    fn fBase__operatorNew(size: c_uint) -> *mut c_void; // 0x802e23b0
    fn dBase_c__ctor(ac: *mut c_void); // 0x80050800
    fn dBase____dt(ptr: *mut c_void, destroy_bases: c_int); // 0x8002c530
    fn ActorBase__ctor(ac: *mut c_void);
    fn ActorBase__dtor(ptr: *mut c_void, destroy_bases: c_int);
    fn ActorBase__getDistToPlayer(ptr: *const BaseActor) -> f32; // 0x8002d470
    fn ActorBase__getSquareDistToPlayer(ptr: *const BaseActor) -> f32; // 0x8002d4a0
}

#[repr(C)]
struct RandoActorGlue {
    base:   BaseActor,
    custom: RandoCustomActor,
}

enum RandoCustomActor {
    BeforeInit,
    ArcLoader {
        item_id:          u16,
        has_loaded_item:  bool,
        load_start_frame: u32,
        load_end_frame:   u32,
    },
}

#[repr(C)]
struct RandoActorGlueVtable {
    rtti:                        [u32; 2],
    init:                        extern "C" fn(actor: *mut RandoActorGlue) -> c_int,
    pre_create:                  u32,
    post_create:                 u32,
    destroy:                     extern "C" fn(actor: *mut RandoActorGlue) -> c_int,
    pre_destroy:                 u32,
    post_destroy:                u32,
    update:                      extern "C" fn(actor: *mut RandoActorGlue) -> c_int,
    pre_update:                  u32,
    post_update:                 u32,
    draw:                        u32,
    pre_draw:                    u32,
    post_draw:                   u32,
    delete_ready:                u32,
    create_heap_with_adjust:     u32,
    create_heap_with_non_adjust: u32,
    init_models:                 u32,
    dtor:                        extern "C" fn(actor: *mut RandoActorGlue, destroy_bases: c_int),
    actor_init1:                 u32,
    actor_init2:                 u32,
    actor_update:                u32,
    actor_update_in_event:       u32,
    unk_0x5c:                    u32,
    unk_0x60:                    u32,
    restore_pos_rot:             u32,
    get_current_event_actor:     u32,
    unk_0x6c:                    u32,
    do_interaction:              u32,
}

// pretty much taken from TgBeltObstacle::vtable (0x80dce538)
static RANDO_ACTOR_GLUE_VTABLE: RandoActorGlueVtable = RandoActorGlueVtable {
    rtti:                        [0; 2],
    init:                        RandoActorGlue_init,
    pre_create:                  0x802E15D0,
    post_create:                 0x8002C8F0,
    destroy:                     RandoActorGlue_destroy,
    pre_destroy:                 0x8002C940,
    post_destroy:                0x802E17A0,
    update:                      RandoActorGlue_update,
    pre_update:                  0x8002CB10,
    post_update:                 0x8002CCC0,
    draw:                        0x8002C860,
    pre_draw:                    0x80050920,
    post_draw:                   0x80050860,
    delete_ready:                0x802E1B90,
    create_heap_with_adjust:     0x802E20E0,
    create_heap_with_non_adjust: 0x802E22E0,
    init_models:                 0x8002C3A0,
    dtor:                        RandoActorGlue_dtor,
    actor_init1:                 0x8002C860,
    actor_init2:                 0x8002C860,
    actor_update:                0x8002C860,
    actor_update_in_event:       0x8002C860,
    unk_0x5c:                    0x8002CE90,
    unk_0x60:                    0x8002CEA0,
    restore_pos_rot:             0x8002CEB0,
    get_current_event_actor:     0x8002DB80,
    unk_0x6c:                    0x8002DB90,
    do_interaction:              0x8002DBA0,
};

#[no_mangle]
extern "C" fn RandoActorGlue_ctor() -> *mut RandoActorGlue {
    unsafe {
        let ptr = fBase__operatorNew(size_of::<RandoActorGlue>() as u32) as *mut RandoActorGlue;
        ActorBase__ctor(ptr.cast());
        (*ptr).base.vtable = &RANDO_ACTOR_GLUE_VTABLE as *const _ as u32;
        (*ptr).custom = RandoCustomActor::BeforeInit;
        ptr.cast()
    }
}

#[no_mangle]
extern "C" fn RandoActorGlue_init(actor: *mut RandoActorGlue) -> c_int {
    unsafe {
        (*actor).custom.init(&mut (*actor).base);
    }
    1
}

#[no_mangle]
extern "C" fn RandoActorGlue_update(actor: *mut RandoActorGlue) -> c_int {
    unsafe {
        (*actor).custom.update(&mut (*actor).base);
    }
    1
}

#[no_mangle]
extern "C" fn RandoActorGlue_destroy(actor: *mut RandoActorGlue) -> c_int {
    unsafe {
        (*actor).custom.destroy(&mut (*actor).base);
    }
    1
}

#[no_mangle]
extern "C" fn RandoActorGlue_dtor(actor: *mut RandoActorGlue, destroy_bases: c_int) {
    unsafe {
        drop_in_place(&mut (*actor).custom);
        ActorBase__dtor(actor.cast(), destroy_bases);
    }
}

impl RandoCustomActor {
    fn init(&mut self, base_actor: &mut BaseActor) {
        let subtype = base_actor.params & 0xFF;
        match subtype {
            0 => {
                let item_id = (base_actor.params >> 8) & 0xFFFF;
                *self = RandoCustomActor::ArcLoader {
                    item_id:          item_id as u16,
                    has_loaded_item:  false,
                    load_start_frame: 0,
                    load_end_frame:   0,
                };
            },
            _ => {},
        }
    }
    fn update(&mut self, base_actor: &mut BaseActor) {
        match self {
            RandoCustomActor::BeforeInit => {},
            RandoCustomActor::ArcLoader {
                item_id,
                has_loaded_item,
                load_start_frame,
                load_end_frame,
            } => {
                let sq_link_dist = unsafe { ActorBase__getSquareDistToPlayer(base_actor) };
                if *has_loaded_item {
                    if check_arcs_loaded(*item_id) && *load_end_frame == 0 {
                        *load_end_frame = game_frame();
                        println!(
                            "took {} frames to load {}",
                            *load_end_frame - *load_start_frame,
                            item_id
                        );
                    }
                    if sq_link_dist > 4000f32 * 4000f32 {
                        println!("now unloading {item_id}");
                        // it is now too far away, unload
                        unload_arcs_for_item(*item_id);
                        *has_loaded_item = false;
                        *load_end_frame = 0;
                        *load_start_frame = 0;
                    }
                } else {
                    if sq_link_dist < 2000f32 * 2000f32 {
                        println!("now loading {item_id}");
                        // it is now too near, load
                        load_arcs_for_item(*item_id);
                        *has_loaded_item = true;
                        if !check_arcs_loaded(*item_id) {
                            *load_start_frame = game_frame();
                        }
                    }
                }
            },
        }
    }
    fn destroy(&mut self, _base_actor: &mut BaseActor) {
        match self {
            RandoCustomActor::ArcLoader {
                item_id,
                has_loaded_item,
                ..
            } => {
                if *has_loaded_item {
                    unload_arcs_for_item(*item_id);
                }
            },
            _ => {},
        }
    }
}
