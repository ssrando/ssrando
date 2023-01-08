SECTIONS
{
    .text : {
        __text_start = . ;
        *(.text)
        *(.text.*)
        __text_end  = . ;
    }

    .data : {
        __data_start = . ;
        *(.rodata)
        *(.data)
        *(.bss)
        *(COMMON)
        __data_end  = . ;
    }
}

updateCurrentSword = 0x8005c110;
getGratitudeCrystalCount = 0x80252710;
checkButtonAHeld = 0x80059860;
checkButtonAPressed = 0x80059680;
checkButtonBHeld = 0x80059880;
checkButtonBPressed = 0x800596a0;
FlagManager__getUncommittedFlags = 0x800bf5f0;
FlagManager__setFlagOrCounter = 0x800bf530;
INPUT_BUFFER = 0x80599d0c;
AcItem__isBabyRattle = 0x80256c30;
Math__approachF = 0x802decd0;
FileManager__getDungeonFlags = 0x8000a460;
FlagManager__setFlagTo1 = 0x800bf5b0;
FileManager__getSceneflags = 0x8000a4e0;
SceneflagManager__setTempOrSceneflag = 0x800be2d0;
SceneflagManager__setFlagGlobal = 0x800be1f0;
SceneflagManager__checkFlagGlobal = 0x800bdf20;
requestFileLoadFromDisk = 0x802f0060;
SPAWN_SLAVE = 0x805b3860;
AcOTBox__initDowsingTarget = 0x8026d780;
FILE_MANAGER = 0x80574ffc;
SCENEFLAG_MANAGER = 0x805753e0;
ITEMFLAG_MANAGER = 0x80575400;
STORYFLAG_MANAGER = 0x805753FC;
DUNGEONFLAG_MANAGER = 0x80575404;
STATIC_DUNGEON_FLAGS = 0x805a9c58;
TextManager__setNumericArgs = 0x800b8a60;
TextManager__setStringArg = 0x800b7fa0;
LYT_MSG_MANAGER = 0x80575488;
checkStoryflagIsSet = 0x80141e90;
