.open "main.dol"
.org @NextFreeSpace
.global fix_freestanding_item_y_offset
fix_freestanding_item_y_offset:
; r29 is the item ptr, r3 needs to NOT be modified
lwz r0, 0x4(r29) ; params1
rlwinm r4,r0,12,28,31 ; extract subtype: (r0 >> 0x14) & 0xF
cmpwi r4, 9
bne func_end
rlwinm r4,r0,0,0xff ; r0 & 0xFF
cmpwi r4, 0x5E ; heartpieces are already high enough, don't push them up
beq func_end
lfs f0,-0x7ce8(r2) ; 10.0
stfs f0, 0xd14(r29) ; store freestandingYOffset
func_end:
addi r11, r1, 0x50 ; replaced instruction
blr

.global should_increase_freestanding_model_size
should_increase_freestanding_model_size:
lwz r0, 0x4(r3) ; params1
rlwinm r3,r0,12,28,31 ; extract subtype: (r0 >> 0x14) & 0xF
cmpwi r3, 9 ; check if subtype is 9
li r3, 0
bnelr ; if not, return false
rlwinm r0,r0, 0,24,31 ; r0 & 0xFF, itemid
cmpwi r0, 0x5D ; return false for HC
beqlr
cmpwi r0, 0x5E ; return false for HP
beqlr
li r3, 1 ; otherwise, return true
blr

; helper function, to be able to just call one function to modify a storyflag
; r3 is storyflag, r4 is value
.global setStoryflagToValue
setStoryflagToValue:
mr r5, r4
mr r4, r3
lwz r3, STORYFLAG_MANAGER@sda21(r13)
lwz r12, 0x0(r3)
lwz r12, 0x28(r12)
mtctr r12
bctr

smallkey_to_flagindex:
.byte 11 ; SV
.byte 17 ; LMF
.byte 12 ; AC
.byte 15 ; FS
.byte 18 ; SS
.byte 20 ; SK
.byte 9 ; Lanayru Caves
.align 4

.global handleSmallKeyGet
handleSmallKeyGet:
mr r3, r31 ; r31 has item id from parent function
stwu r1, -0x10(r1)
mflr r0
stw r0, 20(r1)
stw r31, 12(r1) ; r31 is flagindex of the dungeon
stw r30, 8(r1)
addi r4, r3, -200 ; fist small key at 200
cmplwi r4, 6
bgt smallkey_func_end ; not a small key
lis r5, smallkey_to_flagindex@ha
addi r5, r5, smallkey_to_flagindex@l
lbzx r31, r4, r5 ; load flagindex of the small key
lwz r3, DUNGEONFLAG_MANAGER@sda21(r13)
lha r0, 2(r3)
cmpw r0, r31 ; check if dungeon item is for current area
bne handle_other_area_small_key
lwz r4, 8(r3) ; ptr to FlagSpace, which points to static dungeonflags
lwz r5, 0(r4) ; load first word of dungeonflags, last 4 bits are small key count
addi    r0,r5,1 ; curVal = (curVal & ~0xF) | ((curVal + 1) & 0xF)
clrlwi  r0,r0,28
rlwimi  r0,r5,0,0,27
stw r0, 0(r4) ; set flag and write back
li r0, 1
stb r0, 0(r3) ; set commit flag
b smallkey_func_end
handle_other_area_small_key:
lwz r3, FILE_MANAGER@sda21(r13)
bl FileManager__getDungeonFlags
rlwinm r4, r31, 4, 0, 27 ; flagindex * 16
lwzx r5, r3, r4 ; load first word of saved dungeonflags, last 4 bits are small key count
addi    r0,r5,1 ; curVal = (curVal & ~0xF) | ((curVal + 1) & 0xF)
clrlwi  r0,r0,28
rlwimi  r0,r5,0,0,27
stwx r0, r3, r4 ; set flag and write back
smallkey_func_end:
li r3, 5 ; removed instruction from parent function
lwz r30, 8(r1)
lwz r31, 12(r1)
lwz r0, 20(r1)
mtlr r0
addi r1, r1, 0x10
blr

