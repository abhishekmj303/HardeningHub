from harden import config_file

def get_script(config):
    privilege_escalation_config = config["privilege_escalation"]
    script = ""

    if privilege_escalation_config["use_pty"]:
        script += '''
sudoers_line="Defaults use_pty"
visudo -c -q || { echo "Error: visudo check failed. Please fix the sudoers file manually."; exit 1; }
echo "$sudoers_line" | sudo EDITOR='tee -a' visudo
'''
    if privilege_escalation_config["enable_logfile"]:
        script += ''

    if privilege_escalation_config["disable_password"]:
        script += ''
    
    if privilege_escalation_config["enable_reauthentication"]:
        script += ''
    
    if privilege_escalation_config["authentication_timeout"]:
        script += ''

    if privilege_escalation_config["restrict_su"]:
        script += ''
    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))