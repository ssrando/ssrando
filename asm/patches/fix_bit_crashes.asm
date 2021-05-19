.open "main.dol"

.org 0x801b9a14
bl alloc_keyboard_arcs_conditional
.org 0x801b9a48
bl alloc_keyboard_arcs_conditional

.org 0x801b9b70
nop ; don't deref pointer to keyboard arc, could be null
nop
nop
nop

.org 0x801b9b94
nop
nop
nop
nop

.close