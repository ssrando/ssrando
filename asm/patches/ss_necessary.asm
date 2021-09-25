.open "main.dol"
; The subtype of TBox (chests) is determined by the item id
; change it, so that it uses 00 00 00 30 of params1 instead
.org 0x80269530 ; in AcOTBox::init
lwz r0, 0x4(r28) ; load params1
rlwinm r0,r0,28,30,31 ; r0 = (r0 >> 4) & 3
stb r0, 0x1209(r28) ; store subtype
b 0x80269554

.org 0x80115A04 ; in some function that is text advancing related
li r4, 1 ; enables instant text

; patch to not update sword model when getting an upgrade
.org 0x8005e2f0
stwu r1, -0x30(r1) ; change function prologue to match the function it branches to at the end
mflr r0
stw r0, 0x34(r1)
stw r31, 0x2C(r1)
mr r31, r3
stw r30, 0x28(r1)
bl updateCurrentSword
b 0x8005e378
.org 0x8005e384 ; branch to initModels, after actual model updates (which crash)
b 0x8005e250

; to make sure that all items randomized to freestanding locations
; force a textbox, make them subtype 9 and have them act like baby rattle
.org 0x80256c30
lwz r3, 0x4(r3) ; load params1
rlwinm r3,r3,0xc,0x1c,0x1f ; extract subtype
b 0x802476e0 ; branch to rest of function, that returns if it's 9
.org 0x802476e0
subi r0, r3, 9 ; subtype 9, normally checks for rattle itemid

; don't show fi text after map
.org 0x80252b48
b 0x80252bb4

; function that checks if the item is the bird statuette
; always return false to fix the animation
.org 0x80250b00
li r3, 0
blr

; this function checks if a skipflag is set, always return true
.org 0x800bfd20
li r3, 1
blr

; always use the freestanding Y offset for the model, it's 0 most of the time anyway
.org 0x8024d818
b 0x8024d82c

; let all freestanding randomized items use the slingshot item scaling
.org 0x8024aea0
bl should_increase_freestanding_model_size ; custom function that checks ifthe freestanding item scale should be applied

; orignally used for the slingshot for freestanding item scaling, make them bigger
.org 0x80251450
lfs f1,-0x7c68(r2) ; 2.0
blr

; at the end of the item init func, branch to a custom function which fixes the Y offsets
.org 0x8024d438
bl fix_freestanding_item_y_offset

; don't treat faron statues differently after levias
.org 0x80142078
b 0x801420d8

; don't force open the map to faron after levias
.org 0x802d01e8
b 0x802d0214

; always just return from the function that wants to open
; the item screen after a treasure
.org 0x802d02c0
blr

; skip adding to the pouch counter, that is done in the events now
.org 0x80253be4
nop

; after giving gratitude crystals, update the counter in text number 1 with the crystal counter
.org 0x802539dc
b 0x802da0c0
; this replaces unused code
.org 0x802da0c0
lwz r3, -0x4040(r13) ;ITEMFLAG_MANAGER
li r4, 0x1F6 ;gratitude crystals
bl FlagManager__getUncommittedFlags
lwz r4, -0x3fb8(r13) ;LYT_MSG_MANAGER
lwz r4, 0x724(r4) ;Text Manager
stw r3, 0x8A0(r4) ;text counter 1
lwz r0, 0x24(r1) ; instruction that was overwritten
b 0x802539e0

; change storyflag that disables sandship dowsing
; to bombed sandship
.org 0x80097b18
li r4, 0x110

; when checking for story- & sceneflags for triggering the NpcTke
; check both flags to trigger, instead of only one
.org 0x8027ce64
cmplwi r3, 0
bne 0x8027ce78
li r3, 0
nop

; special text when entering faron pillar during SotH, skip over it
.org 0x80141f00
b 0x80141f44

; in the item actor init function, always check if this is a random treasure and apply the final determined item id if necessary
.org 0x8024ac68
nop
nop
nop
nop

; after the function that starts the new file, also process the startflags
.org 0x801bb9bc
b processStartflags

; always allocate keyboard arcs to the end of the heap, to make sure
; faron BiT doesn't crash
.org 0x801b9a10
li r5, 2
.org 0x801b9a44
li r5, 2

; when loading a stage
.org 0x80198dc0
bl unset_sandship_timestone_if_necessary

.close

.open "d_a_obj_time_door_beforeNP.rel"
.org 0xD4C
blt 0xDEC ; also allow opening GoT with a better sword
.close

