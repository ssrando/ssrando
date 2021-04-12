typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

class SceneflagManager {
public:
    SceneflagManager() {}
    int checkFlag(s8 room, u8 flag);
    void setFlag(s8 room, u8 flag);
};

extern u8 CURRENT_SWORD;
extern SceneflagManager* SCENEFLAG_MANAGER;
extern void giveItem(u16 itemid, int bottleSlot, int zero);

// only the fields we care about
class AcOSwSwordBeam {
public:
int id;
int params1;
char pad[0xa8-0x8];
int params2;
};

struct Vec3f {
    float x,y,z;
};

struct Vec3s {
    s16 x,y,z;
};


class ActorLink {
public:
    void setPosRot(Vec3f* pos, Vec3s* rot, int zero1, int one, int zero2);
};

extern ActorLink *LINK_PTR;

enum SwordType : u8 {
    PRACTICE_SWORD,
    GODDESS_SWORD,
    GODDESS_LONGSWORD,
    GODDESS_WHITESWORD,
    MASTERSWORD,
    TRUE_MASTERSWORD,
    NO_SWORD,
};

void handleHitEvent(AcOSwSwordBeam* actor) {
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
    if (!SCENEFLAG_MANAGER->checkFlag(0, 50)) {
        // first reward
        giveItem((actor->params1 >> 0x18) & 0xFF, -1, 0);
        SCENEFLAG_MANAGER->setFlag(0, 50);
    }
    if (CURRENT_SWORD < 2) return;
    if (!SCENEFLAG_MANAGER->checkFlag(0, 51)) {
        // second reward
        giveItem((actor->params1 >> 0x10) & 0xFF, -1, 0);
        SCENEFLAG_MANAGER->setFlag(0, 51);
    }
    if (CURRENT_SWORD < 3) return;
    if (!SCENEFLAG_MANAGER->checkFlag(0, 52)) {
        // third reward
        giveItem((actor->params2 >> 0x18) & 0xFF, -1, 0);
        SCENEFLAG_MANAGER->setFlag(0, 52);
    }
}