from logic.constants import ALL_TYPES
from packedbits import PackedBitsReader, PackedBitsWriter

from collections import OrderedDict


OPTIONS = [
    {
        'name': 'Dry Run',
        'command': 'dry-run',
        'type': 'boolean',
        'default': False,
        'permalink': False,
        'help': 'Only generate a spoiler log, doesn\'t attempt to patch any game files',
    },
    {
        'name': 'Randomize Tablets',
        'command': 'randomize-tablets',
        'type': 'boolean',
        'default': False,
        'help': 'Randomize the 3 Stone Tablets, blocking the access to the surface',
    },
    {
        'name': 'Closed Thunderhead',
        'command': 'closed-thunderhead',
        'type': 'boolean',
        'default': False,
        'help': 'Thunderhead is closed by default, obtain Ballad of the Goddess to immediately open it',
    },
    {
        'name': 'Swordless',
        'command': 'swordless',
        'type': 'boolean',
        'default': False,
        'help': 'Instead of starting with the goddess sword, in this mode all sword upgrades, including the pracice sword, have to be found',
    },
    # {
    #     'name': 'Required Dungeons',
    #     'command': 'required-dungeons',
    #     'type': 'int',
    #     'default': 2,
    #     'min': 0,
    #     'max': 6,
    #     'bits': 3,
    #     'help': '(not implemented yet) the number of dungeons that are required, to beat the seed',
    # },
    # {
    #     'name': 'Randomize Sailcloth',
    #     'command': 'randomize-sailcloth',
    #     'type': 'boolean',
    #     'default': False,
    #     'help': '(not implemented yet) Instead of starting with the Sailcloth, it\'s added to the item pool',
    # },
    {
        'name': 'Invisible Sword',
        'command': 'invisible-sword',
        'type': 'boolean',
        'default': False,
        'help': 'Dumb hack that makes the sword always invisible so it doesn\'t crash on console if obtaining an upgraded sword',
    },
    {
        'name': 'Empty unrequired Dungeons',
        'command': 'empty-unrequired-dungeons',
        'type': 'boolean',
        'default': False,
        'help': 'If activated, only the required dungeons will contain progression items',
    },
    {
        'name': 'Banned Types',
        'command': 'banned-types',
        'type': 'multichoice',
        'default': [],
        'choices': ALL_TYPES,
        'help': "Choose subtypes that can't contain progression items, as a comma seperated list, available types are: " + ", ".join(ALL_TYPES),
    },
    {
        'name': 'Seed',
        'command': 'seed',
        'type': 'int',
        'default': -1,
        'permalink': False, # seed is seperate
        'help': 'Specify a seed to use for randomization, leave empty for random seed',
    },
]

class Options():
    def __init__(self):
        self.options = OrderedDict()
        self.reset_to_default()

    def reset_to_default(self):
        self.options.clear()
        for option in OPTIONS:
            self.options[option['command']]=option['default']
    
    @staticmethod
    def parse_and_validate_option(value: str, option: dict):
        validation_errors = []
        if option['type'] == 'boolean':
            value = value.lower() == 'true'
        elif option['type'] == 'int':
            try:
                value = int(value)
            except ValueError:
                validation_errors.append(f'{value} is not a number, which is required for {option["command"]}')
            if 'max' in option and value > option['max']:
                validation_errors.append(f'{value} is greater than the maximum of {option["max"]} for {option["command"]}')
            if 'min' in option and value < option['min']:
                validation_errors.append(f'{value} is smaller than the minimum of {option["min"]} for {option["command"]}')
        elif option['type'] == 'multichoice':
            value = [v.strip() for v in value.split(',')]
            unknown_values = [v for v in value if not v in option['choices']]
            if len(unknown_values) > 0:
                validation_errors.append(f'Unknown choice(s) for {option["command"]}: {unknown_values}')
        elif option['type'] == 'singlechoice':
            if not value in option['choices']:
                validation_errors.append(f'value {value} is not valid for {option["command"]}')
        else:
            raise Exception(f'unknown type: {option["type"]}')
        return value, validation_errors

    def update_from_cmd_args(self, raw_options):
        problems = []
        for option in OPTIONS:
            if option['command'] in raw_options:
                value = raw_options.pop(option['command'])
                value, validation_errors = Options.parse_and_validate_option(value, option)
                if len(validation_errors) > 0:
                    problems.extend(validation_errors)
                    continue
                self.options[option['command']] = value
        for option_name in raw_options.keys():
            problems.append(f'unknown option {option_name}!')
        return problems
    
    def get_permalink(self):
        writer = PackedBitsWriter()
        for option in OPTIONS:
            if not option.get('permalink',True):
                continue
            value = self.options.get(option['command'],option['default'])
            if option['type'] == 'boolean':
                # one bit
                writer.write(int(value), 1)
            elif option['type'] == 'int':
                # needs information, how many bits this number is
                writer.write(value, option['bits'])
            elif option['type'] == 'multichoice':
                # as many bits as choices
                for choice in option['choices']:
                    writer.write(int(choice in value), 1)
            elif option['type'] == 'singlechoice':
                # needs information, how many bits this number is, then it's just the index to the choices
                writer.write(option['choices'].index(value), option['bits'])
            else:
                raise Exception(f'unknown type: {option["type"]}')
        writer.flush()
        return writer.to_base64()
    
    def set_option(self, option_name, option_value):
        """
        Sets the option to a value, this function checks if the value is valid, and throws an exception if it isn't
        """
        option_dict = dict((op['command'], op) for op in OPTIONS)
        if not option_name in option_dict:
            raise ValueError(f'not a valid option: {option_name}!')
        option = option_dict[option_name]
        if option['type'] == 'boolean':
            if not isinstance(option_value, bool):
                raise TypeError(f'value for option {option_name} has to be a boolean, got {type(option_value)}!')
        elif option['type'] == 'int':
            if not isinstance(option_value, int):
                raise TypeError(f'value for option {option_name} has to be a number, got {type(option_value)}!')
        elif option['type'] == 'multichoice':
            if not isinstance(option_value, list):
                raise TypeError(f'value for option {option_name} has to be a list, got {type(option_value)}!')
            unknown_values = [v for v in option_value if not v in option['choices']]
            if unknown_values:
                raise ValueError(f'Unknown choice(s) for {option_name}: {unknown_values}')
        elif option['type'] == 'singlechoice':
            if not option_value in option['choices']:
                raise ValueError(f'Unknown choice for {option_name}: {unknown_values}')
        self.options[option_name] = option_value

    def validate_options(self):
        for option_name in self.options:
            self.set_option(option_name, self[option_name])

    def update_from_permalink(self, permalink):
        reader = PackedBitsReader.from_base64(permalink)
        for option in OPTIONS:
            if not option.get('permalink',True):
                continue
            if option['type'] == 'boolean':
                value = bool(reader.read(1))
            elif option['type'] == 'int':
                value = reader.read(option['bits'])
            elif option['type'] == 'multichoice':
                # as many bits as choices
                value = []
                for choice in option['choices']:
                    if reader.read(1):
                        value.append(choice)
            elif option['type'] == 'singlechoice':
                value = option['choices'][reader.read(option['bits'])]
            else:
                raise Exception(f'unknown type: {option["type"]}')
            self.options[option['command']] = value
    
    def __getitem__(self, item):
        return self.options[item]
    
    def get(self, item, default=None):
        return self.options.get(item, default)
