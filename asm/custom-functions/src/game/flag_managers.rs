#![allow(non_snake_case)]
use super::file_manager::{self};
use core::{
    ffi::{c_ushort, c_void},
    ptr::addr_of_mut,
};

#[repr(C)]
struct FlagSpace {
    flag_ptr:   *mut u16,
    flag_count: u16,
    pad:        u16,
    call_ptr:   u32,
}

#[repr(C)]
pub struct DungeonflagManager {
    pub should_commit: bool,
    pub flagindex:     c_ushort,
}
#[repr(C)]
pub struct StoryflagManager {
    tobefilled: u32,
}
#[repr(C)]
pub struct SceneflagManager {
    sceneflags:      FlagSpace,
    tempflags:       FlagSpace,
    zoneflags:       FlagSpace,
    m_flag_helper:   u8,
    unk1:            u8,
    pub scene_index: u8,
}
#[repr(C)]
pub struct ItemflagManager {
    tobefilled: u32,
}

extern "C" {
    fn FlagManager__setFlagTo1(mgr: *mut c_void, flag: u16);
    fn FlagManager__getFlagOrCounter(mgr: *mut c_void, flag: u16) -> u16;
    fn FlagManager__setFlagOrCounter(mgr: *mut c_void, flag: u16, value: u16);

    fn setStoryflagToValue(flag: u16, value: u16);
    static STORYFLAG_MANAGER: *mut StoryflagManager;
    static SCENEFLAG_MANAGER: *mut SceneflagManager;
    static ITEMFLAG_MANAGER: *mut ItemflagManager;
    static DUNGEONFLAG_MANAGER: *mut DungeonflagManager;
    static mut STATIC_STORYFLAGS: [c_ushort; 0x80];
    static mut STATIC_ITEMFLAGS: [c_ushort; 0x40];
    static mut STATIC_DUNGEON_FLAGS: [c_ushort; 8usize];
    fn SceneflagManager__setFlag(mgr: *mut SceneflagManager, roomid: u16, flag: u16);
    fn SceneflagManager__setFlagGlobal(mgr: *mut SceneflagManager, scene_index: u16, flag: u16);
    fn SceneflagManager__unsetFlagGlobal(mgr: *mut SceneflagManager, scene_index: u16, flag: u16);
    fn SceneflagManager__checkFlagGlobal(
        mgr: *mut SceneflagManager,
        scene_index: u16,
        flag: u16,
    ) -> bool;
    fn StoryflagManager__doCommit(mgr: *mut StoryflagManager);
    fn ItemflagManager__doCommit(mgr: *mut ItemflagManager);
    fn checkStoryflagIsSet(p: *const StoryflagManager, flag: u16) -> bool;
    fn AcItem__checkItemFlag(flag: u16) -> bool;

}

impl StoryflagManager {
    pub fn get_static() -> *mut [u16; 0x80] {
        addr_of_mut!(STATIC_STORYFLAGS)
    }
    pub fn do_commit() {
        unsafe { StoryflagManager__doCommit(STORYFLAG_MANAGER) };
    }
    pub fn check(flag: u16) -> bool {
        unsafe { checkStoryflagIsSet(core::ptr::null(), flag) }
    }
    pub fn get_value(flag: u16) -> u16 {
        unsafe { FlagManager__getFlagOrCounter(STORYFLAG_MANAGER as _, flag) }
    }
    pub fn set_to_value(flag: u16, value: u16) {
        unsafe { FlagManager__setFlagOrCounter(STORYFLAG_MANAGER as _, flag, value) };
    }
    #[no_mangle]
    pub fn storyflag_set_to_1(flag: u16) {
        unsafe { FlagManager__setFlagTo1(STORYFLAG_MANAGER as _, flag) };
    }
}

impl ItemflagManager {
    pub fn get_static() -> *mut [u16; 0x40] {
        addr_of_mut!(STATIC_ITEMFLAGS)
    }
    pub fn do_commit() {
        unsafe { ItemflagManager__doCommit(ITEMFLAG_MANAGER) };
    }
    pub fn check(flag: u16) -> bool {
        unsafe { AcItem__checkItemFlag(flag) }
    }
    pub fn set_to_value(flag: u16, value: u16) {
        unsafe { FlagManager__setFlagOrCounter(ITEMFLAG_MANAGER as _, flag, value) };
    }
}

