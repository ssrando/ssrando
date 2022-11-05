.open "main.dol"
.org 0x801e346c ; checks for hero mode for damage doubling
nop ; don't branch away if normal mode
; shift damage 8 bits left (256x), ensures death even on normal mode + guardian potion
rlwinm r27,r27,0x8,0x0,0x1e
.close