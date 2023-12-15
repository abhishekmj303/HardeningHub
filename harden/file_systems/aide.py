import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]
    # Start with an empty script and build it up
    script = ""

    if file_systems_config['enable_aide']:
        # Each file system gets its own set of commands
        script += f"""
apt install aide aide-common
aideinit
mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
"""
    return script

if __name__ == "__main__":
    config = config_file.read()
    print(get_script(config))
