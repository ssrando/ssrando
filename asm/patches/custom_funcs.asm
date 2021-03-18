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