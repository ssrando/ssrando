from ssrando import Randomizer


class ItemPool:
    FILLER_ITEMS: list = []

    rando: Randomizer
    progress_items: list
    dungeon_items: list
    nonprogress_items: list
    junk_items: list

    def __init__(self, rando: Randomizer, progress_items: list, dungeon_items: list, nonprogress_items: list, junk_items: list):
        self.rando = rando
        self.progress_items = self.rando.rng.shuffle(progress_items.copy())
        self.dungeon_items = self.rando.rng.shuffle(dungeon_items.copy())
        self.nonprogress_items = self.rando.rng.shuffle(nonprogress_items.copy())
        self.nonprogress_items = self.rando.rng.shuffle(junk_items.copy())

    def get_nonprogress_item(self):
        if len(self.nonprogress_items) <= 0:
            return self.get_junk_item()
        self.nonprogress_items.pop()

    def get_junk_item(self):
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
        return self.progress_items.pop()

    def get_all_progress_items(self):
        return self.progress_items

    def update_progress_pool(self):
        raise NotImplementedError('abstract')

    def make_progress_item_nonprogress(self, item):
        # shuffle the item into the nonprogress pool
        self.nonprogress_items.append(item)
        self.rando.rng.shuffle(self.nonprogress_items)

        # remove from the progress pool (no need to reshuffle)
        self.progress_items.remove(item)

    def make_nonrogress_item_progress(self, item):
        # shuffle the item into the progress pool
        self.progress_items.append(item)
        self.rando.rng.shuffle(self.progress_items)

        # remove from the nonprogress pool (no need to reshuffle)
        self.nonprogress_items.remove(item)
