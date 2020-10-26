from collections import OrderedDict

from ssrando import Randomizer

confirm = True

while confirm:

    print("Welcome to the Skyward Sword Randomizer\nIn the following i will ask you some questions about your Rando experience\n")
    print("Is this a dry run? (Spoiler log only)\nType y for yes and n for no")
    dry_run = input()
    print("Will you play on Console? (Enables invisible sword patch)\nType y for yes and n for no")
    invis_sword = input()
    print("Do you want to randomize tablets?\nType y for yes and n for no")
    rand_tablets = input()
    print("Do you want to start without a sword?\nType y for yes and n for no")
    swordless = input()
    print("Do you want to start with closed Thunderhead?\nType y for yes and n for no")
    closed_thunderhead = input()
    print("Do you want to use a specifc seed?\nPlease type the correct seed, -1 for no seed")
    seed = input()

    options = OrderedDict()
    # If in doubt do not make a dry run
    if dry_run == "y":
        options["dry-run"] = True
    else:
        options["dry-run"] = False


    # If in doubt, invisble sword
    if invis_sword == "n":
        options["invisible-sword"] = False
    else:
        options["invisible-sword"] = True

    if rand_tablets == "y":
        options["randomize-tablets"] = True
    else:
        options["randomize-tablets"] = False

    if swordless == "y":
        options["swordless"] = True
    else:
        options["swordless"] = False

    if closed_thunderhead == "y":
        options["closed-thunderhead"] = True
    else:
        options["closed-thunderhead"] = False

    seed = seed.strip() or '-1'
    seed = int(seed)
    options["seed"] = seed

    print("Now generating a seed with the following options:\n"
          "Dry Run: ", options["dry-run"],
          "\nInvisible Sword: ", options["invisible-sword"],
          "\nRandomized Tablets: ", options["randomize-tablets"],
          "\nSwordless: ", options["swordless"],
          "\nClosed Thunderhead: ", options["closed-thunderhead"],
          "\nSeed: ", options["seed"])

    print("If these options are not correct, please type n, otherwise the seed will be generated")
    confirm_input = input()

    if not confirm_input =="n":
        confirm = False

rando = Randomizer(options)
print(rando.seed)
rando.randomize()


