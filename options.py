from packedbits import PackedBitsReader, PackedBitsWriter
from pathlib import Path
from yaml_files import checks, options

from collections import OrderedDict

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
        for option_name, option in OPTIONS.items():
            if option_name in opts:
                try:
                    self.set_option(option_name, opts[option_name])
                except ValueError as e:
                    print(f"error restoring option {option_name}:", e)

    def __getitem__(self, item):
        return self.options[item]

    def get(self, item, default=None):
        return self.options.get(item, default)

    def copy(self):
        o = Options()
        o.options = self.options.copy()
        return o
