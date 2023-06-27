.open "main.dol"
; The subtype of TBox (chests) is determined by the item id
; change it, so that it uses 00 00 00 30 of params1 instead
.org 0x80269530 ; in AcOTBox::init
lwz r0, 0x4(r28) ; load params1
rlwinm r0,r0,28,30,31 ; r0 = (r0 >> 4) & 3
stb r0, 0x1209(r28) ; store subtype
b 0x80269554

.org 0x80115cf8 ; non-final text box
bl textbox_a_pressed_or_b_held ; change button function

.org 0x80115f98 ; final text box
bl textbox_a_pressed_or_b_held ; change button function

; Make all skippable event be skippable without waiting 4 frames
.org 0x800a0968 ; if 2 button is being held
li r3, 1 ; return true instead of waiting 4 frames
b 0x800a09a0

; Show all text in a textbox at once
.org 0x80115A04 ; in some function that is text advancing related
li r4, 1 ; enables instant text

; Fast textboxes advancing
.org 0x8010f5f4 ; checks what some textbox state stuff
b 0x8010f654 ; branch to (unused??) block that sets textboxes to be clearable

; Fast textbox appearing - makes textbox blur go weird
.org 0x8011593c
nop

; Remove textbox blur
.org 0x800b3370
blr

; Remove Fi text janky appearing
; (equivalent to removing textbox blur for Fi text)
.org 0x80120c60
blr

; remove text pauses
; copies instruction for just ignoring a command
.org 0x800b2774
lhz r3, 0x147a(r26)
addi r0, r3, 1
sth r0, 0x147a(r26)

; remove sword item from sword pedestal and give new story flag 951
.org 0x801d45ec
bl set_goddess_sword_pulled_scene_flag

; Sword pedestal textbox removal
.org 0x801d4b20
li r5, -1

; Change starting location to remove intro cutscenes
.org 0x801bb960 ; Change starting stage
subi r3, r13, 0x5b44 ; previously 0x601c (F405 -> F001r)

.org 0x801bb964 ; Change starting roomID
li r4, 1 ; Room 0 -> 1

.org 0x801bb968 ; Change starting layer
li r5, 3 ; Layer 0 -> 3

.org 0x801bb96c ; Change starting entrance
li r6, 5 ; Entrance 0 -> 5

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

; allow triforces to fall down when bonked
.org 0x8024edbc
li r3, 0

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
lwz r3, ITEMFLAG_MANAGER@sda21(r13)
li r4, 0x1F6 ;gratitude crystals
bl FlagManager__getUncommittedFlags
lwz r4, LYT_MSG_MANAGER@sda21(r13)
lwz r4, 0x724(r4) ;Text Manager
stw r3, 0x8A0(r4) ;text counter 1
lwz r0, 0x24(r1) ; instruction that was overwritten
b 0x802539e0

; change top priority dowsing icon to sandship
.org 0x800983ec ; checks zelda dowsing
b 0x80098428 ; checks sandship dowsing

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
b process_startflags

; always allocate keyboard arcs to the end of the heap, to make sure
; faron BiT doesn't crash
.org 0x801b9a10
li r5, 2
.org 0x801b9a44
li r5, 2

; when loading a stage
.org 0x80198dc0
bl unset_sandship_timestone_if_necessary

; replace check for sword with check for not trial
.org 0x80221aa8
lis r3, SPAWN_SLAVE+0x26@ha
lbz r3, SPAWN_SLAVE+0x26@l(r3)
cmplwi r3, 1

; remove goddess sword requirement to call fi
.org 0x80221b50
nop

; don't prevent calling fi in water
.org 0x80221b5c
nop

; force the language to be english
.org 0x803d6630
li r3, 1 ; 1 is english
blr

; always return true when checking if a treasure/insect was obtained this play session
.org 0x80252edc
li r3, 1

; optimize some code around separating textfileindex from entrypoint
; to then temporarily backup the current textfileindex
; this fixes potential crashes when initiating a conversation while a Npc updates for the first time
.org 0x800c41f8
mullw r5, r4, r5
subf r5, r5, r28
rlwinm r5, r5, 0, 0x10, 0x1F
lwz r6, GLOBAL_MESSAGE_RELATED_CONTEXT@sda21(r13)
lwz r28, 0x2f8(r6) ; currentTextFileNumber
b 0x800c4220 ; skip stuff we don't need anymore

; restore the backed up text file number
; the destructor here does nothing so we can overwrite it
.org 0x800c4240
lwz r6, GLOBAL_MESSAGE_RELATED_CONTEXT@sda21(r13)
stw r28, 0x2f8(r6) ; currentTextFileNumber

; always use non trial mode when using loadzones
.org 0x80242060
li r7, 0 ; force non trial

; treat all Kikwi's as "found" in non main faron stages
.org 0x8004ec24
; make sure this branch is always taken, should always be the case anyways
b 0x8004ec30
li r3, 1 ; code below jumps here when not in faron main
.org 0x8004ec44
lis r4, SPAWN_SLAVE+2@ha
lhz r4, SPAWN_SLAVE+2@l(r4)
cmplwi r4, 0x3030 ; '00', we assume all stages like XX00 are faron main
bne 0x8004ec28 ; if not faron main, treat this kikwi as found