impl SceneflagManager {
    pub fn set_local(flag: u16) {
        unsafe { SceneflagManager__setFlag(SCENEFLAG_MANAGER, 0, flag) }
    }
    pub fn check_global(scn_idx: u16, flag: u16) -> bool {
        unsafe { SceneflagManager__checkFlagGlobal(SCENEFLAG_MANAGER, scn_idx, flag) }
    }
    pub fn set_global(scn_idx: u16, flag: u16) {
        unsafe { SceneflagManager__setFlagGlobal(SCENEFLAG_MANAGER, scn_idx, flag) };
    }
    pub fn unset_global(scn_idx: u16, flag: u16) {
        unsafe { SceneflagManager__unsetFlagGlobal(SCENEFLAG_MANAGER, scn_idx, flag) };
    }
    pub fn get_flags() -> *const [u16] {
        let t = unsafe { &*SCENEFLAG_MANAGER };
        return core::ptr::slice_from_raw_parts::<u16>(
            t.sceneflags.flag_ptr,
            t.sceneflags.flag_count.into(),
        );
    }
}

impl DungeonflagManager {
    pub fn get_ptr() -> *mut DungeonflagManager {
        unsafe { DUNGEONFLAG_MANAGER }
    }
    /// returns the pointer to the static dungeonflags, those for the current
    /// sceneflagindex
    pub fn get_local() -> *mut [u16; 8] {
        addr_of_mut!(STATIC_DUNGEON_FLAGS)
    }
    pub fn get_global(scn_idx: u16) -> *mut [u16; 8] {
        unsafe {
            (*file_manager::get_dungeon_flags())
                .as_mut_ptr()
                .add(scn_idx as usize)
        }
    }
    pub fn get_global_key_count(scn_idx: u16) -> u16 {
        unsafe { (*Self::get_global(scn_idx))[1] & 0xF }
    }
}

