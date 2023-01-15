;this is a 2-part patch. in ss_necessary it will remove the isHeroMode check with 3 nops
; replacing this line will keep normalmode behavior.
.open "main.dol"
.org 0x801c5d98
nop
.close