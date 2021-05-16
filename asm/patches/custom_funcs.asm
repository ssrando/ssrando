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
lwz r3,-0x4044(r13) ; STORYFLAG_MANAGER
lwz r12, 0x0(r3)
lwz r12, 0x28(r12)
mtctr r12
bctr

; replaces the normal boss key get logic with one, that works everywhere
; datatable for boss key itemid to flagindex
bosskey_to_flagindex:
.byte 12; AC
.byte 15; FS
.byte 18; SS
.byte 13; eldin key piece, just use an unused index since this should never happen
.byte 11; SV
.byte 14; ET
.byte 17; LMF
.align 4
map_to_flagindex:
.byte 11 ; SV
.byte 14 ; ET
.byte 17 ; LMF
.byte 12 ; AC
.byte 15 ; FS
.byte 18 ; SS
.byte 20 ; SK
.align 4
.global handleBossKeyMapDungeonflag
handleBossKeyMapDungeonflag:
stwu r1, -0x10(r1)
mflr r0
stw r0, 20(r1)
stw r31, 12(r1) ; r31 is flagindex of the dungeon, r30 is the mask if it's a map or a boss key
stw r30, 8(r1)
addi r4, r3, -25 ; fist boss key
cmplwi r4, 6
bgt handle_map ; is not a boss key
li r30, 0x80
lis r5, bosskey_to_flagindex@ha
addi r5, r5, bosskey_to_flagindex@l
lbzx r31, r4, r5
b set_dungeonflag
handle_map:
addi r4, r3, -207 ; first map
cmplwi r4, 6
bgt bkget_func_end ; neither map nor boss key
li r30, 0x02
lis r5, map_to_flagindex@ha
addi r5, r5, map_to_flagindex@l
lbzx r31, r4, r5
set_dungeonflag:
lwz r3,-0x403c(r13) ; DUNGEONFLAG_MANAGER
lha r0, 2(r3)
cmpw r0, r31 ; check if dungeon item is for current area
bne handle_other_area
lwz r4, 8(r3)
lhz r0, 0(r4) ; load static dungeonflag that also has the boss key and map flag
or r0, r0, r30
sth r0, 0(r4) ; set flag and write back
li r0, 1
stb r0, 0(r3) ; set commit flag
b bkget_func_end
handle_other_area:
lwz r3,-0x4444(r13) ; FILE_MANAGER
bl FileManager__getDungeonFlags
rlwinm r4, r31, 4, 0, 27 ; flagindex * 16
lhzx r0, r3, r4 ; load byte from the saved dungeonflags that also has the boss key and map flag
or r0, r0, r30
sthx r0, r3, r4 ; set flag and write back
bkget_func_end:
lwz r30, 8(r1)
lwz r31, 12(r1)
lwz r0, 20(r1)
mtlr r0
addi r1, r1, 0x10
blr


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
lwz r3,-0x403c(r13) ; DUNGEONFLAG_MANAGER
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
lwz r3,-0x4444(r13) ; FILE_MANAGER
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

.global alloc_only_if_no_first_file
alloc_only_if_no_first_file:
; can't use r3, r4, r5, r6
lwz r12, -0x3cb4(r13) ; LINK_PTR
lwz r12, 0x4(r12) ; link params
xoris r12, r12, 0xFFFF ; check for 0xFFFF0FFF, actor params on title screen, are different in BiT
cmpwi r12, 0x0FFF
beq do_requestFileLoadFromDisk
lwz r12,-0x4444(r13) ; FILE_MANAGER
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
lwz r3,-0x3cac(r13) ; RELOADER_PTR
li r4, 0 ; current room, all rooms in skykeep are room 0 
li r5, 1 ; take exit 1, it's always the skyloft exit
li r6, 2 ; idk
li r7, 2 ; idk
b Reloader__triggerExit
.close

.open "d_a_obj_warpNP.rel"
.org @NextFreeSpace
.global check_should_delay_walk_out_event
check_should_delay_walk_out_event:
mr r4, r3
lbz r3, 0xc7d(r4) ; counter, in the original actor this was the itemid to wait on (all code that uses it is skipped)
cmpwi r3, 5 ; only increment it to an arbitrary amoung
bgelr
addi r3, r3, 1 ; increment
stb r3, 0xc7d(r4) ; store counter back

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
lwz r3,-0x3cb4(r13) ; LINK_PTR
addi r4, r1, 8
li r5, 0
li r6, 0
li r7, 1
li r8, 0
bl ActorLink__setPosRot
lwz r3,-0x4060(r13) ; SCENEFLAG_MANAGER
li r4, 50
bl SceneflagManager__checkTempOrSceneflag
cmpwi r3, 0
bne longsword_reward_check
lwz r0, 0x4(r31)
rlwinm r3,r0,8,24,31
li r4, -1
li r5, 0
bl giveItem
lwz r3,-0x4060(r13); SCENEFLAG_MANAGER
li r4, 50
bl SceneflagManager__setTempOrSceneflag
longsword_reward_check:
lbz r0,-0x77cc(r13); EQUIPPED_SWORD
cmplwi r0, 2
blt function_end
lwz r3,-0x4060(r13); SCENEFLAG_MANAGER
li r4, 51
bl SceneflagManager__checkTempOrSceneflag
cmpwi r3, 0
bne whitesword_reward_check
lwz r0, 0x4(r31)
rlwinm r3,r0,16,24,31
li r4, -1
li r5, 0
bl giveItem
lwz r3,-0x4060(r13); SCENEFLAG_MANAGER
li r4, 51
bl SceneflagManager__setTempOrSceneflag
whitesword_reward_check:
lbz r0,-0x77cc(r13); EQUIPPED_SWORD
cmplwi r0, 3
blt function_end
lwz r3,-0x4060(r13); SCENEFLAG_MANAGER
li r4, 52
bl SceneflagManager__checkTempOrSceneflag
cmpwi r3, 0
bne function_end
lwz r0, 0xa8(r31)
rlwinm r3,r0,8,24,31
li r4, -1
li r5, 0
bl giveItem
lwz r3,-0x4060(r13); SCENEFLAG_MANAGER
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

.close