; function to set a sceneflag to the saved flags area
; breaks in normal gameplay when settings a sceneflag for the current sceneflagindex
; r3 is flag, r4 is area
.global setSceneflagForArea
setSceneflagForArea:
stwu r1, -16(r1)
mflr r0
stw r0, 20(r1)
stw r31, 12(r1)
stw r30, 8(r1)
mr r30, r3
mr r31, r4
cmplwi r3, 128
bge setSceneflagForArea_end
lwz r3, FILE_MANAGER@sda21(r13)
bl FileManager__getSceneflags
srwi r4, r30, 4
rlwinm r0, r31, 3, 0, 28
add r0, r4, r0
rlwinm r6, r0, 1, 0, 30
lhzx r5, r3, r6
li r4, 1
rlwinm r0,r30,0,28,31
slw r0, r4, r0
clrlwi r0, r0, 16
or r0, r5, r0
sthx r0, r3, r6
setSceneflagForArea_end:
lwz r31, 12(r1)
lwz r30, 8(r1)
lwz r0, 20(r1)
mtlr r0
addi r1, r1, 16
blr

; function, that only actually loads the keyboard arcs if the following conditions are met:
; 1. you are in BiT (checked with Link's actor params)
; 2. All files are not empty
.global alloc_keyboard_arcs_conditional
alloc_keyboard_arcs_conditional:
; can't use r3, r4, r5, r6
lwz r12, LINK_PTR@sda21(r13)
lwz r12, 0x4(r12) ; link params
xoris r12, r12, 0xFFFF ; check for 0xFFFF0FFF, actor params on title screen, are different in BiT
cmpwi r12, 0x0FFF
beq do_requestFileLoadFromDisk
lwz r12, FILE_MANAGER@sda21(r13)
lwz r12, 0(r12) ; location for all saved save files
lbz r11, 0x53ad(r12) ; new savefile flag on file 1 + 0x20 offset from save files in general
cmpwi r11, 1
beq do_requestFileLoadFromDisk
addi r12, r12, 0x53c0
lbz r11, 0x53cd(r12) ; new savefile flag on file 2
cmpwi r11, 1
beq do_requestFileLoadFromDisk
addi r12, r12, 0x53c0
lbz r11, 0x53cd(r12) ; new savefile flag
cmpwi r11, 1
bnelr
do_requestFileLoadFromDisk:
b requestFileLoadFromDisk

.global unset_sandship_timestone_if_necessary
unset_sandship_timestone_if_necessary:
li r28, 0 ; replaced instruction
lis r3, SPAWN_SLAVE@ha
lwz r3, SPAWN_SLAVE@l(r3) ; load 4 bytes of stage name
xoris r0, r3, 0x4233 ; 'B3'
cmplwi r0, 0x3031 ; '01
beqlr
xoris r0, r3, 0x4433 ; 'D3'
cmplwi r0, 0x3031 ; '01
beqlr
; if we're not in Sandship (D301), Sandship Escape (D301_1) or Tentalus (B301)
; unset the storyflag
li r3, 154 ; storyflag for SSH timeshift stone being active
li r4, 0 ; storyflag will be unset
b setStoryflagToValue

.global patch_bit
patch_bit:
li r0, 0
stb r0, -0x3ca3(r13) ; RELOADER_TYPE
blr

; space to declare all the functions defined in the
; custom-functions rust project
.global process_startflags
.global handle_bk_map_dungeonflag
.global rando_text_command_handler
.global textbox_a_pressed_or_b_held
.global set_goddess_sword_pulled_scene_flag

.close


.open "d_a_birdNP.rel"
.org @NextFreeSpace
.global loftwing_speed_limit ; expects loftwing actor in r3
loftwing_speed_limit:
lis r6, INPUT_BUFFER@ha ; input buffer
lwz r6, INPUT_BUFFER@l(r6)
andis. r0, r6, 0x0400 ; check for B pressed
bne c_up_pressed
lfs f1,-0x3948(r2) ; 350.0f constant
b past_if_else
c_up_pressed:
lfs f1,-0x56c0(r2) ; 80.0f constant
past_if_else:
lfs f0, 0x144(r3)
fcmpo cr0, f1, f0
bgelr
stfs f1, 0x144(r3)
blr
.close

.open "d_t_D3_scene_changeNP.rel"
.org @NextFreeSpace
.global trigger_exit_one
trigger_exit_one:
lwz r3, RELOADER_PTR@sda21(r13)
li r4, 0 ; current room, all rooms in sky keep are room 0
li r5, 1 ; take exit 1, it's always the skyloft exit
li r6, 2 ; idk
li r7, 2 ; idk
b Reloader__triggerExit
.close

.open "d_a_obj_warpNP.rel"
.org @NextFreeSpace
.global check_should_delay_walk_out_event
check_should_delay_walk_out_event:
; 0xC94 (rando exclusive field at the end of the warp struct) either holds:
; 0, if there is no pointer stored, this should not happen and will crash :)
; some pointer to the item actor that the trial gave to the player
; 1 if the item event has started. This is fine because 1 is not a valid pointer
mr r4, r3 ; r3 is trial pointer
lwz r3, 0xC94(r4)
cmplwi r3, 1
beqlr
lbz r3, 0xB0F(r3) ; some byte from the actorevent idk, was 0 before event and then 1
cmplwi r3, 0
beqlr
li r3, 1
stw r3, 0xC94(r4)
blr
.close

