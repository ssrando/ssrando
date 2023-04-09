.open "main.dol"

; patch all boss keys and maps (which have 2 as their item set flagtype)
; to set their flag through a custom function that works everywhere
.org 0x80251d04
mr r3, r30
bl handle_bk_map_dungeonflag
b 0x80251d48


; patch small key collection to use function that works everywhere
; replaces li r3, 5, which is done at the end of the function
.org 0x80253cf8
bl handleSmallKeyGet


; assign model index for small keys and maps
.org 0x804e8f40
; make items 200 to 206 (inclusive) small keys for their dungeon
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


; need for the item get animation
; the good game SS is, it assumes the best default and crashes
.org 0x804ECC9C
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
.int 0 ; item 214


; Allow getting arbitrary models in getItemModelForItem
; replace call to getModelDataFromOarc
; uses space from duplicate null check
.org 0x8016fb00
mr r25, r5 ; keep param3
mr r5, r26 ; get itemId into r5
bl get_item_arc_name
mr r5, r25 ; restore param3
stw r3, 0xc(r1)

; replace null check
cmpwi r3, 0
bne 0x8016fb24

; replace getting model name
.org 0x8016fc38
bl get_item_model_name


; Create AcItem__mainModel for custom items
; add additional case to AcItem::initModels
.org 0x8024a9d4
b is_custom_rando_item


; fix item get height and scale for custom items
.org 0x8024d924
addi r4, r1, 0x30
bl fix_custom_item_get
nop
nop
nop
nop

; custom tadtone item get height
.org 0x8057be3c
.float -25.0

.close
