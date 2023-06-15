from paths import IS_RUNNING_FROM_SOURCE, RANDO_ROOT_PATH
from pathlib import Path

# Try to add the git commit hash to the version number if running from source.
if IS_RUNNING_FROM_SOURCE:
    import toml

    with open("pyproject.toml") as f:
        proj = toml.load(f)
    VERSION = proj["tool"]["poetry"]["version"]
    VERSION_WITHOUT_COMMIT = VERSION
    version_suffix = "_NOGIT"

    import subprocess

    try:
        version_suffix = (
            "_"
            + subprocess.check_output(
                ["git", "rev-parse", "--short=7", "HEAD"], cwd=Path(__file__).parent
            )
            .decode("ASCII")
            .strip()
        )
        retcode = subprocess.call(["git", "diff-index", "--quiet", "HEAD", "--"])
        if retcode != 0:
            version_suffix += "_dirty"
    except Exception:
        pass  # probably not git installed

    VERSION += version_suffix
else:
    VERSION = (RANDO_ROOT_PATH / "version-with-git.txt").read_text().strip()
    VERSION_WITHOUT_COMMIT = VERSION
