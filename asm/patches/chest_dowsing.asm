.open "main.dol"

; always register the dowsing target, this is safe since a non initialized dowsing target
; has dowsing index 8, so it's rejected from registering and unregistering
.org 0x80269820
li r3, 1

; select the top dowsing slot when starting a new game file
.org 0x8000ab18
stb r6, 0x53b2(r28)

; get the dowsing slot index from first nibble in params
.org 0x80269788
lwz r0, 0xa8(r28) ; params2
srwi r4,r0,28 ; first nibble
cmplwi r4, 8
bge 0x802697e0 ; branch to handling goddess chest dowsing
bl AcOTBox__initDowsingTarget
b 0x802697e0

; always return true for hasPropellerDowsing, so there's always top dowsing
.org 0x80097bc0
li r3, 1
blr

; fall back to propeller dowsing if you don't have sandship dowsing
.org 0x80098430 ; after checking if you don't have sandship dowsing
beq 0x8009845c ; propeller dowsing image

.close

.open "d_a_obj_warpNP.rel"

; never register trial gate dowsing
.org 0xbf8
nop ; skip over init

.close