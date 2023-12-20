from harden import config_file

def get_script(config):
    privilege_escalation_config = config["privilege_escalation"]
    script = ""

    if privilege_escalation_config["use_pty"]:
        script += '''
config_file="/etc/sudoers"

cp "$config_file" "$config_file.bak"

if grep -q "^Defaults[[:space:]]*use_pty" "$config_file"; then
    echo
else
    echo "Defaults use_pty" >> "$config_file"
fi
'''
    if privilege_escalation_config["enable_logfile"]:
        script += '''
config_file="/etc/sudoers"

cp "$config_file" "$config_file.bak"

if grep -q "^Defaults[[:space:]]*logfile" "$config_file"; then
    echo
else
    echo "Defaults logfile=/var/log/sudo.log" >> "$config_file"
fi
'''

    if privilege_escalation_config["disable_nopassword"]:
        script += '''
config_file="/etc/sudoers"

cp "$config_file" "$config_file.bak"

if grep -q NOPASSWD "$config_file"; then
    sed -i 'NOPASSWD/d' "$config_file"
fi
'''
    
    if privilege_escalation_config["enable_reauthentication"]:
        script += '''
config_file="/etc/sudoers"

cp "$config_file" "$config_file.bak"

if grep -q "!authenticate" "$config_file"; then
    sed -i '!authenticate/d' "$config_file"
fi
'''
    
    if privilege_escalation_config["authentication_timeout"]:
        script += '''
authentication_timeout = privilege_escalation_config["authentication_timeout"]
config_file="/etc/sudoers"

cp "$config_file" "$config_file.bak"

if grep -q "^Defaults[[:space:]]*timestamp_timeout" "$config_file"; then
    sed -i "s/^Defaults[[:space:]]*timestamp_timeout.*/Defaults timestamp_timeout=$authentication_timeout/" "$config_file"
else
    echo "Defaults timestamp_timeout=$authentication_timeout" >> "$config_file"
fi

if grep -q "^Defaults[[:space:]]*env_reset,[[:space:]]*timestamp_timeout" "$config_file"; then
    sed -i "s/^Defaults[[:space:]]*env_reset,[[:space:]]*timestamp_timeout.*/Defaults env_reset, timestamp_timeout=$authentication_timeout/" "$config_file"
else
    echo "Defaults env_reset, timestamp_timeout=$authentication_timeout" >> "$config_file"
fi
'''

    if privilege_escalation_config["restrict_su"]:
        script += '''
empty_group = "sugroup"

groupadd "$empty_group"

su_line = "auth required pam_wheel.so use_uid group=$empty_group"
echo "$su_line" >> /etc/pam.d/su 
'''
    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))