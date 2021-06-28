from collections import OrderedDict
import sys

from ssrando import Randomizer, PlandoRandomizer, VERSION
from logic.placement_file import PlacementFile
from options import OPTIONS, Options


def process_command_line_options(options):
    if "help" in options:
        print("Skyward Sword Randomizer Version " + VERSION)
        print("Available command line options:\n")
        longest_option = max(len(option_name) for option_name in OPTIONS.keys())
        for option_name, option in OPTIONS.items():
            print(" --" + option_name.ljust(longest_option) + " " + option["help"])
        # permalink
        print()
        print(
            " --"
            + "permalink".ljust(longest_option)
            + " "
            + "Specify a permlink, which includes the settings. This is set first, other options may override these settings"
        )
        # bulk options
        print()
        print(
            " --"
            + "bulk".ljust(longest_option)
            + " "
            + "Runs the randomizer in bulk mode, to generate lots of spoiler logs. Implies --dry-run"
        )
        print(
            " --"
            + "low".ljust(longest_option)
            + " "
            + "(bulk mode only) specify the lower end of seeds to generate (inclusive, default: 1)"
        )
        print(
            " --"
            + "high".ljust(longest_option)
            + " "
            + "(bulk mode only) specify the higher end of seeds to generate (inclusive, default: 100)"
        )
        print(
            " --"
            + "threads".ljust(longest_option)
            + " "
            + "(bulk mode only) specify the number of threads to use (default: 1)"
        )
        print()
        print(
            " --"
            + "placement-file".ljust(longest_option)
            + " "
            + "specify the location of a placement file json that is used directly as a plandomizer, overrides all other options"
        )
        return None
    elif "version" in options:
        print(VERSION)
        return None
    else:
        cleaned_options = Options()
        if "permalink" in options:
            cleaned_options.update_from_permalink(options.pop("permalink"))
        problems = cleaned_options.update_from_cmd_args(options)
        if problems:
            print("ERROR: invalid options:")
            for problem in problems:
                print(problem)
        return cleaned_options


def get_ranges(start, end, parts):
    step = (end + 1 - start) / parts
    for i in range(parts):
        yield (int(start + step * i), int(start + step * (i + 1)))


if "NOGIT" in VERSION:
    print("WARNING: Running from source, but without git, this is highly discouraged")

# use command line parameters
cmd_line_args = OrderedDict()
for arg in sys.argv[1:]:
    arg_parts = arg.split("=", 1)
    option_name = arg_parts[0]
    assert option_name.startswith("--")
    if len(arg_parts) == 1:
        cmd_line_args[option_name[2:]] = "true"
    else:
        cmd_line_args[option_name[2:]] = arg_parts[1]
plcmt_file_name = cmd_line_args.pop("placement-file", None)
if plcmt_file_name is not None:
    plcmt_file = PlacementFile()
    with open(plcmt_file_name) as f:
        plcmt_file.read_from_file(f)
    plcmt_file.check_valid()

    plandomizer = PlandoRandomizer(plcmt_file)
    total_progress_steps = plandomizer.get_total_progress_steps()
    progress_steps = 0

    def progress_callback(action):
        global progress_steps
        print(f"{action} {progress_steps}/{total_progress_steps}")
        progress_steps += 1

    plandomizer.progress_callback = progress_callback
    plandomizer.randomize()
    exit(0)

bulk_mode = False
if cmd_line_args.pop("bulk", False):
    bulk_mode = True
    bulk_low = int(cmd_line_args.pop("low", "1"))
    bulk_high = int(cmd_line_args.pop("high", "100"))
    if bulk_high < bulk_low:
        print("high has to be higher than low!")
        exit(1)
    bulk_threads = int(cmd_line_args.pop("threads", "1"))
options = process_command_line_options(cmd_line_args)
if options is not None:
    if bulk_mode:
        from multiprocessing import Process

        options.set_option("dry-run", True)

        def randothread(start, end, local_opts):
            for i in range(start, end):
                local_opts.set_option("seed", i)
                rando = Randomizer(local_opts)
                rando.randomize()

        threads = []
        for (start, end) in get_ranges(bulk_low, bulk_high, bulk_threads):
            thread = Process(target=randothread, args=(start, end, options.copy()))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    elif options["noui"]:
        rando = Randomizer(options)
        if not options["dry-run"]:
            rando.check_valid_directory_setup()
        total_progress_steps = rando.get_total_progress_steps()
        progress_steps = 0

        def progress_callback(action):
            global progress_steps
            print(f"{action} {progress_steps}/{total_progress_steps}")
            progress_steps += 1

        rando.progress_callback = progress_callback
        rando.randomize()
        print(f"SEED HASH: {rando.randomizer_hash}")
    else:
        from gui.randogui import run_main_gui

        run_main_gui(options)
