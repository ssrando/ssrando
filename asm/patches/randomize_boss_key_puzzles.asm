; skip vanilla boss key angle init
.open "d_a_obj_door_bossNP.rel"
.org 0x867C ; 0x80c8facc

bl set_randomized_bk_angles
b 0x86C4 ; 0x80c8fb14

.close