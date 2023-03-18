.open "main.dol"

; overwrite the patch in ss_necessary to set the startflags
; set the interface, then the startflags
.org 0x801bb9bc
b interface_light

.close