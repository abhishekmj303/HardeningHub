from harden import config_file

def get_script(config):
    firewall_config = config["firewall"]
    # Start with an empty script and build it up
    script = ""

    if firewall_config['enable']:
        # Each file system gets its own set of commands
        script += f"apt install ufw\n"
        script += f"apt purge iptables-persistent\n"
        script += f"systemctl --now enable ufw.service\n"
        if firewall_config['configure_loopback_traffic']:
            script += f"ufw allow in on lo\n"
            script += "ufw allow out on lo\n"
            script += "ufw deny in from 127.0.0.0/8\n"
            script += "ufw deny in from ::1\n"
        elif firewall_config['enable_default_deny']:
            script += "ufw default deny incoming\n"
            script += "ufw default deny outgoing\n"
            script += "ufw default deny routed\n"

    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))