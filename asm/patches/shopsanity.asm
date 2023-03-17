.open "d_a_shop_sampleNP.rel"
.org 0x11A0
; in function that sets up the shopitem classes, check if this
; is an item that uses the patched extra wallet class
bl check_needs_custom_storyflag_subtype

.org 0x1224
; this normally sets up the bug net, but this is already handled and uses the extra wallet class
; so it's essentially free space
; we need to branch for the extra pouches now, cause otherwise pouch items use a different shop item class
cmplwi r4, 0x14 ; extra pouch 1 (300R)
beq 0x12C8
cmplwi r4, 0x15 ; extra pouch 2 (600R)
beq 0x12D8
cmplwi r4, 0x16 ; extra pouch 3 (1200R)
beq 0x12E8
b 0x1250 ; skip rest of this block


; patches to make the extra wallet class use the last 2 bytes of the shop sample list as storyflag to check if it's sold out
.org 0xAA0
nop ; checks if the extra wallet bought counter is >= 3, even though this should never be met, nop the branch anyways

; end of function that gives the item, change it so that it sets the storyflag for having bought this shop item
.org 0xACC 
lhz r31, 0xC(r3) ; load itemid
lhz r3, 0x52(r3) ; load storyflag to set
li r4, 1 ; storyflag will be set to true
bl setStoryflagToValue
mr r3, r31
li r4, -1
li r5, 0
bl giveItem
lwz r0, 0x14(r1)
lwz r31, 0xC(r1)
lwz r30, 0x8(r1)
mtlr r0
addi r1,r1,0x10
blr

; this is the function that checks, if the extra wallet class is supposed to be sold out
; and advance to the next item in the chain
; change it, so that it checks the storyflag from the shop sample list
.org 0xA00
lhz r3, 0x0(r3) ; shop item id
lis r4, SHOP_ITEMS@ha
addi r4, r4, SHOP_ITEMS@l ; load shop item table
mulli r3, r3, 0x54 ; array offset
add r3, r3, r4 ; array offset
lhz r4, 0x52(r3) ; load storyflag
b checkStoryflagIsSet

; .org 0x808b43c8
.org 0x33B8
lhz r28, 0xC(r6) ; make the item id accessible for the next function
nop ; this overwrites a useless call to sprintf, probably debug leftover
nop

; .org 0x808b43e4
.org 0x33D4
li r6, 0x123 ; model flags, otherwise the texture anim is shared

; .org 0x808b43f4
.org 0x33E4
bl correct_rupee_color

; Custom item height struct stuff
; SHOP_ITEM[0x4C] = float of height offset
; .org 0x808b66ec
.org 0x56DC
lfs f0, 0x4C(r3); load custom height value into f0
stfs f0, 0x4(r31); store custom height for shop item
b 0x5740

; Remove the null height value
; .org 0x808b67e8
.org 0x57D8
nop; stops the new height from being overwritten

.close