import tomlkit
import os
import shutil
from typing import Mapping
from harden import physical_ports

FILE_PATH = ""
TEMP_FILE_PATH = ""


def create_copy():
    shutil.copyfile(FILE_PATH, TEMP_FILE_PATH)


def read():
    if not os.path.exists(TEMP_FILE_PATH):  # Check if the copy does not exist
        create_copy()  # Create the copy if it doesn't exist
    with open(TEMP_FILE_PATH, "r") as f:
        return tomlkit.load(f)


def write(config: Mapping):
    with open(TEMP_FILE_PATH, "w") as f:
        tomlkit.dump(config, f)


def save(file_path: str = None):
    if file_path is None:
        file_path = FILE_PATH
    shutil.copyfile(TEMP_FILE_PATH, file_path)


def update_toml_obj(toml_obj: tomlkit.items.Item, config: dict):
    # Recursively update the toml object with the config dict
    for key, value in config.items():
        if isinstance(value, dict):
            update_toml_obj(value, toml_obj[key])
        elif isinstance(value, list):
            for i in range(len(value)):
                if i >= len(toml_obj[key]):
                    toml_obj[key].append(tomlkit.inline_table())
                if isinstance(value[i], dict):
                    update_toml_obj(value[i], toml_obj[key][i])
                else:
                    toml_obj[key][i] = value[i]
        else:
            toml_obj[key] = value


def init(file_path: str = None):
    global FILE_PATH, TEMP_FILE_PATH

    if file_path is None:
        file_path = os.path.join(os.path.dirname(__file__), "../config/sampleconfig.toml")
    
    FILE_PATH = file_path
    TEMP_FILE_PATH = FILE_PATH + ".tmp"
    create_copy()
    return physical_ports.get_devices(read())