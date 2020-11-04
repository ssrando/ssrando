from collections import OrderedDict
import sys

from ssrando import Randomizer, VERSION
from options import OPTIONS, Options

def process_command_line_options(options):
    if 'help' in options:
        print('Skyward Sword Randomizer Version '+VERSION)
        print('Available command line options:\n')
        longest_option = max(len(option['command']) for option in OPTIONS)
        for option in OPTIONS:
            print(' --'+option["command"].ljust(longest_option) + ' ' + option['help'])
        return None
    elif 'version' in options:
        print(VERSION)
        return None
    else:
        cleaned_options = Options()
        problems = cleaned_options.update_from_cmd_args(options)
        if problems:
            print('ERROR: invalid options:')
            for problem in problems:
                print(problem)
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
        total_progress_steps = rando.get_total_progress_steps()
        progress_steps=0
        def progress_callback(action):
            global progress_steps
            print(f'{action} {progress_steps}/{total_progress_steps}')
            progress_steps+=1
        rando.progress_callback = progress_callback
        rando.randomize()
        print(rando.seed)
else:
    # interactive script
    confirm = True

    while confirm:
        options = Options()
        print("Welcome to the Skyward Sword Randomizer Version " + VERSION)
        print("In the following i will ask you some questions about your Rando experience\n")
        for option_name, option in OPTIONS.items():
            print(option["name"] + ': ' + option["help"])
            if option["type"] == "boolean":
                print("Type y for yes and n for no")
                chosen = input()
                options.set_option(option_name, (chosen.strip() == 'y'))
            elif option["type"] == 'int':
                number = input()
                number = number.strip()
                if number == '':
                    number = option["default"]
                options.set_option(option_name, int(number))
            elif option["type"] == 'multichoice':
                value = input()
                value = [v.strip() for v in value.split(',')]
                value = [v for v in value if v]
                options.set_option(option_name, value)
            else:
                options.set_option(option_name, input())
                
        print("Now generating a seed with the following options:")
        for option_name, option in OPTIONS.items():
            print(f'{option["name"]}:  {options[option_name]}')

        print("If these options are not correct, please type n, otherwise the seed will be generated")
        confirm_input = input()

        if not confirm_input =="n":
            confirm = False

    rando = Randomizer(options)
    print(rando.seed)
    rando.randomize()

