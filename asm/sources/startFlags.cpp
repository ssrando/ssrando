#include "common.h"

void setAreaSceneflag(u32 flag, int sceneIndex)
{
    if (flag >= 0x80)
    {
        return; // this is not a sceneflag
    }
    u16 *savedFlags = FILE_MANAGER->getSceneflags();
    // each area uses 16 bytes, so 8 u16
    int slot = flag / 16; // each u16 has 16 bits
    int shift = flag % 16;
    savedFlags[sceneIndex * 8 + slot] |= (1 << shift);
}

void processStartflags()
{
    FILE_MANAGER->anticommitFlag = 1;
    u16 *flagentryPtr = (u16 *)0x804ee1b8; // 512 unused bytes
    u16 val;
    // storyflags
    while ((val = *flagentryPtr++) != 0xFFFF)
    {
        STORYFLAG_MANAGER->setStoryflag(val);
    }
    // itemflags
    while ((val = *flagentryPtr++) != 0xFFFF)
    {
        u32 flagidx = val & 0x1FF;
        u32 count = val >> 9;
        ITEMFLAG_MANAGER->setItemflagToValue(flagidx, count);
    }
    // sceneflags
    while ((val = *flagentryPtr++) != 0xFFFF)
    {
        u32 area = val >> 8;
        u32 flag = val & 0xFF;
        setAreaSceneflag(flag, area);
    }
    // handle dungeonflags
    // each entry uses 1 byte:
    // 0x08 is the flag for boss key
    // 0x02 is the flag for map
    // (val >> 2) & 0x7 is small key count
    u16 *dungeonFlags = FILE_MANAGER->dungeonFlags[0];
    u8 *flagentryPtrU8 = (u8 *)flagentryPtr;
    for (int i = 11; i < 22; i++)
    {
        u8 rawVal = *flagentryPtrU8++;
        u16 actualVal = ((rawVal & 0xA) << 8) | ((rawVal >> 2) & 7);
        dungeonFlags[0] = actualVal;
        dungeonFlags += 8;
    }
    flagentryPtr = (u16 *)flagentryPtrU8;
    ITEMFLAG_MANAGER->setItemflagToValue(501 /*rupee counter*/, *flagentryPtr++);
    // current hearts
    *(u16 *)(((u8 *)FILE_MANAGER) + 0x530A) = *flagentryPtr++;
    FILE_MANAGER->anticommitFlag = 0;
}
