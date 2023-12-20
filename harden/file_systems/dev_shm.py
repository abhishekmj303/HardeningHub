import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]
    # Start with an empty script and build it up
    script = ""

    if file_systems_config['configure_fs']['dev_shm']:
        # Each file system gets its own set of commands
        script += """
#!/bin/bash

echo "Applying remediation for the /dev/shm partition..."

# Backup /etc/fstab
cp /etc/fstab /etc/fstab.backup

# Add nodev option to /dev/shm in /etc/fstab
if grep -q "/dev/shm" /etc/fstab; then
    # /dev/shm is present in fstab, update it
    sed -i '/\/dev\/shm/ s/defaults/defaults,nodev/' /etc/fstab
else
    # /dev/shm not present, add it
    echo "tmpfs /dev/shm tmpfs defaults,nodev 0 0" >> /etc/fstab
fi

# Remount /dev/shm
mount -o remount /dev/shm

echo "Remediation applied. /dev/shm is now mounted with 'nodev' option."

"""
    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))



