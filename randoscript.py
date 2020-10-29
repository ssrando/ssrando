from collections import OrderedDict
import sys

from ssrando import Randomizer
from options import OPTIONS

def process_command_line_options(options):
    if 'help' in options:
        print('Skyward Sword Randomizer')
        print('Available command line options:\n')
        longest_option = max(len(option['command']) for option in OPTIONS)
        for option in OPTIONS:
            print(' --'+option["command"].ljust(longest_option) + ' ' + option['help'])
        return None
    else:
        cleaned_options = {}
        for option in OPTIONS:
            if option['command'] in options:
                value = options.pop(option['command'])
                if option['type'] == 'boolean':
                    value = value.lower() == 'true'
                elif option['type'] == 'int':
                    value = int(value)
                cleaned_options[option['command']] = value
            else:
                cleaned_options[option['command']] = option['default']
        for option_name in options.keys():
            print(f'unknown option {option_name}!')
        return cleaned_options

# check if interactive script should be run, or if there were command line parameters
if len(sys.argv) > 1:
    # use command line parameters
    cmd_line_args = OrderedDict()
    for arg in sys.argv[1:]:
        arg_parts = arg.split("=", 1)
        option_name = arg_parts[0]
        assert option_name.startswith('--')
        if len(arg_parts) == 1:
            cmd_line_args[option_name[2:]] = 'true'
        else:
            cmd_line_args[option_name[2:]] = arg_parts[1]
    options = process_command_line_options(cmd_line_args)
    if options is not None:
        rando = Randomizer(options)
        rando.randomize()
        print(rando.seed)
else:
    # interactive script
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