.open "d_a_obj_door_bossNP.rel"
; fix the array of storyflags the boss door checks for as dungeon completion
.org 0x9770 ; 0x130+ data2 offset 0x9640
.word 0
.word 0x53
.word 0
.word 0x7
.word 0
.word 0x32C
.word 0
.word 0x288
.word 0
.word 0x54
.word 0
.word 0x3A5
.close

.open "d_a_obj_item_heart_containerNP.rel"
.org 0x2214 ; function, that gives the item when collecting the container
rlwinm r3,r0,16,24,31 ; r0 has params1, item is (r0 >> 16) & 0xFF
li r4, 7 ; set subtype to 7 to force textbox
.close

.open "d_a_obj_chandelierNP.rel"
.org 0x1D70 ; function, that spawns the "heartpiece"
li r4, 9 ; set itemsubtype to 9
stw r30, 0x8(r1)
mr r30, r3
lwz r0, 0x4(r3) ; params1
rlwinm r3,r0,24,24,31 ; (r0 >> 8) & 0xFF, itemid

.org 0xF7C ; in function, that runs when bonking the chandelier
nop ; branches over activating the chanderlier event after spiral charge, never take the branch
.close

.open "d_a_obj_soilNP.rel"
.org 0x1A10 ; function that gives the key piece
lbz r3, 0xa8(r31) ; grab itemid from first params2 byte

.org 0x1950 ; also function that gives the key piece
lbz r3, 0xa8(r3) ; grab itemid from first param2 byte

.org 0xE54 ; function that sets the sceneflag
nop ; normally only sets the flag, if the item was a key piece, nop the branch
.close

.open "d_a_obj_warpNP.rel"
.org 0x234
li r3, 0xC98 ; in ctor, give 4 bytes more memory

.org 0x22C0 ; function, that gives the trial item
stwu r1,-16(r1)
mflr r0
stw r0,20(r1)
stw r31,12(r1)
mr r31,r3 ; r31 is AcOWarp ptr
lwz r3,-0x4044(r13) ; STORYFLAG_MANAGER
lhz r4, 0xaa(r31) ; 3rd and 4th byte in params2 is storyflag for completing trial
bl FlagManager__setFlagTo1 ; set storyflag for completing trial
lbz r3, 0x4(r31) ; first byte of params1 is itemid
li r4, -1 ; set pouch slot param to -1, otherwise pouch items break
li r5, 0 ; 3rd arg for giveItem function call
bl giveItem ; give the item for the trial
stw r3, 0xC94(r31)
lwz r0,20(r1)
lwz r31,12(r1)
mtlr r0
addi r1,r1,16
blr

.org 0x2344 ; function, that runs after giving the item, if the event is triggered immediately, the item won't be given
bl check_should_delay_walk_out_event ; check whether or not the item get event started
cmpwi r3, 0 ; function returns 0 if returning from the trial should be delayed
beq 0x23A4
nop

; the trial storyflags got changed, cause they used the same one as the items associated with it
.org 0x2F48
li r4, 0x397 ; new storyflag

.org 0x2F88
li r4, 0x398

.org 0x2FD4
li r4, 0x399

.org 0x3020
li r4, 0x39A

.org 0x2B08
li r4, 0x397

.org 0x2B48
li r4, 0x398

.org 0x2B94
li r4, 0x399

.org 0x2BE0
li r4, 0x39A

.org 0xC8C
li r4, 0x397

.org 0xCCC
li r4, 0x398

.org 0xD18
li r4, 0x399

.org 0xD64
li r4, 0x39A

.close

.open "d_a_e_bcNP.rel"
.org 0x4828 ; in death function (?), when it checks if it should set the sceneflag
lbz r0, 0x1254(r31) ; load if the boko has the key
cmplwi r0, 1 ; check if it's 1, it doesn't set the flag if this condition is met

.org 0x491C ; in the same functions, never drop the key on the boko death
b 0x4934

.org 0xE8F8 ; when whipping the bokoblin
lbz r3, 0xab(r31) ; load itemid from last byte of params2
lbz r6, 0x1343(r31)
extsb r30, r30
li r4, 9 ; change itemtype to 9

.org 0xEB30 ; another function that gives the item
lbz r3, 0xab(r31) ; load itemid from last byte of params2
lbz r6, 0x1343(r31)
extsb r28, r28
li r4, 9 ; change itemtype to 9

.close

