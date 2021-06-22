from ssrando import Randomizer


class ItemPool:
    FILLER_ITEMS: list = [
        "Blue Rupee",
        "Red Rupee",
        "Semi Rare Treasure",
        "Rare Treasure",
    ]

    rando: Randomizer
    progress_items: list
    dungeon_progress_items: list
    nonprogress_items: list
    dungeon_nonprogress_items: list
    junk_items: list

    all_progress_items: list
    all_nonprogress_items: list

    def __init__(self, rando: Randomizer, progress_items: list, dungeon_progress_items: list, nonprogress_items: list,
                 dungeon_nonprogress_items, junk_items: list):
        self.rando = rando
        self.progress_items = self.rando.rng.shuffle(progress_items.copy())
        self.dungeon_progress_items = self.rando.rng.shuffle(dungeon_progress_items.copy())
        self.nonprogress_items = self.rando.rng.shuffle(nonprogress_items.copy())
        self.dungeon_nonprogress_items = self.rando.rng.shuffle(dungeon_nonprogress_items.copy())
        self.nonprogress_items = self.rando.rng.shuffle(junk_items.copy())

        self.all_progress_items = progress_items + dungeon_progress_items
        self.all_nonprogress_items = nonprogress_items + dungeon_nonprogress_items

    def get_nonprogress_item(self):
        """
        Pops and returns the next item in the nonprogress pool
        """
        if len(self.nonprogress_items) <= 0:
            return self.get_junk_item()
        self.nonprogress_items.pop()

    def get_junk_item(self):
        """
        Pops and returns the next item from the junk pool. this method is conscious of the rupoor settings, and will return a
        Rupoor when appropriate. In most cases where a rupoor is explicitly returned the junk pool will remain unmodified
        """
        if self.rando.options['rupoor-mode'] == 'Rupoor Insanity':
            return 'Rupoor'
        if len(self.junk_items) <= 0:
            if self.rando.options['rupoor-mode'] == 'Rupoor Mayhem':  # any added junk items will also be rupoors
                return 'Rupoor'
            return self.rando.rng.choice(self.FILLER_ITEMS)
        if self.rando.options['rupoor-mode'] == 'Rupoor Mayhem':
            if self.rando.rng.random() <= 0.5:  # 50% chance that any junk item is a rupoor
                return 'Rupoor'
        return self.junk_items.pop()

    def get_progress_item(self):
        """
        Pops and returns the next item from the progress pool
        """
        return self.progress_items.pop()

    def get_dungeon_progress_item(self):
        """
        Pops and returns the next item from the dungeon item pool
        """
        return self.dungeon_progress_items.pop()

    def get_dungeon_nonprogress_item(self):
        """
        Pops and returns the next item from the dungeon nonprogress pool
        """
        return self.dungeon_nonprogress_items.pop()

    def update_progress_pool(self):
        """
        Updates the progress pool based on the settings for the randomizer
        """
        raise NotImplementedError('abstract')

    def make_progress_item_nonprogress(self, item):
        """
        Makes a previously progress item a nonprogress pool item, exchanging the item between the two subpools. This process
        results in the nonprogress pool being reshuffled
        """
        # shuffle the item into the nonprogress pool
        self.nonprogress_items.append(item)
        self.rando.rng.shuffle(self.nonprogress_items)

        # remove from the progress pool (no need to reshuffle)
        self.progress_items.remove(item)

    def make_nonrogress_item_progress(self, item):
        """
        Makes a previously nonprogress item a progress item in the pool, basically exchanging the item between the subpools.
        This results in the progress pool being reshuffled
        """
        # shuffle the item into the progress pool
        self.progress_items.append(item)
        self.rando.rng.shuffle(self.progress_items)
        self.all_progress_items.append(item)

        # remove from the nonprogress pool (no need to reshuffle)
        self.nonprogress_items.remove(item)
        self.all_nonprogress_items.remove(item)

    def remove_item(self, item):
        """
        Removes a single instance of an item from the item pool, regardless sof which subpool it is in
        """
        if item in self.progress_items:
            self.progress_items.remove(item)
            self.all_progress_items.remove(item)
        elif item in self.dungeon_progress_items:
            self.dungeon_progress_items.remove(item)
            self.all_progress_items.remove(item)
        elif item in self.nonprogress_items:
            self.nonprogress_items.remove(item)
            self.all_nonprogress_items.remove(item)
        elif item in self.dungeon_nonprogress_items:
            self.dungeon_nonprogress_items.remove(item)
            self.all_nonprogress_items.remove(item)
        else:  # if it hasn't appeared anywhere else, it is either junk or doesn't exist at all
            self.junk_items.remove(item)
