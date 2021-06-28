from pathlib import Path
from typing import AnyStr
import os


def get_project_root() -> AnyStr:
    return Path(__file__).parent.parent.as_posix()


def get_data_dir() -> AnyStr:
    return os.path.join(get_project_root(), "data")

