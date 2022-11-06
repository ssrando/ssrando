.open "main.dol"
.org 0x801e346c ; checks for hero mode for damage doubling
nop ; don't branch away if normal mode
; load highest possible negative damage amount
li r27, -32768
.close