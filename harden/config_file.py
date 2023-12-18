import tomlkit
import os
import shutil
from typing import Mapping

file_path = ""
temp_file_path = ""

def set_config_file(path):
    global file_path, temp_file_path
    file_path = path
    temp_file_path = file_path + ".tmp"


def create_copy():
    shutil.copyfile(file_path, temp_file_path)


def read():
    if not os.path.exists(temp_file_path):  # Check if the copy does not exist
        create_copy()  # Create the copy if it doesn't exist
    with open(temp_file_path, "r") as f:
        return tomlkit.load(f)


def write(config: Mapping):
    with open(temp_file_path, "w") as f:
        tomlkit.dump(config, f)


def save():
    os.replace(temp_file_path, file_path)


set_config_file(os.path.join(os.path.dirname(__file__), "../config/sampleconfig.toml"))