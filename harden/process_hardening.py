from harden import config_file

def get_script(config):
    file_systems_config = config["processes"]

    # Start with an empty script and build it up
    script = ""

    if file_systems_config.get('remove_prelink', False):
        script += """
sudo prelink -ua
apt purge prelink
"""

    if file_systems_config.get('enable_aslr', False):
        script += """
echo "kernel.randomize_va_space = 2" | sudo tee -a /etc/sysctl.d/60-kernel_sysctl.conf
sudo sysctl -w kernel.randomize_va_space=2
"""

    if file_systems_config.get('disable_error_reporting', False):
        script += """
# Check if Apport service is installed
if systemctl list-unit-files | grep -qw apport.service; then
    # Update Apport configuration to disable error reporting
    echo "enabled=0" | sudo tee /etc/default/apport

    # Stop and disable the Apport service
    sudo systemctl stop apport.service
    sudo systemctl disable apport.service

    echo "Apport error reporting has been disabled."
else
    echo "Apport service is not installed."
fi
"""

    if file_systems_config.get('restrict_core_dumps', False):
        script += """
systemctl is-enabled coredump.service
# Restrict core dumps
echo "Restricting core dumps..."

# Append settings to /etc/security/limits.conf
echo "* hard core 0" | sudo tee -a /etc/security/limits.conf

# Append and immediately apply the setting to sysctl
echo "fs.suid_dumpable = 0" | sudo tee -a /etc/sysctl.conf
sudo sysctl -w fs.suid_dumpable=0

# Configure systemd-coredump settings if installed
if [ -f /etc/systemd/coredump.conf ]; then
    echo "Configuring systemd-coredump settings..."
    sudo sed -i '/^Storage=/c\Storage=none' /etc/systemd/coredump.conf
    sudo sed -i '/^ProcessSizeMax=/c\ProcessSizeMax=0' /etc/systemd/coredump.conf
    sudo systemctl daemon-reload
fi

echo "Core dump restrictions applied successfully."

"""

    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))
