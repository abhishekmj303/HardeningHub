import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["apparmor"]
    # Start with an empty script and build it up

    script = ""
    if file_systems_config['enable']:
        # Install AppArmor
        script += "sudo apt-get install apparmor -y\n"
        script += "sudo apt install apparmor-utils\n"

        if file_systems_config['mode'] == 'enforce':
            # Set AppArmor profiles to enforce mode
            script += "sudo aa-enforce /etc/apparmor.d/*\n"
        elif file_systems_config['mode'] == 'complain':
            # Set AppArmor profiles to complain mode
            script += "sudo aa-complain /etc/apparmor.d/*\n"

    return script

if __name__ == "__main__":
    # Example configuration for demonstration
    config = {
        "apparmor": {
            "enable": True,
            "mode": "enforce"  # Can be "enforce" or "complain"
        }
    }
    generated_script = get_script(config)
    print(generated_script)
