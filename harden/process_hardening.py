from harden import config_file

def get_script(config):
    file_systems_config = config["processes"]

    # Start with an empty script and build it up
    script = ""

    if file_systems_config.get('remove_prelink', False):
        script += """
prelink -ua
apt purge prelink
"""

    if file_systems_config.get('enable_aslr', False):
        script += """
echo "kernel.randomize_va_space = 2" >> /etc/sysctl.d/60-kernel_sysctl.conf
sysctl -w kernel.randomize_va_space=2
"""

    if file_systems_config.get('disable_error_reporting', False):
        script += """
# Disable error reporting
echo "enabled=0" > /etc/default/apport
systemctl stop apport.service
systemctl --now disable apport.service
# Alternatively, to remove the apport package
# apt purge apport
"""

    if file_systems_config.get('restrict_core_dumps', False):
        script += """
# Restrict core dumps
echo "* hard core 0" >> /etc/security/limits.conf
echo "fs.suid_dumpable = 0" >> /etc/sysctl.conf
sysctl -w fs.suid_dumpable=0
# If systemd-coredump is installed, configure coredump settings
if [ -f /etc/systemd/coredump.conf ]; then
    echo "Storage=none" >> /etc/systemd/coredump.conf
    echo "ProcessSizeMax=0" >> /etc/systemd/coredump.conf
    systemctl daemon-reload
fi
"""

    return script

if __name__ == "__main__":
    config = config_file.read()
    print(get_script(config))
