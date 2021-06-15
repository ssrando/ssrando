from paths import IS_RUNNING_FROM_SOURCE, RANDO_ROOT_PATH
from pathlib import Path

# Try to add the git commit hash to the version number if running from source.
if IS_RUNNING_FROM_SOURCE:
    VERSION = (RANDO_ROOT_PATH / "version.txt").read_text().strip()
    VERSION_WITHOUT_COMMIT = VERSION
    version_suffix = "_NOGIT"

    import subprocess

    try:
        version_suffix = (
            "_"
            + subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], cwd=Path(__file__).parent
            )
            .decode("ASCII")
            .strip()
        )
    except Exception:
        pass  # probably not git installed

    VERSION += version_suffix
else:
    VERSION = (RANDO_ROOT_PATH / "version-with-git.txt").read_text().strip()
    VERSION_WITHOUT_COMMIT = VERSION
