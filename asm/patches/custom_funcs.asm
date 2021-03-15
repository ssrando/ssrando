.open "main.dol"
.org @NextFreeSpace

; global shortcut to just simply set a storyflag
.global super_epic_test_func
super_epic_test_func:
nop
nop
nop
nop
blr

.close


.open "d_a_birdNP.rel"
.org @NextFreeSpace
.global loftwing_speed_limit ; expects loftwing actor in r3
loftwing_speed_limit:
lis r6, INPUT_BUFFER@ha ; input buffer
lwz r6, INPUT_BUFFER@l(r6)
andis. r0, r6, 0x4000 ; check for c up pressed
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