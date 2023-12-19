from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]

    script = "#!/bin/bash\n\n"  # Start with a bash shebang and a newline

    # Check if 'squashfs' is to be blocked
    if 'squashfs' in file_systems_config['block'] and file_systems_config['block']['squashfs']:
        script += """
#!/bin/bash

echo "Processing module: squashfs..."

# Function to check if a module is blacklisted
is_blacklisted() {
    local module=$1
    grep -qrP "^\s*blacklist\s+$module\b" /etc/modprobe.d/ && return 0 || return 1
}

# Check if module 'squashfs' is set to be not loadable
if ! modprobe -n -v squashfs | grep -q 'install /bin/true'; then
    echo "Setting module 'squashfs' to be not loadable"
    echo "install squashfs /bin/false" | sudo tee /etc/modprobe.d/squashfs.conf
else
    echo "Module 'squashfs' is already set to be not loadable."
fi

# Unload module 'squashfs' if it is currently loaded
if lsmod | grep -q "squashfs"; then
    echo "Unloading module 'squashfs'"
    sudo modprobe -r squashfs || echo "Failed to unload module 'squashfs'. It might be in use."
else
    echo "Module 'squashfs' is not currently loaded."
fi

# Blacklist module 'squashfs' if not already blacklisted
if ! is_blacklisted "squashfs"; then
    echo "Blacklisting module 'squashfs'"
    echo "blacklist squashfs" | sudo tee -a /etc/modprobe.d/squashfs.conf
else
    echo "Module 'squashfs' is already blacklisted."
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