// Flag enums
#[repr(u16)]
#[derive(Copy, Clone, Hash, PartialEq, Eq)]
#[allow(non_camel_case_types)]
pub enum Itemflag {
    CUPBOARD_TEXT                    = 0x0,
    SMALL_KEY                        = 0x1,
    GREEN_RUPEE                      = 0x2,
    BLUE_RUPEE                       = 0x3,
    RED_RUPEE                        = 0x4,
    COMPLETED_TRIFORCE               = 0x5,
    HEART                            = 0x6,
    SINGLE_ARROW                     = 0x7,
    BUNDLE_OF_ARROWS                 = 0x8,
    GODDESS_WHITE_SWORD              = 0x9,
    PRACTICE_SWORD                   = 0xA,
    GODDESS_SWORD                    = 0xB,
    GODDESS_LONGSWORD                = 0xC,
    MASTER_SWORD                     = 0xD,
    TRUE_MASTER_SWORD                = 0xE,
    SAILCLOTH                        = 0xF,
    GODDESS_HARP                     = 0x10,
    SPIRIT_VESSEL                    = 0x11,
    UNK18                            = 0x12,
    BOW                              = 0x13,
    CLAWSHOTS                        = 0x14,
    BIRD_STATUETTE                   = 0x15,
    COMMON_BUG                       = 0x16,
    UNCOMMON_BUG                     = 0x17,
    RARE_BUG                         = 0x18,
    ANCIENT_CISTERN_BOSS_KEY         = 0x19,
    FIRE_SANCTUARY_BOSS_KEY          = 0x1A,
    SANDSHIP_BOSS_KEY                = 0x1B,
    KEY_PIECE                        = 0x1C,
    SKYVIEW_BOSS_KEY                 = 0x1D,
    EARTH_TEMPLE_BOSS_KEY            = 0x1E,
    LANAYRU_MINING_FACILITY_BOSS_KEY = 0x1F,
    SILVER_RUPEE                     = 0x20,
    GOLD_RUPEE                       = 0x21,
    RUPOOR                           = 0x22,
    FIVE_GRATITUDE_CRYSTALS          = 0x23,
    GLITTERING_SPORES                = 0x24,
    UNK37                            = 0x25,
    UNK38                            = 0x26,
    UNK39                            = 0x27,
    FIVE_BOMBS                       = 0x28,
    TEN_BOMBS                        = 0x29,
    STAMINA_FRUIT                    = 0x2A,
    TEAR_OF_FARORE                   = 0x2B,
    TEAR_OF_DIN                      = 0x2C,
    TEAR_OF_NAYRU                    = 0x2D,
    SACRED_TEAR                      = 0x2E,
    LIGHT_FRUIT                      = 0x2F,
    ONE_GRATITUDE_CRYSTAL            = 0x30,
    GUST_BELLOWS                     = 0x31,
    DUNGEON_MAP_FI_TEXT              = 0x32,
    DUNGEON_MAP_EMPTY                = 0x33,
    SLINGSHOT                        = 0x34,
    BEETLE                           = 0x35,
    WATER                            = 0x36,
    MUSHROOM_SPORES                  = 0x37,
    DIGGING_MITTS                    = 0x38,
    FIVE_DEKU_SEEDS                  = 0x39,
    UNK58                            = 0x3A,
    UNK59                            = 0x3B,
    TEN_DEKU_SEEDS                   = 0x3C,
    COMMON_TREASURE                  = 0x3D,
    COMMON_TREASURE2                 = 0x3E,
    UNCOMMON_TREASURE                = 0x3F,
    RARE_TREASURE                    = 0x40,
    GUARDIAN_POTION                  = 0x41,
    GUARDIAN_POTION_PLUS             = 0x42,
    UNK67                            = 0x43,
    WATER_DRAGON_SCALE               = 0x44,
    UNK69                            = 0x45,
    BUG_MEDAL                        = 0x46,
    BUG_NET                          = 0x47,
    FAIRY_WITH_BUG_NET               = 0x48,
    UNK73                            = 0x49,
    SACRED_WATER                     = 0x4A,
    HOOK_BEETLE                      = 0x4B,
    QUICK_BEETLE                     = 0x4C,
    TOUGH_BEETLE                     = 0x4D,
    HEART_POTION                     = 0x4E,
    HEART_POTION_PLUS                = 0x4F,
    UNK80                            = 0x50,
    HEART_POTION_PLUS_PLUS           = 0x51,
    UNK82                            = 0x52,
    GUARDIAN_POTION_EMPTY            = 0x53,
    STAMINA_POTION                   = 0x54,
    STAMINA_POTION_PLUS              = 0x55,
    AIR_POTION                       = 0x56,
    AIR_POTION_PLUS                  = 0x57,
    FAIRY_IN_A_BOTTLE                = 0x58,
    UNK89                            = 0x59,
    IRON_BOW                         = 0x5A,
    SACRED_BOW                       = 0x5B,
    BOMB_BAG                         = 0x5C,
    HEART_CONTAINER                  = 0x5D,
    HEART_PIECE                      = 0x5E,
    TRIFORCE_OF_COURAGE              = 0x5F,
    TRIFORCE_OF_POWER                = 0x60,
    TRIFORCE_OF_WISDOM               = 0x61,
    SEA_CHART                        = 0x62,
    MOGMA_MITTS                      = 0x63,
    HEART_MEDAL                      = 0x64,
    RUPEE_MEDAL                      = 0x65,
    TREASURE_MEDAL                   = 0x66,
    POTION_MEDAL                     = 0x67,
    CURSED_MEDAL                     = 0x68,
    SCATTERSHOT                      = 0x69,
    UNK106                           = 0x6A,
    UNK107                           = 0x6B,
    MEDIUM_WALLET                    = 0x6C,
    BIG_WALLET                       = 0x6D,
    GIANT_WALLET                     = 0x6E,
    TYCOON_WALLET                    = 0x6F,
    ADVENTURE_POUCH                  = 0x70,
    POUCH_EXPANSION                  = 0x71,
    LIFE_MEDAL                       = 0x72,
    UNK115                           = 0x73,
    WOODEN_SHIELD                    = 0x74,
    BANDED_SHIELD                    = 0x75,
    BRACED_SHIELD                    = 0x76,
    IRON_SHIELD                      = 0x77,
    REINFORCED_SHIELD                = 0x78,
    FORTIFIED_SHIELD                 = 0x79,
    SACRED_SHIELD                    = 0x7A,
    DIVINE_SHIELD                    = 0x7B,
    GODDESS_SHIELD                   = 0x7C,
    HYLIAN_SHIELD                    = 0x7D,
    REVITALIZING_POTION              = 0x7E,
    REVITALIZING_POTION_PLUS         = 0x7F,
    SMALL_SEED_SATCHEL               = 0x80,
    MEDIUM_SEED_SATCHEL              = 0x81,
    LAGRE_SEED_SATCHEL               = 0x82,
    SMALL_QUIVER                     = 0x83,
    MEDIUM_QUIVER                    = 0x84,
    LARGE_QUIVER                     = 0x85,
    SMALL_BOMB_BAG                   = 0x86,
    MEDIUM_BOMB_BAG                  = 0x87,
    LARGE_BOMB_BAG                   = 0x88,
    WHIP                             = 0x89,
    FIRESHIELD_EARRINGS              = 0x8A,
    UNK139                           = 0x8B,
    BIG_BUG_NET                      = 0x8C,
    FARON_GRASSHOPPER                = 0x8D,
    WOODLAND_RHINO_BEETLE            = 0x8E,
    DEKU_HORNET                      = 0x8F,
    SKYLOFT_MANTIS                   = 0x90,
    VOLCANIC_LADYBUG                 = 0x91,
    BLESSED_BUTTERFLY                = 0x92,
    LANAYRU_ANT                      = 0x93,
    SAND_CICADA                      = 0x94,
    GERUDO_DRAGONFLY                 = 0x95,
    ELDIN_ROLLER                     = 0x96,
    SKY_STAG_BEETLE                  = 0x97,
    STARRY_FIREFLY                   = 0x98,
    EMPTY_BOTTLE                     = 0x99,
    RUPEE_MEDAL_                     = 0x9A,
    HEART_MEDAL_                     = 0x9B,
    UNK156                           = 0x9C,
    UNK157                           = 0x9D,
    CAWLIN_LETTER                    = 0x9E,
    BEEDLES_INSECT_CAGE              = 0x9F,
    RATTLE                           = 0xA0,
    HORNET_LAVAE                     = 0xA1,
    BIRD_FEATHER                     = 0xA2,
    TUMBLEWEED                       = 0xA3,
    LIZARD_TAIL                      = 0xA4,
    ELDIN_ORE                        = 0xA5,
    ANCIENT_FLOWER                   = 0xA6,
    AMBER_RELIC                      = 0xA7,
    DUSK_RELIC                       = 0xA8,
    JELLY_BLOB                       = 0xA9,
    MONSTER_CLAW                     = 0xAA,
    MONSTER_HORN                     = 0xAB,
    ORNAMENTAL_SKULL                 = 0xAC,
    EVIL_CRYSTAL                     = 0xAD,
    BLUE_BIRD_FEATHER                = 0xAE,
    GOLDEN_SKULL                     = 0xAF,
    GODDESS_PLUME                    = 0xB0,
    EMERALD_TABLET                   = 0xB1,
    RUBY_TABLET                      = 0xB2,
    AMBER_TABLET                     = 0xB3,
    STONE_OF_TRIALS                  = 0xB4,
    UNK181                           = 0xB5,
    UNK182                           = 0xB6,
    UNK183                           = 0xB7,
    UNK184                           = 0xB8,
    UNK185                           = 0xB9,
    BALLAD_OF_THE_GODDESS            = 0xBA,
    FARORE_COURAGE                   = 0xBB,
    NAYRU_WISDOM                     = 0xBC,
    DIN_POWER                        = 0xBD,
    FARON_SONG_OF_THE_HERO_PART      = 0xBE,
    ELDIN_SONG_OF_THE_HERO_PART      = 0xBF,
    LANAYRU_SONG_OF_THE_HERO_PART    = 0xC0,
    SONG_OF_THE_HERO                 = 0xC1,
    REVITALIZING_POTION_PLUS_PLUS    = 0xC2,
    HOT_PUMPKIN_SOUP                 = 0xC3,
    COLD_PUMPKIN_SOUP                = 0xC4,
    LIFE_TREE_SEEDLING               = 0xC5,
    LIFE_TREE_FRUIT                  = 0xC6,
    EXTRA_WALLET                     = 0xC7,
    HEART_PIECE_COUNTER              = 0x1E9,
    POUCH_EXPANSION_COUNTER          = 0x1EA,
    DEKU_SEED_COUNTER                = 0x1ED,
    ARROW_COUNTER                    = 0x1F2,
    BOMB_COUNTER                     = 0x1F3,
    RUPEE_COUNTER                    = 0x1F5,
    CRYSTAL_PACK_COUNTER             = 0x1F6,
    KEY_PIECE_COUNTER                = 0x1F9,
    EXTRA_WALLET_COUNTER             = 0x1FC,
    MAX511                           = 0x1FF,
}
