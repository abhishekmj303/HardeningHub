import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["apparmor"]
    # Start with an empty script and build it up
    script = ""

    if file_systems_config['enable']:
        # Each file system gets its own set of commands
        script += f"sudo apt install apparmor"
    if file_systems_config['mode'] == 'enforce':
        script += f"aa-enforce /etc/apparmor.d/*"
    else:
        script += f"aa-complain /etc/apparmor.d/*"
    return script

if __name__ == "__main__":
    config = config_file.read()
    print(get_script(config))
