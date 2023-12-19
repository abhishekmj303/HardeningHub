from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]

    script = "#!/bin/bash\n\n"  # Start with a bash shebang and a newline

    # Check if 'udf' is to be blocked
    if 'udf' in file_systems_config['block'] and file_systems_config['block']['udf']:
        script += """
echo "Processing module: udf..."

# Check if module 'udf' is set to be not loadable
if ! modprobe -n -v udf | grep -q 'install /bin/true'; then
    echo "Setting module 'udf' to be not loadable"
    echo "install udf /bin/false" | sudo tee /etc/modprobe.d/udf.conf
fi

# Unload module 'udf' if it is currently loaded
if lsmod | grep -q "udf"; then
    echo "Unloading module 'udf'"
    sudo modprobe -r udf
fi

# Blacklist module 'udf' if not already blacklisted
if ! grep -q "blacklist udf" /etc/modprobe.d/*; then
    echo "Blacklisting module 'udf'"
    echo "blacklist udf" | sudo tee -a /etc/modprobe.d/udf.conf
fi
"""
    return script

if __name__ == "__main__":
    # Example configuration for demonstration
    config = {
        "file-systems": {
            "block": {
                "udf": True
            }
        }
    }
    generated_script = get_script(config)
    print(generated_script)