.open "d_a_obj_time_stoneNP.rel"
.org @NextFreeSpace
.global set_first_time_cs_already_watched
set_first_time_cs_already_watched: ; r27 is AcOTimeShiftStone actor
li r0, 0
stb r0, 0x147e(r27) ; store false so first time longer CS doesn't play
stb r0, 0x1485(r27) ; store false so first time longer CS doesn't play
lfs f3,0xb4(r30) ; instruction that got replaced
blr

.close

.open "d_a_obj_sw_sword_beamNP.rel"
; function that checks for your current sword, so that you can't activate the crest
.org @NextFreeSpace
.global handle_crest_hit_item_give
handle_crest_hit_item_give: ; see sources/IoSGodCrest.cpp
stwu r1, -0x20(r1)
mflr r0
stw r0, 0x24(r1)
stw r31, 0x1C(r1)
mr r31, r3
; load Vec3f (0,0,304)
lis r0, 0x4398 ; float 304
stw r0, 0x10(r1)
li r0, 0 ; float 0.0
stw r0, 0x8(r1)
stw r0, 0xC(r1)
lwz r3, LINK_PTR@sda21(r13)
addi r4, r1, 8
li r5, 0
li r6, 0
li r7, 1
li r8, 0
bl ActorLink__setPosRot
lwz r3, SCENEFLAG_MANAGER@sda21(r13)
li r4, 50
bl SceneflagManager__checkTempOrSceneflag
cmpwi r3, 0
bne longsword_reward_check
lwz r0, 0x4(r31)
rlwinm r3,r0,8,24,31
li r4, -1
li r5, 0
bl giveItem
lwz r3, SCENEFLAG_MANAGER@sda21(r13); SCENEFLAG_MANAGER
li r4, 50
bl SceneflagManager__setTempOrSceneflag
longsword_reward_check:
lbz r0, EQUIPPED_SWORD@sda21(r13)
cmplwi r0, 2
blt function_end
lwz r3, SCENEFLAG_MANAGER@sda21(r13)
li r4, 51
bl SceneflagManager__checkTempOrSceneflag
cmpwi r3, 0
bne whitesword_reward_check
lwz r0, 0x4(r31)
rlwinm r3,r0,16,24,31
li r4, -1
li r5, 0
bl giveItem
lwz r3, SCENEFLAG_MANAGER@sda21(r13)
li r4, 51
bl SceneflagManager__setTempOrSceneflag
whitesword_reward_check:
lbz r0, EQUIPPED_SWORD@sda21(r13)
cmplwi r0, 3
blt function_end
lwz r3, SCENEFLAG_MANAGER@sda21(r13)
li r4, 52
bl SceneflagManager__checkTempOrSceneflag
cmpwi r3, 0
bne function_end
lwz r0, 0xa8(r31)
rlwinm r3,r0,8,24,31
li r4, -1
li r5, 0
bl giveItem
lwz r3, SCENEFLAG_MANAGER@sda21(r13)
li r4, 52
bl SceneflagManager__setTempOrSceneflag
function_end:
lwz r31, 0x1C(r1)
lwz r0, 0x24(r1)
mtlr r0
addi r1, r1, 0x20
blr
.close

