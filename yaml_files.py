import os
from paths import RANDO_ROOT_PATH
from pathlib import Path
import yaml


# from: https://gist.github.com/pypt/94d747fe5180851196eb?permalink_comment_id=4015118#gistcomment-4015118
class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = set()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(f"Duplicate {key!r} key found in YAML.")
            mapping.add(key)
        return super().construct_mapping(node, deep)


def yaml_load(file_path: Path):
    with file_path.open("r", encoding="utf-8") as f:
        return yaml.load(f, UniqueKeyLoader)


beedle_texts_file = RANDO_ROOT_PATH / "beedle_texts.yaml"
beedle_texts = yaml_load(beedle_texts_file)

checks_file = RANDO_ROOT_PATH / "checks.yaml"
checks = yaml_load(checks_file)

eventpatches_file = RANDO_ROOT_PATH / "eventpatches.yaml"
eventpatches = yaml_load(eventpatches_file)

hints_file = RANDO_ROOT_PATH / "hints.yaml"
hints = yaml_load(hints_file)

items_file = RANDO_ROOT_PATH / "items.yaml"
items = yaml_load(items_file)

map_exits_file = RANDO_ROOT_PATH / "entrances.yaml"
map_exits = yaml_load(map_exits_file)

music_file = RANDO_ROOT_PATH / "music.yaml"
music = yaml_load(music_file)

options_file = RANDO_ROOT_PATH / "options.yaml"
options = yaml_load(options_file)

patches_file = RANDO_ROOT_PATH / "patches.yaml"
patches = yaml_load(patches_file)

glitchless_requirements_file = (
    RANDO_ROOT_PATH / "SS Rando Logic - Glitchless Requirements.yaml"
)
glitchless_requirements = yaml_load(glitchless_requirements_file)

glitched_requirements_file = (
    RANDO_ROOT_PATH / "SS Rando Logic - Glitched Requirements.yaml"
)
glitched_requirements = yaml_load(glitched_requirements_file)


def requirements_gen(folder: Path):
    files = sorted(os.listdir(folder))
    files = filter(lambda s: s[0].isupper() and s.endswith(".yaml"), files)
    requirements = {
        os.path.splitext(filename)[0]: yaml_load(folder / filename)
        for filename in files
    } | {"allowed-time-of-day": "Both"}
    requirements["exits"] = {"Start": "Nothing"}
    if "macros.yaml" in os.listdir(folder):
        requirements["macros"] = yaml_load(folder / "macros.yaml")
    return requirements


requirements_folder = RANDO_ROOT_PATH / "logic" / "requirements"
requirements = requirements_gen(requirements_folder)
