#include "common.h"

void handleHitEvent(AcOSwSwordBeam *actor)
{
    // hardcoding the room here is fine
    // hardcoding the sceneflags is also fine, this code only runs for that one crest in
    // isle of songs
    // if we got this far, we know we have at least goddess sword
    Vec3f pos;
    pos.x = 0;
    pos.y = 0;
    pos.z = 304;
    // place link at fixed coordinates to prevent voiding before getting the item
    LINK_PTR->setPosRot(&pos, nullptr, 0, 1, 0);
    if (!SCENEFLAG_MANAGER->checkFlag(0, 50))
    {
        // first reward
        giveItem((actor->params1 >> 0x18) & 0xFF, -1, 0);
        SCENEFLAG_MANAGER->setFlag(0, 50);
    }
    if (CURRENT_SWORD < 2)
        return;
    if (!SCENEFLAG_MANAGER->checkFlag(0, 51))
    {
        // second reward
        giveItem((actor->params1 >> 0x10) & 0xFF, -1, 0);
        SCENEFLAG_MANAGER->setFlag(0, 51);
    }
    if (CURRENT_SWORD < 3)
        return;
    if (!SCENEFLAG_MANAGER->checkFlag(0, 52))
    {
        // third reward
        giveItem((actor->params2 >> 0x18) & 0xFF, -1, 0);
        SCENEFLAG_MANAGER->setFlag(0, 52);
    }
}
