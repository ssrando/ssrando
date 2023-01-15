.open "main.dol"
; Stars :D
.org 0x801aaf28
b 0x801ab0f8

; Remove weird camera culling on Skyloft and The Sky
.org 0x801ab6fc ; check for Skyloft stage
nop
.org 0x801ab70c ; check for Sky stage
b 0x801ab790

.close