from paths import RANDO_ROOT_PATH
import yaml

CACHE = {}


def read_yaml_file_cached(filename: str):
    if filename in CACHE:
        return CACHE[filename]
    else:
        with (RANDO_ROOT_PATH / filename).open() as f:
            yaml_file = yaml.safe_load(f)
        CACHE[filename] = yaml_file
        return yaml_file