.open "d_a_shop_sampleNP.rel"
.org @NextFreeSpace
; checks if this is one of the shop items that need the modified shopsample class
.global check_needs_custom_storyflag_subtype
check_needs_custom_storyflag_subtype:
; r3 cannot be modified, r4 is the shopitemid and can't be modified
; the result is in the condition register, equal flag has to be set if the shopitemid is one we care about
; bool test(int i) {
;    return i == 24
;           || i == 17
;           || i == 18
;           || i == 25
;           || i == 27;
;}
addi r9,r4,-24
cmplwi r9,1
ble lbl_21
addi r9,r4,-17
cmplwi r9,1
ble lbl_21
xori r5,r4,27
cntlzw r5,r5
srwi r5,r5,5
b lbl_end
lbl_21:
li r5,1
lbl_end:
cmpwi r5, 1
blr

.global correct_rupee_color
correct_rupee_color:
; itemId r28
; heapMaybe r29
; brres ptr at r1 + 0xC
; model ptr r31
; model instance r27
; setup "function args"
lwz r3, 0xC(r1) ; brres
mr r4, r31 ; model
mr r5, r27 ; modelInstance
mr r6, r29 ; heap
mr r7, r28 ; itemid
; see https://godbolt.org/z/ovq7Yczhx
mflr 0
stwu 1,-64(1)
li 10,6
li 9,0
stw 30,56(1)
mtctr 10
lis 30,RUPEE_ITEM_TO_TEX_FRAME@ha
stw 0,68(1)
stw 27,44(1)
la 30,RUPEE_ITEM_TO_TEX_FRAME@l(30)
stw 29,52(1)
stw 31,60(1)
stw 3,24(1)
stw 4,28(1)
stw 28,48(1)
mr 28,5
.correct_rupee_colorL5:
slwi 31,9,3
addi 9,9,1
lhzx 10,30,31
cmpw 7,10,7
beq- 7,.correct_rupee_colorL11
bdnz .correct_rupee_colorL5
lwz 0,68(1)
lwz 27,44(1)
mtlr 0
lwz 28,48(1)
lwz 29,52(1)
lwz 30,56(1)
lwz 31,60(1)
addi 1,1,64
; replaced instruction
addi r11,r1,0x130
blr
.correct_rupee_colorL11:
li 3,44
stw 6,32(1)
li 27,0
bl allocOnCurrentHeap
; leak this memory, but it seems to be allocated on this
; actors heap, so it gets freed when the actor is freed as well
stw 27,4(3)
mr 29,3
stw 27,8(3)
addi 3,3,12
add 31,30,31
bl func_0x802ee0e0
lis 9,0x8054
ori 9,9,9624
stw 27,40(29)
stw 9,0(29)
subi r4,r13,0x69d0; "Rupee"
addi 3,1,24
bl getAnmTexPatFromBrres
lwz 6,32(1)
addi 5,1,8
stw 3,8(1)
addi 4,1,28
li 7,0
li 8,1
mr 3,29
bl AnmTexPatControl__bind
lwz 9,0x10(28)
mr 3,28
mr 4,29
lwz 9,36(9)
mtctr 9
bctrl
lfs 1,4(31)
mr 3,29
li 4,0
bl AnmTexPatControl__setFrame
; calling the destructor makes it not work
; this feels very wrong, but seems to work?
lwz 0,68(1)
lwz 27,44(1)
mtlr 0
lwz 28,48(1)
lwz 29,52(1)
lwz 30,56(1)
lwz 31,60(1)
addi 1,1,64
; replaced instruction
addi r11,r1,0x130
blr

.close

.open "d_a_npc_douguyanightNP.rel"
.org @NextFreeSpace
.global select_new_item_column
select_new_item_column:
; r5 is command
cmplwi r5, 9 ; we only care about command 9 (custom for advancing what item row to buy)
bne new_treasure_function_end
; get current row
lwz r3, STORYFLAG_MANAGER@sda21(r13)
li r4, 0x28C
bl FlagManager__getFlagOrCounter
addi r3, r3, 1 ; advance 1 slot
rlwinm r5,r3,0,30,31 ; only use last 2 bits, there are 4 options
lwz r3, STORYFLAG_MANAGER@sda21(r13)
li r4, 0x28C
bl FlagManager__setFlagOrCounter
; end of function we jumped out of
new_treasure_function_end:
lwz r31, 0x3C(r1)
li r3, 1
lwz r30, 0x38(r1)
lwz r29, 0x34(r1)
lwz r28, 0x30(r1)
lwz r0, 0x44(r1)
mtlr r0
addi r1, r1, 0x40
blr

