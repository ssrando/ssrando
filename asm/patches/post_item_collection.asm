; Custom hook to do things after collecting an item
.open "main.dol"
.org 0x80252df0
bl after_item_collection_hook
.close