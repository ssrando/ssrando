typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned long u32;
typedef signed long s32;

class FlagSpace {
public:
    u16* flagsPtr;
    u16 flagsCount;
    void* vtable;
};

class SceneflagManager {
public:
    FlagSpace sceneflags;
    FlagSpace tempflags;
    FlagSpace zoneflags;
    u16 unk;
    u16 sceneIndex;
    u8 shouldCommit;
    
    void setTempOrSceneflag(u32 flag); // 800be2d0
};

extern SceneflagManager* SCENEFLAG_MANAGER;

class FileManager {
public:
u8 _0[0xa84e];
u8 anticommitFlag;
    u16* getSceneflags();
};

extern FileManager* FILE_MANAGER;

class StoryflagManager {
public:
    void setStoryflag(u32 flag);
};

extern StoryflagManager* STORYFLAG_MANAGER;

class ItemflagManager {
public:
    void setItemflag(u32 flag);
};

extern ItemflagManager* ITEMFLAG_MANAGER;

void setAreaSceneflag(u32 flag, int sceneIndex) {
    if (flag >= 0x80) {
        return; // this is not a sceneflag
    }
    u16* savedFlags = FILE_MANAGER->getSceneflags();
    // each area uses 16 bytes, so 8 u16
    int slot = flag / 16; // each u16 has 16 bits
    int shift = flag % 16;
    savedFlags[sceneIndex * 8 + slot] |= (1 << shift);
}

void processStartflags() {
    FILE_MANAGER->anticommitFlag = 1;
    u16* flagentryPtr = (u16*) 0x804ee1b8; // 512 unused bytes
    u16 val;
    // storyflags
    while ((val = *flagentryPtr++) != 0xFFFF) {
        STORYFLAG_MANAGER->setStoryflag(val);
    }
    // itemflags
    while ((val = *flagentryPtr++) != 0xFFFF) {
        ITEMFLAG_MANAGER->setItemflag(val);
    }
    // sceneflags
    while ((val = *flagentryPtr++) != 0xFFFF) {
        u32 area = val >> 8;
        u32 flag = val & 0xFF;
        setAreaSceneflag(flag, area);
    }
    FILE_MANAGER->anticommitFlag = 0;
}