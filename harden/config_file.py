import tomlkit
import os
import shutil
from typing import Mapping

file_path = os.path.join(os.path.dirname(__file__), "../config/sampleconfig.toml")
temp_file_path = os.path.join(os.path.dirname(file_path), "sampleconfig_copy.toml")


def create_copy():
    shutil.copyfile(file_path, temp_file_path)


def read():
    with open(temp_file_path, "r") as f:
        return tomlkit.load(f)


def write(config: Mapping):
    with open(temp_file_path, "w") as f:
        tomlkit.dump(config, f)


def save():
    os.replace(temp_file_path, file_path)
