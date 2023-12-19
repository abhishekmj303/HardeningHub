from harden import config_file

def get_script(config):
    file_systems_config = config["service_clients"]
    script = "#!/bin/bash\n\n"

    services = {
        'remove_nis': 'nis',
        'remove_rsh': 'rsh-client',
        'remove_talk': 'talk',
        'remove_telnet': 'telnet',
        'remove_ldap': 'ldap-utils',
        'remove_rpc': 'rpcbind'
    }

    for key, package in services.items():
        if file_systems_config.get(key, False):
            script += f"""
# Check and remove {package} if installed
if dpkg-query -W -f='{{Status}}' {package} 2>/dev/null | grep -q "ok installed"; then
    echo "Removing {package}..."
    sudo apt purge {package} -y
else
    echo "{package} is not already installed or has been removed."
fi
"""

    return script

if __name__ == "__main__":
    # Sample configuration for demonstration
    config = {
        "service_clients": {
            "remove_nis": True,
            "remove_rsh": True,
            "remove_talk": True,
            "remove_telnet": True,
            "remove_ldap": True,
            "remove_rpc": True
        }
    }
    generated_script = get_script(config)
    print(generated_script)
