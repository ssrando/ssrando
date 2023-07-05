.open "d_a_shop_sampleNP.rel"

; (808b1da4 - 808b1140) + 130

; keep the shop item addr in r3, not specifically the itemID
.org 0xD78
mr r31, r3

.org 0xD94
bl handle_potion_lady_give_item

.close