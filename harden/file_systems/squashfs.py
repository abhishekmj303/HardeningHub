from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]

    script = "#!/bin/bash\n\n"  # Start with a bash shebang and a newline

    # Check if 'squashfs' is to be blocked
    if 'squashfs' in file_systems_config['block'] and file_systems_config['block']['squashfs']:
        script += """
echo "Processing module: squashfs..."

# Check if module 'squashfs' is set to be not loadable
if ! modprobe -n -v squashfs | grep -q 'install /bin/true'; then
    echo "Setting module 'squashfs' to be not loadable"
    echo "install squashfs /bin/false" | sudo tee /etc/modprobe.d/squashfs.conf
fi

# Unload module 'squashfs' if it is currently loaded
if lsmod | grep -q "squashfs"; then
    echo "Unloading module 'squashfs'"
    sudo modprobe -r squashfs
fi

# Blacklist module 'squashfs' if not already blacklisted
if ! grep -q "blacklist squashfs" /etc/modprobe.d/*; then
    echo "Blacklisting module 'squashfs'"
    echo "blacklist squashfs" | sudo tee -a /etc/modprobe.d/squashfs.conf
fi
"""
    return script

if __name__ == "__main__":
    # Example configuration for demonstration
    config = {
        "file-systems": {
            "block": {
                "squashfs": True
            }
        }
    }
    generated_script = get_script(config)
    print(generated_script)