; this is to remove code to be overwritten in gamepatches.py (around line 1260) - Damage multiplier
.org 0x801e3468
nop
nop
nop

; we need to make sure you can't die in thrill digger and bug heaven, even with a high damage multiplier
.org 0x801e351c
bl no_minigame_death

;remove heromode check for air meter
.org 0x801c5d8c
nop
nop
nop

; branch to function for rando custom text event flows (if no other matches)
.org 0x801aff2c
bgt 0x801b0788
.org 0x801b0788
bl rando_text_command_handler
b 0x801b0764 ; return to original function

; here is the required sequence of buttons stored,
; to get the crash screen to show up, since it's 0 terminated,
; overwriting the first element with 0 will make it not check any buttons
.org 0x804dba00
.word 0

; allow collecting items underwater
.org 0x8025685c
bl allow_item_get_underwater

; Update branches
.org 0x802511f4
beq 0x80251208
.org 0x802511fc
beq 0x80251208

; If getting an big item underwater, act like a small item
; Fixes janky item get animation underwater
; Uses excess space from multiple copies of the same code
.org 0x8025121c
; r5 is re-assigned after this
lwz r5, LINK_PTR@sda21(r13) ; get LINK_PTR
lwz r5, 0x364(r5) ; get actionflags
rlwinm. r5, r5, 0x0, 0xd, 0xd ; is Link in water?
cmpwi r5, 0
bne 0x80251208 ; if in water, use DefaultGetItem event
nop

; Modify STORYFLAG_DEFINITIONS to allow flag 953 to be a counter
; STATIC_STORYFLAGS[index] = 805a9b7e
; shiftMask uses 7 lsb for the counter (max value of 128)
; shiftMask >> 4 = 0 so:
; Story Flag #953 (0x03B9) - US from 805A9B7E 0x01 to 805A9B7E 0x40
.org 0x80511502
.byte 0x53 ; index
.byte 0x7  ; shiftMask


; allow tadtone dowsing after getting hasCollectedAllTadtones flag
.org 0x80097b84
nop
nop
nop
nop
nop
nop
nop
nop

; Show Tadtone Scroll even after getting Water Dragon's Reward
.org 0x80299ca8
nop
nop
nop
nop

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
lwz r3, STORYFLAG_MANAGER@sda21(r13)
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

; this usually delays starting the trial finish event until the
; tear display is ready, which can softlock so skip the check,
; which seems to only have a visual impact *at worst*
;
; instead check if link finished his walk, otherwise it can still softlock
;
; preferably, the tear display should be fixed, but this works for now
.org 0x1A9c
lbz r0, 0xc90(r30)

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
bl enforce_loftwing_speed_cap
nop
nop
nop

.org 0x9FB4 ; 809b712c in ghidra
nop ; don't cap speed here

.org 0x9FC4 ; belongs to function above, instead of blr, branch to loftwing_speed_limit function at the end
ble skip_store_max
stfs f0,0xfb8(r3)
skip_store_max:
b enforce_loftwing_speed_cap
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
bge 0x2650 ; instead of only checking for White Sword for the last reward, check for at least that

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

.open "d_t_skyEnemyNP.rel"
.org 0x1270
lis r3, 0x46DF ; float 28544.0, replaces 12000
.org 0x1280
stw r3, 0x30(r1)
.close

.open "d_a_obj_tornadoNP.rel"
.org 0x920 ; thanks to 16 byte alignment, we can just insert 2 instructions here
lis r4, 0x47DF ; float 114176.0, just arbitrarily large to not make the tornado despawn
stw r4, 0x1A4(r31) ; culling distance, most likely
lwz r31, 0x3C(r1)
lwz r30, 0x38(r1)
mtlr r0
addi r1, r1, 0x40
blr
.close

.open "d_a_obj_swrd_prjNP.rel" ; goddess wall
.org 0x4D48
b 0x4D70 ; skip over code checking for skyview mogma storyflag
.org 0x5024
b 0x5070 ; skip over code checking for scale and BotG (we check for BotG somewhere else again)
.org 0x63E8
bl reveal_goddess_wall_check ; require BotG here

.close

.open "d_t_insectNP.rel"
.org 0xC70
li r4, 9 ; change goddess wall requirement from scale to harp
.org 0xBC4
li r4, 9 ; change goddess wall requirement from imp1 to harp

; fix trial storyflags
.org 0x9DC
li r4, 0x397 ; new storyflag

.org 0xA1C
li r4, 0x398

.org 0xA68
li r4, 0x399

.org 0xAB4
li r4, 0x39A
.close

.open "d_a_obj_bellNP.rel"
.org 0xCE0 ; function called when transitioning to the state after dropping rupee
b try_end_pumpkin_archery
.close

.open "d_a_obj_light_lineNP.rel"
.org 0xDAC
bl check_activated_storyflag
.close

; Force Sword in pedestal
.open "d_a_obj_seat_swordNP.rel"
.org 0x10F4
li r4, 951 ; story flag for raising sword
.close

