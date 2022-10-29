from collections import OrderedDict
import sys
import argparse
from logic.logic_input import Areas
from yaml_files import requirements, checks, hints, map_exits

from ssrando import Randomizer, PlandoRandomizer, VERSION
from logic.placement_file import PlacementFile
from options import OPTIONS, Options


def get_ranges(start, end, parts):
    step = (end + 1 - start) / parts
    for i in range(parts):
        yield (int(start + step * i), int(start + step * (i + 1)))


def main():
    if "NOGIT" in VERSION:
        print(
            "WARNING: Running from source, but without git, this is highly discouraged"
        )

    # add options
    parser = argparse.ArgumentParser(
        description="Skyward Sword Randomizer Version " + VERSION
    )
    parser.add_argument(
        "--permalink",
        help="Specify a permalink, which includes the settings. This is set first, other options may override these settings",
    )
    parser.add_argument(
        "--placement-file",
        help="Specify the location of a placement file json that is used directly as a plandomizer, overrides all other options",
    )
    parser.add_argument(
        "--version",
        help="Prints the version and exits",
        action="store_true",
    )
    seed_opts = parser.add_argument_group("seed options")

    for optname, opt in OPTIONS.items():
        args = {
            "help": f'(default: {opt["default"]}) {opt["help"]}',
        }
        if opt["type"] == "boolean":
            args["const"] = "true"
            args["nargs"] = "?"
            args["metavar"] = "BOOL"
        elif opt["type"] == "int":
            args["type"] = int
            if "min" in opt and "max" in opt:
                args[
                    "help"
                ] = f'(default: {opt["default"]}, min: {opt["min"]}, max: {opt["max"]}) {opt["help"]}'
        elif opt["type"] == "singlechoice":
            args["choices"] = opt["choices"]
            if isinstance(opt["default"], int):
                args["type"] = int
        seed_opts.add_argument(f"--{optname}", **args)

    bulk_opts = parser.add_argument_group("bulk options")
    bulk_opts.add_argument(
        "--bulk",
        help="Runs the randomizer in bulk mode, to generate lots of spoiler logs. Implies --dry-run",
        action="store_true",
    )
    bulk_opts.add_argument(
        "--low",
        help="specify the lower end of seeds to generate (inclusive)",
        default=1,
        type=int,
        dest="bulk_low",
    )
    bulk_opts.add_argument(
        "--high",
        help="specify the higher end of seeds to generate (inclusive)",
        default=100,
        type=int,
        dest="bulk_high",
    )
    bulk_opts.add_argument(
        "--threads",
        help="specify the number of threads to use",
        default=1,
        type=int,
        dest="bulk_threads",
    )

    parsed_args = parser.parse_args()
    if parsed_args.version:
        print(VERSION)
        exit(0)
    options = Options()
    if parsed_args.permalink is not None:
        options.update_from_permalink(parsed_args.permalink)
    all_errors = []
    for optname, opt in OPTIONS.items():
        optval = parsed_args.__getattribute__(optname.replace("-", "_"))
        if optval is not None:
            value, validation_errors = Options.parse_and_validate_option(optval, opt)
            if validation_errors:
                all_errors.extend(validation_errors)
            else:
                options.set_option(optname, value)

    if all_errors:
        print("Options ERROR:")
        for err in all_errors:
            print(err)
        exit(1)

    areas = Areas(requirements, checks, hints, map_exits)

    plcmt_file_name = parsed_args.placement_file
    if plcmt_file_name is not None:
        plcmt_file = PlacementFile()
        with open(plcmt_file_name) as f:
            plcmt_file.read_from_file(f)
        plcmt_file.check_valid(areas)

        plandomizer = PlandoRandomizer(plcmt_file, areas)
        total_progress_steps = plandomizer.get_total_progress_steps
        progress_steps = 0

        def progress_callback(action):
            nonlocal progress_steps
            print(f"{action} {progress_steps}/{total_progress_steps}")
            progress_steps += 1

        plandomizer.progress_callback = progress_callback
        plandomizer.randomize()
        exit(0)

    assert options is not None

    if parsed_args.bulk:
        bulk_low = parsed_args.bulk_low
        bulk_high = parsed_args.bulk_high
        if bulk_high < bulk_low:
            print("high has to be higher than low!")
            exit(1)
        bulk_threads = parsed_args.bulk_threads

        options.set_option("dry-run", True)

        def randothread(start, end, local_opts):
            for i in range(start, end):
                try:
                    local_opts.set_option("seed", i)
                    rando = Randomizer(areas, local_opts)
                    rando.randomize()
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    import traceback

                    stack_trace = traceback.format_exc()
                    error_message = (
                        f"error seed {i}:\n\n" + str(e) + "\n\n" + stack_trace
                    )
                    print(error_message, file=sys.stderr)

        if bulk_threads == 1:
            randothread(bulk_low, bulk_high, options)
        else:
            from multiprocessing import Process

            threads = []
            for start, end in get_ranges(bulk_low, bulk_high, bulk_threads):
                thread = Process(target=randothread, args=(start, end, options.copy()))
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
    elif options["noui"]:
        rando = Randomizer(areas, options)
        if not options["dry-run"]:
            rando.check_valid_directory_setup()
        total_progress_steps = 0
        progress_steps = 0

        def update_progress_dialog(hash, total_steps):
            nonlocal total_progress_steps
            total_progress_steps = total_steps

        def progress_callback(action):
            nonlocal progress_steps
            print(f"{action} {progress_steps}/{total_progress_steps}")
            progress_steps += 1

        rando.progress_callback = progress_callback
        rando.randomize(update_progress_dialog)
        print(f"SEED HASH: {rando.randomizer_hash}")
    else:
        from gui.randogui import run_main_gui

        run_main_gui(areas, options)


if __name__ == "__main__":
    main()
