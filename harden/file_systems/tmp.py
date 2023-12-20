import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]
    # Start with an empty script and build it up
    script = "#!/bin/bash\n\n"

    if file_systems_config.get('configure_fs', {}).get('tmp', False):
        # Unmask the tmp.mount for systemd
        script += "sudo systemctl unmask tmp.mount\n"

        # Check if /etc/fstab needs to be updated
        if file_systems_config['configure_fs']['tmp'].get('update_fstab', False):
            script += (
                "# Update /etc/fstab for tmpfs configuration\n"
                "echo 'tmpfs /tmp tmpfs defaults,rw,nosuid,nodev,noexec,relatime,size=2G 0 0' | sudo tee -a /etc/fstab\n"
            )

        # Check if tmp.mount file needs to be created/updated
        if file_systems_config['configure_fs']['tmp'].get('update_tmp_mount', False):
            script += (
                "# Create/update tmp.mount file\n"
                "echo '[Unit]\\nDescription=Temporary Directory /tmp\\n"
                "ConditionPathIsSymbolicLink=!/tmp\\nDefaultDependencies=no\\n"
                "Conflicts=umount.target\\nBefore=local-fs.target umount.target\\n"
                "After=swap.target\\n[Mount]\\nWhat=tmpfs\\nWhere=/tmp\\n"
                "Type=tmpfs' | sudo tee /etc/systemd/system/tmp.mount\n"
            )

        # Add a command to start the tmp.mount service
        script += "sudo systemctl start tmp.mount\n"

    return script

if __name__ == "__main__":
    # Example configuration for demonstration
    config = {
        "file-systems": {
            "configure_fs": {
                "tmp": {
                    "update_fstab": True,
                    "update_tmp_mount": True
                }
            }
        }
    }
    generated_script = get_script(config)
    print(generated_script)
