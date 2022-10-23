.open "main.dol"
; allow dowsing in dungeons
.org 0x80208304
li r3, 0x0 ; remove stage check
.close