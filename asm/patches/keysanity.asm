.open "main.dol"
.org 0x80251d04
; patch all boss keys and maps (which have 2 as their item set flagtype) to set their flag through a custom function
; that works everywhere
mr r3, r30
bl handleBossKeyMapDungeonflag
b 0x80251d48

.org 0x80253cf8
; patch small key collection to use function that works everywhere
; replaces li r3, 5, which is done at the end of the function
bl handleSmallKeyGet

; make items 200 to 206 (inclusive) small keys for their dungeon
.org 0x804e8f40
.word 0 ; SV
.word 0 ; LMF
.word 0 ; AC
.word 0 ; FS
.word 0 ; SS
.word 0 ; SK
.word 0 ; Caves
; then maps (from 207 to 213)
.word 0x2A ; SV
.word 0x2A ; ET
.word 0x2A ; LMF
.word 0x2A ; AC
.word 0x2A ; FS
.word 0x2A ; SS
.word 0x2A ; SK

.org 0x804ECC9C ; need for the animation. The good game SS is, it assumes the best default and crashes
.int 0 ; item 201
.int 0 ; item 202
.int 0 ; item 203
.int 0 ; item 204
.int 0 ; item 205
.int 0 ; item 206
.int 0x1000 ; item 207
.int 0x1000 ; item 208
.int 0x1000 ; item 209
.int 0x1000 ; item 210
.int 0x1000 ; item 211
.int 0x1000 ; item 212
.int 0x1000 ; item 213
.close