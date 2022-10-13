#pragma once

typedef unsigned char byte;
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

struct SpawnStruct
{
    char name[32];
    short transitionFadeFrames;
    byte room;
    byte layer;
    byte entrance;
    byte night;
    byte trial;
    byte transitionType;
    byte field8_0x28;
    byte field9_0x29;
    byte field10_0x2a;
    byte field11_0x2b;
};

extern SpawnStruct SPAWN_SLAVE;
extern SpawnStruct SPAWN_MASTER;

class FlagSpace
{
public:
    u16 *flagsPtr;
    u16 flagsCount;
    void *vtable;
};

class StoryflagManager
{
public:
    void setStoryflag(u32 flag);
    u16 getStoryflag(u32 flag);
};

extern StoryflagManager *STORYFLAG_MANAGER;

class SceneflagManager
{
public:
    FlagSpace sceneflags;
    FlagSpace tempflags;
    FlagSpace zoneflags;
    u16 unk;
    u16 sceneIndex;
    u8 shouldCommit;

    SceneflagManager() {}
    int checkFlag(s8 room, u8 flag);
    void setFlag(s8 room, u8 flag);
    int checkFlagGlobal(u8 scene, u8 flag);
    void setFlagGlobal(u8 scene, u8 flag);
    void unsetFlagGlobal(u8 scene, u8 flag);
};

class FileManager
{
public:
    u8 _0[0xa84e];
    u8 anticommitFlag;
    u16 *getSceneflags();
};

extern FileManager *FILE_MANAGER;

class ItemflagManager
{
public:
    void setItemflag(u32 flag);
};

extern ItemflagManager *ITEMFLAG_MANAGER;

extern u8 CURRENT_SWORD;
extern SceneflagManager *SCENEFLAG_MANAGER;
extern void giveItem(u16 itemid, int bottleSlot, int zero);

// only the fields we care about
class AcOSwSwordBeam
{
public:
    int id;
    int params1;
    char pad[0xa8 - 0x8];
    int params2;
};

struct Vec3f
{
    float x, y, z;
};

struct Vec3s
{
    s16 x, y, z;
};

class ActorLink
{
public:
    void setPosRot(Vec3f *pos, Vec3s *rot, int zero1, int one, int zero2);
};

extern ActorLink *LINK_PTR;

enum SwordType : u8
{
    PRACTICE_SWORD,
    GODDESS_SWORD,
    GODDESS_LONGSWORD,
    GODDESS_WHITESWORD,
    MASTERSWORD,
    TRUE_MASTERSWORD,
    NO_SWORD,
};

class Reloader
{
public:
    u8 _0[0x290];
    float initialSpeed;
    u8 _294[0x29a - 0x294];
    s16 spawnState;
};

extern Reloader *RELOADER_PTR;
