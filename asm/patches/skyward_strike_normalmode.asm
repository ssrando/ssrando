; all changes replace the isHeroMode check with a constant 0 to indicate normal mode
.open "main.dol"
; possibly dealing with skyward sword charge speed?
.org 0x8005e288 
li r3, 0x0

; possibly dealing with skyward sword charge speed?
.org 0x8005e2ac
li r3, 0x0

; spin attack related?
.org 0x801c7a3c
li r3, 0x0

.org 0x801c7b70
li r3, 0x0

.org 0x801ca16c
li r3, 0x0

.org 0x801e21e4
li r3, 0x0

.close