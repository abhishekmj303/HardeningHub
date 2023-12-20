import subprocess
import shlex
from harden import config_file, physical_ports, file_systems\
    , process_hardening, apparmor, gdm, time_sync, firewall\
    , network, ssh, privilege_escalation, pam

def generate(backup: bool = False):
    config = config_file.read()
    script = "#!/bin/bash\n\n"
    if backup:
        # Generate timeshift snapshot
        script += """
if ! command -v timeshift &> /dev/null; then
    apt install timeshift -y
fi
timeshift --create --comments "Harden Script Backup"

"""
    script += physical_ports.get_script(config)
    script += file_systems.get_script(config)
    script += process_hardening.get_script(config)
    script += apparmor.get_script(config)
    script += gdm.get_script(config)
    script += time_sync.get_script(config)
    script += firewall.get_script(config)
    script += network.get_script(config)
    script += ssh.get_script(config)
    script += privilege_escalation.get_script(config)
    script += pam.get_script(config)
    return script

def save(file_path: str, backup: bool = False):
    with open(file_path, "w") as f:
        f.write(generate(backup))

def run(backup: bool = False):
    save("hardening_script.sh", backup)
    subprocess.Popen(
        shlex.split("""x-terminal-emulator -e "bash -c 'sudo bash hardening_script.sh; read -p \"Press enter to continue\"'" """)
    )

if __name__ == "__main__":
    config_file.init()
    save("script.sh")
    