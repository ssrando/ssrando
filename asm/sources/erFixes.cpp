// before spawn struct used funcs
// 801ba910 // not on death
// 801bb5a0

// 801ba978 after
// 800be1f0 set flag global
// 8096050c SCENEFLAGMANAGER
// 807B160C timeshift rel
// 807b3d2c

// timeshiftstone flags: 113-124, 111, 108
// last mine: 113

#include "common.h"

void doErFixes()
{
    if (RELOADER_PTR->initialSpeed > 30)
    {
        RELOADER_PTR->initialSpeed = 30;
    }
    u32 stageName = *(u32 *)SPAWN_SLAVE.name;
    if (stageName == 'F000')
    {
        // Skyloft from Sky Keep
        if (SPAWN_SLAVE.entrance == 53 &&
            STORYFLAG_MANAGER->getStoryflag(22 /* Sky Keep appears */) == 0)
        {
            // Change to entrance next to SK statue
            SPAWN_SLAVE.entrance = 52;
        }
    }
    else if (stageName == 'F300')
    {
        u16 subArea = *(u16 *)&SPAWN_SLAVE.name[4]; // '\0X' for Desert, '_1' for mine
        // Lanayru Desert
        if (subArea <= 0xFF)
        {
            // Lanayru Desert from LMF
            if (SPAWN_SLAVE.entrance == 5)
            {
                if (SCENEFLAG_MANAGER->checkFlagGlobal(7 /* Lanayru Desert */, 30 /* LMF raising */) == 0)
                {
                    // weird entrance, close enough
                    SPAWN_SLAVE.entrance = 12;
                }
            }
            else
                // Lanayru Desert from Mine
                if (SPAWN_SLAVE.entrance == 2)
            {
                goto doTimeshiftFix;
            }
        }
        else
            // Lanayru Mine
            if (subArea == '_1')
        {
            // Mine from Desert
            if (SPAWN_SLAVE.entrance == 1)
            {
                goto doTimeshiftFix;
            }
        }
    }
    else if (stageName == 'F210')
    {
        if (SPAWN_SLAVE.entrance == 0)
        {
            // diving
            RELOADER_PTR->spawnState = 0x13;
        }
    }
    return;
doTimeshiftFix:
    for (int flag = 114; flag <= 124; flag++)
    {
        SCENEFLAG_MANAGER->unsetFlagGlobal(7, flag);
    }
    SCENEFLAG_MANAGER->unsetFlagGlobal(7, 111);
    SCENEFLAG_MANAGER->unsetFlagGlobal(7, 108);
    // last timeshift stone in mine
    SCENEFLAG_MANAGER->setFlagGlobal(7, 113);
}
