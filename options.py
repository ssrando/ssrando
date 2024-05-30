from packedbits import PackedBitsReader, PackedBitsWriter
from pathlib import Path
from yaml_files import checks, options, random_settings_weighting

from collections import OrderedDict
import logic.constants as constants

import random

OPTIONS = OrderedDict((option["command"], option) for option in options)
OPTIONS["excluded-locations"]["choices"] = [check for check in checks]


class Options:
    def __init__(self):
        self.options = OrderedDict()
        self.reset_to_default()

    def reset_to_default(self):
        self.options.clear()
        for option_name, option in OPTIONS.items():
            if option["type"] == "dirpath":
                self.options[option_name] = Path(option["default"]).resolve()
            else:
                self.options[option_name] = option["default"]

    def reset_randomized_settings(self):
        for option_name, option in OPTIONS.items():
            if option["command"] in constants.NON_RANDOMIZED_SETTINGS or (
                "permalink" in option and not option["permalink"]
            ):
                continue
            self.options[option_name] = option["default"]

    @staticmethod
    def parse_and_validate_option(value_str: str, option: dict):
        validation_errors = []
        if option["type"] == "boolean":
            value = value_str.lower() == "true"
        elif option["type"] == "int":
            try:
                value = int(value_str)
            except ValueError:
                validation_errors.append(
                    f'{value_str} is not a number, which is required for {option["command"]}'
                )
                return value_str, validation_errors
            if "max" in option and value > option["max"]:
                validation_errors.append(
                    f'{value} is greater than the maximum of {option["max"]} for {option["command"]}'
                )
            if "min" in option and value < option["min"]:
                validation_errors.append(
                    f'{value} is smaller than the minimum of {option["min"]} for {option["command"]}'
                )
        elif option["type"] == "multichoice":
            value = [v.strip() for v in value_str.split(",")]
            # skip out empty string
            value = [v for v in value if v]
            unknown_values = [v for v in value if not v in option["choices"]]
            if len(unknown_values) > 0:
                validation_errors.append(
                    f'Unknown choice(s) for {option["command"]}: {unknown_values}'
                )
        elif option["type"] == "singlechoice":
            if isinstance(option["default"], int):
                try:
                    value = int(value_str)
                except ValueError:
                    validation_errors.append(
                        f'{value_str} is not a number, which is required for {option["command"]}'
                    )
                    return value_str, validation_errors
            else:
                value = value_str
            if not value in option["choices"]:
                validation_errors.append(
                    f'value {value} is not valid for {option["command"]}'
                )
        elif option["type"] == "dirpath":
            path = Path(value_str).expanduser()
            if not path.is_dir():
                validation_errors.append(f"path {value_str} is not a directory!")
            value = path
        elif option["type"] == "string":
            pass
        else:
            raise Exception(f'Unknown type: {option["type"]}.')
        return value, validation_errors

    def update_from_cmd_args(self, raw_options):
        problems = []
        for option_name, option in OPTIONS.items():
            if option_name in raw_options:
                value = raw_options.pop(option_name)
                value, validation_errors = Options.parse_and_validate_option(
                    value, option
                )
                if len(validation_errors) > 0:
                    problems.extend(validation_errors)
                    continue
                self.options[option_name] = value
        for option_name in raw_options.keys():
            problems.append(f"unknown option {option_name}!")
        return problems

    def get_permalink(self, exclude_seed=False):
        writer = PackedBitsWriter()
        for option_name, option in OPTIONS.items():
            if not option.get("permalink", True):
                continue
            value = self.options.get(option_name, option["default"])
            if option["type"] == "boolean":
                # one bit
                writer.write(int(value), 1)
            elif option["type"] == "int":
                # needs information, how many bits this number is
                writer.write(value, option["bits"])
            elif option_name == "starting-items":
                starting_items = option["choices"].copy()
                while len(starting_items) > 0:
                    starting_item_count = value.count(starting_items[0])
                    if starting_item_count == 0:
                        writer.write(0, 1)
                        starting_items.remove(starting_items[0])
                    else:
                        for progressive_count in range(
                            starting_items.count(starting_items[0])
                        ):
                            writer.write(progressive_count < starting_item_count, 1)
                            starting_items.pop(0)
            elif option["type"] == "multichoice":
                # as many bits as choices
                for choice in option["choices"]:
                    writer.write(int(choice in value), 1)
            elif option["type"] == "singlechoice":
                # needs information, how many bits this number is, then it's just the index to the choices
                writer.write(option["choices"].index(value), option["bits"])
            else:
                raise Exception(f'Unknown type: {option["type"]}.')
        writer.flush()
        permalink = writer.to_base64()
        if self["seed"] != -1 and not exclude_seed:
            permalink += "#" + str(self["seed"])
        return permalink

    def set_option(self, option_name, option_value):
        """
        Sets the option to a value, this function checks if the value is valid, and throws an exception if it isn't
        """
        if not option_name in OPTIONS:
            raise ValueError(f"Not a valid option: {option_name}.")
        option = OPTIONS[option_name]
        if option["type"] == "boolean":
            if not isinstance(option_value, bool):
                raise TypeError(
                    f"Value for option {option_name} has to be a boolean, got {type(option_value)}."
                )
        elif option["type"] == "int":
            if not isinstance(option_value, int):
                raise TypeError(
                    f"Value for option {option_name} has to be a number, got {type(option_value)}."
                )
            if "max" in option and option_value > option["max"]:
                raise ValueError(
                    f'{option_value} is greater than the maximum of {option["max"]} for {option["command"]}.'
                )
            if "min" in option and option_value < option["min"]:
                raise ValueError(
                    f'{option_value} is smaller than the minimum of {option["min"]} for {option["command"]}.'
                )
        elif option["type"] == "multichoice":
            if not isinstance(option_value, list):
                raise TypeError(
                    f"Value for option {option_name} has to be a list, got {type(option_value)}."
                )
            unknown_values = [v for v in option_value if not v in option["choices"]]
            if unknown_values:
                raise ValueError(
                    f"Unknown choice(s) for {option_name}: {unknown_values}."
                )
        elif option["type"] == "singlechoice":
            if isinstance(option["default"], int) and not isinstance(option_value, int):
                option_value = int(option_value)
            if not option_value in option["choices"]:
                raise ValueError(f"Unknown choice for {option_name}: {option_value}.")
        elif option["type"] == "dirpath":
            path = Path(option_value).expanduser()
            if not path.is_dir():
                raise ValueError(f"Path {option_value} is not a directory.")
            option_value = path
        elif option["type"] == "string":
            if not isinstance(option_value, str):
                raise TypeError(
                    f"Value for option {option_name} has to be a string, got {type(option_value)}."
                )
        self.options[option_name] = option_value

    def set_option_str(self, option_name, option_value):
        if not option_name in OPTIONS:
            raise ValueError(f"Not a valid option: {option_name}.")
        value, vaidation_errors = Options.parse_and_validate_option(
            option_value, OPTIONS[option_name]
        )
        if vaidation_errors:
            raise ValueError(f"Validation errors: {vaidation_errors}.")
        self.options[option_name] = value

    def validate_options(self):
        for option_name in self.options:
            self.set_option(option_name, self[option_name])

    def update_from_permalink(self, permalink: str):
        if "#" in permalink:
            # includes the seed as well
            permalink, seed_str = permalink.split("#", 1)
            self.set_option("seed", int(seed_str))
        reader = PackedBitsReader.from_base64(permalink)
        for option_name, option in OPTIONS.items():
            if not option.get("permalink", True):
                continue
            if option["type"] == "boolean":
                value = bool(reader.read(1))
            elif option["type"] == "int":
                value = reader.read(option["bits"])
            elif option["type"] == "multichoice":
                # as many bits as choices
                value = []
                for choice in option["choices"]:
                    if reader.read(1):
                        value.append(choice)
            elif option["type"] == "singlechoice":
                value = option["choices"][reader.read(option["bits"])]
            else:
                raise Exception(f'Unknown type: {option["type"]}.')
            self.set_option(option_name, value)

    def randomize_settings(self, rando):
        rs_weighting = random_settings_weighting(self["random-settings-weighting"])

        for optkey, opt in OPTIONS.items():
            if opt["command"] in constants.NON_RANDOMIZED_SETTINGS or (
                "permalink" in opt and opt["permalink"] == False
            ):
                continue
            else:
                if opt["type"] == "boolean":
                    if opt["command"] == "shopsanity":
                        self.set_option(
                            optkey, True
                        )  # Manually setting shopsanity to true bc it breaks everything rn and I'll fix it soon
                    elif (
                        len([o for o in rs_weighting if o["name"] == opt["name"]]) == 1
                    ):
                        rsopt = [
                            o for o in rs_weighting if o["name"] == opt["name"]
                        ].pop()
                        self.set_option(
                            optkey,
                            rando.rng.choices(
                                [True, False],
                                k=1,
                                weights=[rsopt["checked"], rsopt["unchecked"]],
                            ).pop(),
                        )
                    else:
                        print(
                            f"Did not find option '"
                            + opt["name"]
                            + "' in the selected RS weighting. Defaulting to random selection."
                        )
                        self.set_option(optkey, bool(rando.rng.randint(0, 1)))
                elif opt["type"] == "int":
                    if opt["command"] == "starting-heart-pieces":
                        selec = rando.rng.choices(
                            list(rsopt["choices"].keys()),
                            k=1,
                            weights=rsopt["choices"].values(),
                        ).pop()
                        if selec == 24:
                            self.set_option(optkey, 24)
                        else:
                            self.set_option(optkey, rando.rng.randint(selec, selec + 3))
                    elif (
                        len([o for o in rs_weighting if o["name"] == opt["name"]]) == 1
                    ):
                        rsopt = [
                            o for o in rs_weighting if o["name"] == opt["name"]
                        ].pop()
                        self.set_option(
                            optkey,
                            rando.rng.choices(
                                list(rsopt["choices"].keys()),
                                k=1,
                                weights=rsopt["choices"].values(),
                            ).pop(),
                        )
                    else:
                        print(
                            f"Did not find option '"
                            + opt["name"]
                            + "' in the selected RS weighting. Defaulting to random selection."
                        )
                        self.set_option(
                            optkey, rando.rng.randint(opt["min"], opt["max"])
                        )
                elif opt["type"] == "singlechoice":
                    if len([o for o in rs_weighting if o["name"] == opt["name"]]) == 1:
                        rsopt = [
                            o for o in rs_weighting if o["name"] == opt["name"]
                        ].pop()
                        self.set_option(
                            optkey,
                            rando.rng.choices(
                                list(rsopt["choices"].keys()),
                                k=1,
                                weights=rsopt["choices"].values(),
                            ).pop(),
                        )
                    else:
                        print(
                            f"Did not find option '"
                            + opt["name"]
                            + "' in the selected RS weighting. Defaulting to random selection."
                        )
                        self.set_option(optkey, rando.rng.choice(opt["choices"]))
                elif opt["type"] == "multichoice":
                    if len([o for o in rs_weighting if o["name"] == opt["name"]]) == 1:
                        rsopt = [
                            o for o in rs_weighting if o["name"] == opt["name"]
                        ].pop()
                        choices = rsopt["choices"]
                        rando.rng.shuffle(choices)
                        multichoice = []
                        i = 0
                        if rsopt["maxpicks"] == "None":
                            maxpicks = len(choices)
                        else:
                            maxpicks = rsopt["maxpicks"]
                        for c, weight in choices:
                            if i >= maxpicks:
                                break
                            if (
                                rando.rng.choices(
                                    [True, False],
                                    k=1,
                                    weights=[weight, 100 - weight],
                                ).pop()
                                == True
                            ):
                                multichoice.append(c)
                                i += 1
                        self.set_option(optkey, multichoice)
                    else:
                        print(
                            f"Did not find option '"
                            + opt["name"]
                            + "' in the selected RS weighting. Defaulting to random selection."
                        )
                        self.set_option(
                            optkey,
                            rando.rng.sample(
                                opt["choices"],
                                rando.rng.randint(0, len(opt["choices"])),
                            ),
                        )

    def randomize_progression_locations(self, rando):
        rs_weighting = random_settings_weighting(self["random-settings-weighting"])
        locs_weighting = [o for o in rs_weighting if o["type"] == "locations"].pop()
        non_prog_locs = []

        for loc in self["rs-random-progression-locs"]:
            if locs_weighting["locations"][loc]:
                weight = locs_weighting["locations"][loc]
                if not rando.rng.choices(
                    [True, False], k=1, weights=[weight, 100 - weight]
                ).pop():
                    non_prog_locs.append(loc)
            else:
                print(
                    f"Did not find location '{loc}' in the selected RS weighting. Defaulting to random selection."
                )
                if bool(rando.rng.randint(0, 1)):
                    non_prog_locs.append(loc)
        for loc in self["rs-random-progression-locs"]:
            if loc in non_prog_locs:
                continue
            if not self.check_loc_conditions(loc=loc, non_prog_locs=non_prog_locs):
                non_prog_locs.append(loc)
        for check in OPTIONS["excluded-locations"]["choices"]:
            if check in self["excluded-locations"]:
                continue  # Keep it excluded
            elif checks[check]["type"] is None:
                continue  # Base check
            elif any(i in checks[check]["type"] for i in non_prog_locs):
                self.set_option(
                    "excluded-locations", [*self["excluded-locations"], check]
                )
            else:
                continue

    def check_loc_conditions(self, loc, non_prog_locs):
        if loc.startswith("Batreaux's Rewards"):
            conditions = (
                "Batreaux's Rewards (30 & below)",
                "Batreaux's Rewards (40 & 50)",
                "Batreaux's Rewards (70s & 80)",
            )
        elif loc.startswith("Beedle's Airshop"):
            conditions = (
                "Beedle's Airshop (Cheap)",
                "Beedle's Airshop (Medium)",
                "Beedle's Airshop (Expensive)",
            )
        else:
            return True  # unconditional option
        for c in conditions:
            if loc == c:
                conditions_met = True
                break
            elif c in non_prog_locs:
                conditions_met = False
                break
            else:
                continue
        return conditions_met

    def randomize_cosmetics(self, rando):
        for optkey, opt in OPTIONS.items():
            if (
                opt["command"] not in constants.NON_RANDOMIZED_COSMETICS
                and "cosmetic" in opt
                and opt["cosmetic"] == True
            ):
                if opt["type"] == "boolean":
                    self.set_option(optkey, bool(random.randint(0, 1)))
                elif opt["type"] == "int":
                    if opt["command"] == "star-count":
                        self.set_option(
                            optkey, random.randint(0, 700)
                        )  # Anything over 700 will lag the game
                    else:
                        self.set_option(optkey, random.randint(opt["min"], opt["max"]))
                elif opt["type"] == "singlechoice":
                    self.set_option(optkey, random.choice(opt["choices"]))
                elif opt["type"] == "multichoice":
                    self.set_option(
                        optkey,
                        random.sample(
                            opt["choices"], random.randint(0, len(opt["choices"]))
                        ),
                    )

    def to_dict(self, exclude_nonperma=False, exclude=[]):
        opts = self.options.copy()
        for option_name, option in OPTIONS.items():
            if exclude_nonperma and not option.get("permalink", True):
                del opts[option_name]
                continue
            if option_name in exclude:
                del opts[option_name]
                continue
            if option["type"] == "dirpath":
                opts[option_name] = str(opts[option_name])
        return opts

    def update_from_dict(self, opts):
        def try_set_option(name, value):
            try:
                self.set_option(name, value)
                return True
            except ValueError as e:
                print(f"error restoring option {name}:", e)
                return False

        opts_reset_to_default = []
        for option_name, option in OPTIONS.items():
            if not (
                option_name in opts and try_set_option(option_name, opts[option_name])
            ):
                # reset permalink-relevant options that the preset doesn't include to default
                if option.get("permalink", True):
                    opts_reset_to_default.append(option_name)
                    self.set_option(option_name, option["default"])
        if opts_reset_to_default:
            print(f"options {opts_reset_to_default} were reset to default")

    def __getitem__(self, item):
        return self.options[item]

    def get(self, item, default=None):
        return self.options.get(item, default)

    def copy(self):
        o = Options()
        o.options = self.options.copy()
        return o
