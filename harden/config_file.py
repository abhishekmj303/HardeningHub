import tomlkit
import os
import shutil
from typing import Mapping
from harden import physical_ports

# Config directory of user
CONFIG_DIR = os.path.expanduser("~/.config/HardeningHub")
PROFILE_DIR = os.path.join(CONFIG_DIR, "profiles")
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/HardeningHub/default_config.toml")
TEMP_FILE_PATH = DEFAULT_CONFIG_PATH + ".tmp"

SAMPLE_FILE_PATH = os.path.join(os.path.dirname(__file__), "../config/sampleconfig.toml")

def create_copy(file_path: str = DEFAULT_CONFIG_PATH, temp_file_path: str = None):
    global TEMP_FILE_PATH
    if temp_file_path is None:
        temp_file_path = file_path + ".tmp"
    TEMP_FILE_PATH = temp_file_path
    shutil.copyfile(file_path, TEMP_FILE_PATH)


def read(file_path: str = None):
    if file_path is None:
        file_path = TEMP_FILE_PATH
    with open(file_path, "r") as f:
        return tomlkit.load(f)


def write(config: Mapping):
    with open(TEMP_FILE_PATH, "w") as f:
        tomlkit.dump(config, f)


def save(file_path: str = None):
    if file_path is None:
        file_path = TEMP_FILE_PATH.replace(".tmp", "")
    shutil.copyfile(TEMP_FILE_PATH, file_path)


def get_profiles():
    if not os.path.exists(PROFILE_DIR):
        init_config_dir()
        return []
    
    all_files = os.listdir(PROFILE_DIR)
    profiles = []
    for file in all_files:
        if file.endswith("_config.toml"):
            profiles.append(file.replace("_config.toml", ""))
    
    return profiles


def get_profile_path(profile_name: str):
    return os.path.join(PROFILE_DIR, profile_name + "_config.toml")


def init_config_dir():
    # Create the config directory if it doesn't exist
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        os.makedirs(PROFILE_DIR)
    # Create the default config file if it doesn't exist
    if not os.path.exists(DEFAULT_CONFIG_PATH):
        shutil.copyfile(SAMPLE_FILE_PATH, DEFAULT_CONFIG_PATH)


def init(file_path: str = DEFAULT_CONFIG_PATH):
    create_copy(file_path)
    return physical_ports.get_devices(read(file_path))


def init_profile(profile_name: str):
    file_path = get_profile_path(profile_name)
    shutil.copyfile(DEFAULT_CONFIG_PATH, file_path)
    create_copy(file_path)
    return physical_ports.get_devices(read(file_path))


def import_level(level: str = "w1"):
    if level == "w1":
        file_path = os.path.join(os.path.dirname(__file__), "../config/workstation/level-1.toml")
    elif level == "w2":
        file_path = os.path.join(os.path.dirname(__file__), "../config/workstation/level-2.toml")
    elif level == "s1":
        file_path = os.path.join(os.path.dirname(__file__), "../config/server/level-1.toml")
    elif level == "s2":
        file_path = os.path.join(os.path.dirname(__file__), "../config/server/level-2.toml")
    
    create_copy(file_path, TEMP_FILE_PATH)
    return physical_ports.get_devices(read(file_path))


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
