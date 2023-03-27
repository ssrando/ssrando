.open "main.dol"
.org 0x802e0d00
lis r3, 0x443b
ori r3, r3, 0x4723
stw r3, -0x38a0(r13) ; RNG
blr
.close

.open "d_a_nusi_baseNP.rel"
; .org 0x80bd7060
.org 0x12D0
; don't call random, just go backwards in order
subi r3, r3, 1

; ,org 0x80bd7078
.org 0x12E8
b 0x12D0

.close

.open "d_a_obj_hole_minigameNP.rel"
; use a better seed
; .org 0x80d5c5e4
.org 0x1D14
lis r12, 0x3e8b
ori r12, r12, 0x395f
stw r12, -0x38a0(r13) ; RNG

; jump over useless 2x2 bad stuff check after restoring rng
; .org 0x80d5c628
.org 0x1D58
bl initRng
; b 0x80d5c728
b 0x1E58

; nop restore instructions, since the regs were never saved
; .org 0x80d5c734
.org 0x1E64
nop
nop
nop
.close
