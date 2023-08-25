.open "main.dol"
; replaces isHeroMode with a constant 0x0 to make sure hearts always spawn
; in item init
.org 0x8024acf8
li r3, 0x0

; in some func related to chance-based heart spawns / digspots / pots?
.org 0x800c7c50
li r3, 0x0
.close

.open "d_a_heartfNP.rel"
; This is in init1 and decides whether or not its spawned.
; replaces isHeroMode with a constant 0x0 to make sure hearts always spawn
; 0x80c925d8 in Ghidra
.org 0x848
li r3, 0x0
.close

.open "d_a_e_maguppoNP.rel"
; 0x80d1fd88 in Ghidra
; replaces isHeroMode with a constant 0x0 to make sure hearts always can spawn
.org 0x1338
li r3, 0x0
.close

.open "d_a_obj_asura_pillarNP.rel"
; 0x80c2027c in Ghidra
; replaces isHeroMode with a constant 0x0 to make sure hearts always can spawn
.org 0x9ec
li r3, 0x0
.close

.open "d_t_reactionNP.rel"
; 0x80efced4 in Ghidra (80efced4 - 80efc9e0) + 130
; replaces isHeroMode with a constant 0x0 to make sure hearts always can spawn
.org 0x624
li r3, 0x0
.close