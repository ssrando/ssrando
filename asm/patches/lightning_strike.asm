; changes the skyward strike to lightning (effect only)
.open "main.dol"

.org 0x801c7cb4
nop

.org 0x801c7d14
nop

.org 0x801c7bcc
li r7, 0x63B

.org 0x801c7bd4
li r6, 0x63B

.org 0x801c7bdc
li r4, 0x63B
li r3, 0x63B

.org 0x801e22f0
nop

.org 0x801e22a8
nop

.org 0x801c8048
nop

.org 0x801ca190
li r4, 0x8ae
.close