.open "d_a_e_bceNP.rel"
.org 0x162C ; init func
li r3, 0 ; don't kill the hook beetle bokos if you have hook beetle
b 0x163C

.close

.open "d_a_obj_goddess_cubeNP.rel"
.org 0x1330 ; in function that checks, if the cube can be hit
li r3, 1 ; don't require the first cube near skyview
blr

.close

.open "d_a_npc_aqua_dragonNP.rel"
.org 0x3E7C ; function that checks AC flag
li r4, 0x384 ; new AC flag

.close

.open "d_a_npc_kyui_elderNP.rel"
.org 0x2A30 ; function that spawns slingshot
blr ; do not spawn it ever

.org 0x2CE0 ; let the function, that checks for the slingshot appears storyflag always return false
li r3, 0
blr

.org 0x2C80 ; function that checks for erla storyflag
li r3, 0 ; always return false
blr

.org 0x2E30 ; function that checks for slingshot itemflag
li r3, 0 ; always return false
blr

.close

.open "d_a_obj_chestNP.rel"
.org 0x14E4 ; in function that gives the item
li r4, -1 ; -1 for bottle slot, or pouch items break

.close

; TODO: bird speed patch

.open "d_a_birdNP.rel"
.org 0xA154 ; 809b72e4 in ghidra
mr r3, r31
bl loftwing_speed_limit
nop
nop
nop

.org 0x9FB4 ; 809b712c in ghidra
nop ; don't cap speed here

.org 0x9FC4 ; belongs to function above, instead of blr, branch to loftwing_speed_limit function at the end
ble skip_store_max
stfs f0,0xfb8(r3)
skip_store_max:
b loftwing_speed_limit
.close

.open "d_a_npc_dive_game_judgeNP.rel"
.org 0x2BD8 ; in function that checks if he should loose his party wheel
li r4, 0x130 ; always loose it (batreaux storyflag)

.close

.open "d_a_npc_desertrobotNP.rel"
.org 0x1EA4 ; checks here, if you have hook beetle so he puts it out of his hands, always make it true
nop

.close

.open "d_a_npc_terryNP.rel"
.org 0x444 ; always remove cage from beetles hands
nop

.close

.open "d_a_obj_blast_rockNP.rel"
.org 0xEA4 ; init func
li r0, 0xFF ; always set eventid to 0xFF (so none will play on exploding)

.close

.open "d_a_obj_pot_salNP.rel"
.org 0xB44 ; function that decides if the pot should spawn in lumpy pumpkin
nop ; do not need spiral charge to spawn

.close

.open "d_t_D3_scene_changeNP.rel"
.org 0x458
li r3, 0 ; load a null pointer for the skyloft exit, so the other custom code can take care of it

; this patch branches to the custom trigger_exit_one function, when a scenechange is needed to outside of sky keep
.org 0x2EC ; branch, if link doesn't touch the trigger
beq function_end

.org 0x300 ; branch, if the returned next stage name is null, meaning use exit 1
beq trigger_exit_one_lbl

.org 0x33C
b function_end ; after triggering the normal sky keep entrance mechanic, do not trigger the exit to skyloft
.global trigger_exit_one_lbl
trigger_exit_one_lbl:
bl trigger_exit_one ; if the returned ptr from getNextStageAndEntrance was null, it branches here

.global function_end
function_end:
lwz 31, 0x1C(r1)
li r3, 1
lwz r0, 0x24(r1)
mtlr r0
addi r1, r1, 0x20
blr

.close

.open "d_a_obj_time_stoneNP.rel"
.org 0x15B0
bl set_first_time_cs_already_watched ; in a branch that is not taken for the time shift stone on sandship
.close

.open "d_a_obj_sw_sword_beamNP.rel"
; function that checks for your current sword, so that you can't activate the crest
.org 0x25B0
bge 0x2650 ; instead of only checking for whitesword for the last reward, check for at least that

.org 0xD5C ; should handle the isle of songs CS starting, overwrite it with a jump to the custom function, that gives the items
mr r3, r31
bl handle_crest_hit_item_give
b 0xD88 ; this probably cancels the crest event?

.org 0x1710 ; don't set the sceneflag normally, that's handled in the custom function now
b 0x17C8

.close

.open "d_a_shop_sampleNP.rel"
.org 0x6E9C
.word -1 ; can always buy iron shield
.org 0x6EF0
.word -1 ; can always buy sacred shield
.close

.open "d_a_npc_douguyanightNP.rel"
.org 0xBA0
b select_new_item_column
.close