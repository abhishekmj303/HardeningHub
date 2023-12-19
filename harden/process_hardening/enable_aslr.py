import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["processes"]

    # Start with an empty script and build it up
    script = ""

    if file_systems_config['enable_aslr']:
        script += f"""
echo "kernel.randomize_va_space = 2" >> /etc/sysctl.d/60-kernel_sysctl.conf
sysctl -w kernel.randomize_va_space=2
"""
    return script

if __name__ == "__main__":
    config = config_file.read()
    print(get_script(config))
