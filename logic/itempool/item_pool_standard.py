from ssrando import Randomizer
from .item_pool import ItemPool


class StandardItemPool(ItemPool):
    def __init__(self, rando: Randomizer):
        super().__init__(
            rando,
            [  # progress items
                "Slingshot",
                "Bomb Bag",
                "Gust Bellows",
                "Whip",
                "Bow",
                "Bug Net",
                "Water Scale",
                "Fireshield Earrings",
                "Clawshots",
                "Stone of Trials",
                "Sea Chart",
                "Emerald Tablet",
                "Ruby Tablet",
                "Amber Tablet",
                "Baby Rattle",
                "Cawlin's Letter",
                "Horned Colossus Beetle",
                "Goddess Harp",
                "Ballad of the Goddess",
                "Farore's Courage",
                "Nayru's Wisdom",
                "Din's Power",
                "Faron Song of the Hero Part",
                "Eldin Song of the Hero Part",
                "Lanayru Song of the Hero Part",
                "Spiral Charge"
            ]
            + ["Gratitude Crystal Pack"] * 13
            + ["Gratitude Crystal"] * 15
            + ["Progressive Sword"] * 6
            + ["Progressive Mitts"] * 2
            + ["Progressive Beetle"] * 2
            + ["Progressive Pouch"] * 5
            + ["Key Piece"] * 5
            + ["Empty Bottle"] * 5
            + ["Progressive Wallet"] * 4
            + ["Extra Wallet"] * 3,
            (  # dungeon items
                ["LanayruCaves Small Key"] * 1
                + ["SV Boss Key"] * 1
                + ["SV Small Key"] * 2
                + ["ET Boss Key"] * 1
                + ["ET Small Key"] * 0
                + ["LMF Boss Key"] * 1
                + ["LMF Small Key"] * 1
                + ["AC Boss Key"] * 1
                + ["AC Small Key"] * 2
                + ["SS Boss Key"] * 1
                + ["SS Small Key"] * 2
                + ["FS Boss Key"] * 1
                + ["FS Small Key"] * 3
                + ["SK Boss Key"] * 0
                + ["SK Small Key"] * 1
            ),
            [  # nonprogress items
                "Wooden Shield",
                "Hylian Shield",
                "Cursed Medal",
                "Treasure Medal",
                "Potion Medal",
                "Small Seed Satchel",
                "Small Bomb Bag",
                "Small Quiver",
                "Bug Medal",
            ]
            + ["Heart Medal"] * 2
            + ["Rupee Medal"] * 2
            + ["Heart Piece"] * 24
            + ["Heart Container"] * 6
            + ["Life Medal"] * 2,
            (  # dungeon nonprogress items
                ["SV Map"]
                + ["ET Map"]
                + ["LMF Map"]
                + ["AC Map"]
                + ["SS Map"]
                + ["FS Map"]
                + ["SK Map"]
            ),
            (  # junk items
                4 * ["Blue Rupee"]
                + 25 * ["Red Rupee"]
                + 12 * ["Silver Rupee"]
                + 10 * ["Gold Rupee"]
                + 10 * ["Semi Rare Treasure"]
                + 1 * ["Golden Skull"]
                + 12 * ["Rare Treasure"]
                + 2 * ["Evil Crystal"]
                + 2 * ["Eldin Ore"]
                + 1 * ["Goddess Plume"]
                + 1 * ["Dusk Relic"]
                + 1 * ["Tumbleweed"]
                + 1 * ["5 Bombs"]
             )
        )

    def update_progress_pool(self):
        # the standard item pool doesn't actually make any modifications, logic is responsible for
        # calculating useless items and removing them from the progress pool
        pass
