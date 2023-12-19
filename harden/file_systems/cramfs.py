from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]

    script = "#!/bin/bash\n\n"  # Start with a bash shebang and a newline

    # Loop through each filesystem module in the configuration
    for fs_module in file_systems_config['block']:
        if file_systems_config['block'][fs_module]:
            script += """
echo "Processing module: {fs_module}..."

# Check if module '{fs_module}' is set to be not loadable
if ! modprobe -n -v "{fs_module}" | grep -q 'install /bin/true'; then
    echo "Setting module '{fs_module}' to be not loadable"
    echo "install {fs_module} /bin/false" | sudo tee /etc/modprobe.d/{fs_module}.conf
fi

# Unload module '{fs_module}' if it is currently loaded
if lsmod | grep -q "{fs_module}"; then
    echo "Unloading module '{fs_module}'"
    sudo modprobe -r "{fs_module}"
fi

# Blacklist module '{fs_module}' if not already blacklisted
if ! grep -q "blacklist {fs_module}" /etc/modprobe.d/*; then
    echo "Blacklisting module '{fs_module}'"
    echo "blacklist {fs_module}" | sudo tee -a /etc/modprobe.d/{fs_module}.conf
fi
"""
    return script

if __name__ == "__main__":
    # Example configuration for demonstration
    config = {
        "file-systems": {
            "block": {
                "cramfs": True,
                "squashfs": True,
                "udf": True
            }
        }
    }
    generated_script = get_script(config)
    print(generated_script)
