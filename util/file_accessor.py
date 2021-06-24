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


class YamlOrderedDictLoader(yaml.SafeLoader):
    pass


YamlOrderedDictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: OrderedDict(loader.construct_pairs(node)),
)