.open "d_a_obj_bridge_buildingNP.rel"
; .org 0x80d6a858
; change frames for bridge to extend
.org 0x6E8
li r4, 0x1b

; .org 0x80d6b7e0
; max extension speed
.org 0x1674
.float 70.0

; .org 0x80d6ad30
; change frames for bridge to extend 2
.org 0xBC0
li r4, 0x1b

; .org 0x80d6ac0c
; don't wait on event when there is no event
.org 0xA9C
beq 0xAF0 ; 0x80d6ac60
.close

.open "d_t_player_restartNP.rel"
.org 0x458
; see the custom function for an explanation
bl only_set_flag_conditionally
.org 0x49C
rlwinm. r0, r0, 0, 23, 23 ; check & 0x100 now
.close

.open "d_a_obj_toD3_stone_figureNP.rel"
; .org 0x80f35a18
.org 0x8E8
b set_sot_placed_flag
.close

; make sure groose stays at his groosenator after finishing faron SotH
.open "d_a_npc_bbrvlNP.rel"
; .org 0x80992b24
.org 0x4214
li r3, 0 ; act as if storyflag 16 is not set
; .org 0x80992870
.org 0x3f60
li r3, 0 ; act as if storyflag 16 is not set
; .org 0x80992610
.org 0x3d00
li r3, 0 ; act as if storyflag 16 is not set
; .org 0x8099fe74
.org 0x11564
li r3, 0 ; act as if storyflag 16 is not set
; .org 0x8099ff1c
.org 0x1160c
li r3, 0 ; act as if storyflag 16 is not set
; .org 0x809a0528
.org 0x11c18
li r3, 0 ; act as if storyflag 16 is not set
.close


.open "d_a_obj_clefNP.rel"

; (addr - text0) + offset
; (0x - 0x80ea8380) + 0x130

; Allow anglez to be used to store the item id
.org 0x104C ; 0x80ea929c
nop ; don't overwrite anglez with zero

.org 0x17AC ; 80ea99fc
li r0, 0 ; replace anglez with zero since it's only used for this


; Still init clef actors even if hasCollectedAllTadtones flag is set
.org 0xA58 ; 0x80ea8ca8
nop
nop
nop
nop
nop

;;;;;;;;;;;;;;;;;;
;;; Give items ;;;
;;;;;;;;;;;;;;;;;;
; Give item when in STATE_WAIT_UPDATE
.org 0x1CA4 ; 0x80ea9ef4
mr r4, r29 ; move self into r4
bl give_random_item_from_collecting_tadtone_group

; Give item when in STATE_MOVE_TOWARD_PATH_UPDATE
.org 0x236C ; 0x80eaa5bc
mr r4, r29 ; move self into r4
bl give_random_item_from_collecting_tadtone_group

; Give item when in STATE_PATH_MOVE_UPDATE
.org 0x28EC ; 0x80eaab3c
mr r4, r29 ; move self into r4
bl give_random_item_from_collecting_tadtone_group

; Give item when in STATE_GRAVITATE
.org 0x303C ; 0x80eab28c
mr r4, r29 ; move self into r4
bl give_random_item_from_collecting_tadtone_group
.close


.open "d_t_clef_gameNP.rel"

; (addr - text0) + offset
; (0x - 0x80ee7a60) + 0x110

; Still init clef game even if hasCollectedAllTadtones flag is set
.org 0x2C8 ; 0x80ee7c18
nop
nop
nop
nop
nop

; don't delyeet yourself p l e a s e
; ensure TgClefGame always exists when in Flooded Faron Woods
.org 0x3B4 ; 0x80ee7d04
nop

.org 0x3BC ; 0x80ee7d0c
bl check_tadtone_counter_before_event

; Check for hasCollectedAllTadtones after managing vanilla tadtones
.org 0x45C ; 0x80ee7dac
b 0x3A4 ; 0x80ee7cf4 check for hasCollectedAllTadtones

; re-write return to use extra instruction space at end of function
; not very elegant but works better than re-writing the whole function
; now starts at 0x80ee7db0
lwz r31, 0x4c(r1)
li r3, 1
lwz r30, 0x48(r1)
lwz r0, 0x54(r1)
mtlr r0
addi r1, r1, 0x50
blr

; update return branches to use new address 0x80ee7db0
.org 0x3B8 ; 0x80ee7d08
b 0x460
.org 0x3D8 ; 0x80ee7d28
bne 0x460
.org 0x3E8 ; 0x80ee7d38
beq 0x460
.org 0x434 ; 0x80ee7d84
b 0x460

.close

.open "d_a_obj_time_boatNP.rel"

; 0x80e20260 in ghidra, seems to be some base multiplier at 0.3 (but changing this to something
; less than 1 doesnt seem to change anything?)
.org 0x5d74
.float 1.5 ; seems to make the boat go 1.5x faster

; 0x80e20274 in ghidra, sand sea boat sprint speed multiplier
.org 0x5d88
.float 3.0 ; original sprint speed multiplier is 2.0, so total speed difference is 2.25x

.close