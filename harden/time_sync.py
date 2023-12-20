import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["time-sync"]
    # Start with an empty script and build it up
    script = ""

    if file_systems_config['enable_ntp']:
        # Install NTP package
        script += "sudo apt install ntp\n"
        # Add or edit the line in /etc/init.d/ntp
        if file_systems_config['ntp_servers']:
            for item in file_systems_config['ntp_servers']:
                script += f"echo 'server {item}' iburst| sudo tee -a /etc/ntp.conf\n"
        if file_systems_config['enable_ntp_user']:
            script += "echo 'RUNASUSER=ntp' | sudo tee -a /etc/init.d/ntp\n"
    

        # Restart NTP service
        script += "sudo systemctl restart ntp.service\n"
    
    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))
