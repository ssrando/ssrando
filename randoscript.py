from collections import OrderedDict

from ssrando import Randomizer
from options import OPTIONS

confirm = True

while confirm:

    chosen_options = OrderedDict()
    print("Welcome to the Skyward Sword Randomizer\nIn the following i will ask you some questions about your Rando experience\n")
    for option in OPTIONS:
        print(option["name"] + ': ' + option["help"])
        if option["type"] == "boolean":
            print("Type y for yes and n for no")
            chosen = input()
            chosen_options[option["command"]] = (chosen.strip() == 'y')
        elif option["type"] == 'int':
            number = input()
            number = number.strip()
            if number == '':
                number = option["default"]
            chosen_options[option["command"]] = int(number)
        else:
            chosen_options[option["command"]] = input()
            
    print("Now generating a seed with the following options:")
    for option in OPTIONS:
        print(f'{option["name"]}:  {chosen_options[option["command"]]}')

    print("If these options are not correct, please type n, otherwise the seed will be generated")
    confirm_input = input()

    if not confirm_input =="n":
        confirm = False

rando = Randomizer(chosen_options)
print(rando.seed)
rando.randomize()


