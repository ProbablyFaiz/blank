import os
from pathlib import Path

import dotenv

DOTENV_LOADED = False


def ensure_dotenv_loaded():
    global DOTENV_LOADED
    if not DOTENV_LOADED:
        dotenv.load_dotenv()
        DOTENV_LOADED = True


def getenv(name: str, default=None) -> str:
    """Get an environment variable. If the variable is not set, return the default value.

    Ensures that the .env file is loaded before attempting to get the environment variable.

    Args:
        name: The name of the environment variable.
        default: The default value to return if the environment variable is not set.
    """
    ensure_dotenv_loaded()
    return os.getenv(name, default)


def get_data_path(*args) -> Path:
    """Get the path to a file nested in the data directory. If the DATA_ROOT environment
    variable is set, use that as the root directory. Otherwise, use the data directory
    in the project root.

    Args:
        *args: The path components (strings or Path objects) to append to the data root.
    """
    if data_root := getenv("BLANKET_DATA_ROOT"):
        return Path(data_root).joinpath(*args)
    raise ValueError("DATA_ROOT environment variable is not set.")


BLANKET_ENV: str = getenv("BLANKET_ENV", "dev")


if BLANKET_ENV not in ("dev", "prod"):
    raise ValueError(f"BLANKET_ENV must be either 'dev' or 'prod', got: {BLANKET_ENV}")
