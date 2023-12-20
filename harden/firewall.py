from harden import config_file

def get_script(config):
    firewall_config = config["firewall"]
    script = "#!/bin/bash\n\n"  # Start with a bash shebang and a newline

    if firewall_config['enable']:
        script += "sudo apt install ufw -y\n"  # Install UFW
        script += "sudo apt purge iptables-persistent -y\n"  # Purge iptables-persistent
        script += "sudo systemctl enable --now ufw.service\n"  # Enable and start UFW

        if firewall_config['configure_loopback_traffic']:
            # Configure loopback traffic rules
            script += "sudo ufw allow in on lo\n"
            script += "sudo ufw allow out on lo\n"
            script += "sudo ufw deny in from 127.0.0.0/8\n"
            script += "sudo ufw deny in from ::1\n"
        
        if firewall_config['enable_default_deny']:
            # Set default deny policies
            script += "sudo ufw default deny incoming\n"
            script += "sudo ufw default deny outgoing\n"
            script += "sudo ufw default deny routed\n"

        # Enable UFW with the applied rules
        script += "sudo ufw --force enable\n"
        script += "sudo ufw status verbose\n"  # Display UFW status

    return script

if __name__ == "__main__":
    # Example configuration
    config = {
        "firewall": {
            "enable": True,
            "configure_loopback_traffic": True,
            "enable_default_deny": False
        }
    }
    generated_script = get_script(config)
    print(generated_script)
