.open "main.dol"
; The subtype of TBox (chests) is determined by the item id
; change it, so that it uses 00 00 00 30 of params1 instead
.org 0x80269530 ; in AcOTBox::init
lwz r0, 0x4(r28) ; load params1
rlwinm r0,r0,28,30,31 ; r0 = (r0 >> 4) & 3
stb r0, 0x1209(r28) ; store subtype
cmplwi r0, 3 ; TODO: remove this
b 0x80269554

.org 0x80115A04 ; in some function that is text advancing related
li r4, 1 ; enables instant text

; patch to not update sword model when getting an upgrade
.org 0x8005e2f0
stwu r1, -0x30(r1)
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
b 0x8024a1c0 ; get subtype out of params1
.org 0x80254150
cmpwi r3, 9
beq 0x80254168

; don't show fi text after map
.org 0x80252b48
b 0x80252bb4

; function that checks if the item is the bird statuette
; always return false to fix the animation
.org 0x80250b00
li r3, 0
blr

; this function checks if a checkflag is set, always return true
.org 0x800bfd20
li r3, 1
blr

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
mr r0, r0 ; nice nop idiot

; special text when entering faron pillar during SotH, skip over it
.org 0x80141f00
b 0x80141f44

.close

;.open "d_a_obj_door_boss.rel"
;; 80f0233c, to 80f0229c
;.org 0xC1C
;blt 0xCBC
.close