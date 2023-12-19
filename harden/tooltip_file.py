import tomlkit
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "../config/tooltip.toml")

def read():
    with open(FILE_PATH, "r") as f:
        return tomlkit.load(f)