.open "d_a_obj_door_bossNP.rel"
; in the __sinit function, use a custom randomization function to set
; the initial BK angles
; this replaces some useless, stupid code
; .org 0x80c8fde4
.org 0x8994
lis r4, 0
ori r4, r4, 0
mr r3, r25
bl randomize_boss_key_start_pos
li r3, 0 ; mock what strlen returns

.close