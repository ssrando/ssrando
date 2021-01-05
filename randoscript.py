from collections import OrderedDict
import sys

from ssrando import Randomizer, VERSION
from options import OPTIONS, Options

def process_command_line_options(options):
    if 'help' in options:
        print('Skyward Sword Randomizer Version '+VERSION)
        print('Available command line options:\n')
        longest_option = max(len(option_name) for option_name in OPTIONS.keys())
        for option_name, option in OPTIONS.items():
            print(' --'+option_name.ljust(longest_option) + ' ' + option['help'])
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

if 'NOGIT' in VERSION:
    print('WARNING: Running from source, but without git, this is highly discouraged')

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
    if options['noui']:
        rando = Randomizer(options)
        if not options['dry-run']:
            rando.check_valid_directory_setup()
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
        from gui.randogui import run_main_gui

        run_main_gui(options)

