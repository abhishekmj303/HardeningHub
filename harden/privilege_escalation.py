from harden import config_file

def get_script(config):
    privilege_escalation_config = config["privilege_escalation"]
    script = "#!/bin/bash\n\n"  # Start with a bash shebang and a newline

    if privilege_escalation_config["use_pty"]:
        script += '''
config_file="/etc/sudoers"
sudo cp "$config_file" "$config_file.bak"

if ! sudo grep -q "^Defaults[[:space:]]*use_pty" "$config_file"; then
    echo "Defaults use_pty" | sudo tee -a "$config_file"
fi
'''
    if privilege_escalation_config["enable_logfile"]:
        script += '''
config_file="/etc/sudoers"
sudo cp "$config_file" "$config_file.bak"

if ! sudo grep -q "^Defaults[[:space:]]*logfile" "$config_file"; then
    echo "Defaults logfile=/var/log/sudo.log" | sudo tee -a "$config_file"
fi
'''

    if privilege_escalation_config["disable_nopassword"]:
        script += '''
config_file="/etc/sudoers"
sudo cp "$config_file" "$config_file.bak"

if sudo grep -q NOPASSWD "$config_file"; then
    sudo sed -i '/NOPASSWD/d' "$config_file"
fi
'''
    
    if privilege_escalation_config["enable_reauthentication"]:
        script += '''
config_file="/etc/sudoers"
sudo cp "$config_file" "$config_file.bak"

if sudo grep -q "!authenticate" "$config_file"; then
    sudo sed -i '/!authenticate/d' "$config_file"
fi
'''
    if privilege_escalation_config['enable_authentication_timeout']:
        return script
    
    if privilege_escalation_config["authentication_timeout"]:
        authentication_timeout = privilege_escalation_config["authentication_timeout"]
        script += f'''
config_file="/etc/sudoers"
sudo cp "$config_file" "$config_file.bak"

if sudo grep -q "^Defaults[[:space:]]*timestamp_timeout" "$config_file"; then
    sudo sed -i "s/^Defaults[[:space:]]*timestamp_timeout.*/Defaults timestamp_timeout={authentication_timeout}/" "$config_file"
else
    echo "Defaults timestamp_timeout={authentication_timeout}" | sudo tee -a "$config_file"
fi

if sudo grep -q "^Defaults[[:space:]]*env_reset,[[:space:]]*timestamp_timeout" "$config_file"; then
    sudo sed -i "s/^Defaults[[:space:]]*env_reset,[[:space:]]*timestamp_timeout.*/Defaults env_reset, timestamp_timeout={authentication_timeout}/" "$config_file"
else
    echo "Defaults env_reset, timestamp_timeout={authentication_timeout}" | sudo tee -a "$config_file"
fi
'''

    if privilege_escalation_config["restrict_su"]:
        empty_group = "sugroup"
        script += f'''
sudo groupadd "$empty_group" || true  # Ignore if group already exists
su_line="auth required pam_wheel.so use_uid group=$empty_group"
echo "$su_line" | sudo tee -a /etc/pam.d/su 
'''
    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))