.close

.open "d_a_obj_swrd_prjNP.rel" ; goddess wall
.org @NextFreeSpace
; replaces the call to "isPlayingHarp" and adds the BotG requirement
; we do this because otherwise the actor despawns on load, meaning you can't activate goddess walls
; after getting BotG until you reload
.global reveal_goddess_wall_check
reveal_goddess_wall_check:
stwu r1, -0x10(r1)
mflr r0
stw r0, 20(r1)
bl isPlayingHarp
cmpwi r3, 0
beq reveal_goddess_wall_check_end
lwz r3, ITEMFLAG_MANAGER@sda21(r13)
li r4, 0xba ; BAllad (nice coincidence)
bl FlagManager__getFlagOrCounter
reveal_goddess_wall_check_end:
lwz r0, 20(r1)
mtlr r0
addi r1, r1, 0x10
blr
.close

.open "d_a_obj_bellNP.rel"
; custom function that ends the pumpkin archery minigame early
; used when the bell is hit
.org @NextFreeSpace
.global try_end_pumpkin_archery
try_end_pumpkin_archery:
; check that we're in the right minigame mode
lis r3, SPECIAL_MINIGAME_STATE@ha
lwz r3, SPECIAL_MINIGAME_STATE@l(r3)
cmplwi r3, 6 ; archery
bnelr
stwu r1, -0x10(r1)
mflr r0
stw r0, 20(r1)
li r3, 272 ; NpcPcs, fledge for the minigame
li r4, 0 ; previous actor in search, NULL for search from start
bl findActorByActorType
cmplwi r3, 0 ; I can't think of a way this is ever NULL, but just in case
beq try_end_pumpkin_archery_end
li r4, 0
stw r4, 0x1040(r3) ; store 0 in the remaining time (it's 64 bit)
stw r4, 0x1044(r3)
try_end_pumpkin_archery_end:
lwz r0, 20(r1)
mtlr r0
addi r1, r1, 0x10
blr
.close

.open "d_a_obj_light_lineNP.rel"
.org @NextFreeSpace
.global check_activated_storyflag
check_activated_storyflag:
; actor pointer in r31
stwu r1, -0x10(r1)
mflr r0
stw r0, 20(r1)
lwz r3, 0x4(r31)
rlwinm r4,r3,24,16,31 ; (r3 >> 8) & 0xFFFF
bl checkStoryflagIsSet
stb r3, 0x8fd(r31) ; store that it's activated
mr r3, r31 ; replaced instruction
lwz r0, 20(r1)
mtlr r0
addi r1, r1, 0x10
blr
.close

.open "d_t_rock_boatNP.rel"
.org @NextFreeSpace
.global custom_eldin_platform_comparison
custom_eldin_platform_comparison:

stwu r1, -0x10(r1)
mflr r0
stw r0, 0xc(r1)
stw r31, 0x14(r1) ; r31 currently holds a copy of param_1 from before branch

li r4, 0x13 ; story flag 19 - talked to Fire Dragon
bl checkStoryflagIsSet
lwz r31, 0x14(r1) ; restoring param_1 to r31
lwz r0, 0x138(r31) ; normal check val (basically the line of code we replaced)

lwz r4, 0x4(r31) ; params1
cmpwi r4, 0 ; if params1 is not 0 have normal behavior
bne exit

cmpwi r3, 1
beq exit ; if flag is set, skip the next line
li r0, 0 ; forces the false condition
exit:
mr r3, r31
lwz r4, 0xC(r1)
mtlr r4
addi r1, r1, 0x10
blr
.close

.open "d_t_player_restartNP.rel"
.org @NextFreeSpace
; see: https://rust.godbolt.org/
; in rust because why not
; pub fn test(params1: u32, flags: u32) -> u32 {
;     return flags | if ((params1 >> 0x17) & 1) != 0 { 4 } else { 0 };
; }
.global only_set_flag_conditionally
only_set_flag_conditionally:
; r0 holds params1 (how convenient)
; r4 holds some flags, where 4 means don't copy to File B again
rlwinm r5, r0, 11, 29, 29
or r4, r4, r5
ori r4, r4, 0x100 ; we need to signal that the flag, to cause link to use the PlRsTag entrance, needs to be set
blr
.close
