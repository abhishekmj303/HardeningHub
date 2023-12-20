from harden import config_file

def get_script(config):
    pam_config = config["pam"]

    required_password_level = pam_config.get('required_password_level', 'medium')
    enable_password_length = pam_config.get('enable_password_length', True)
    minimum_password_length = pam_config.get('minimum_password_length', 14) if enable_password_length else 6
    limit_password_reuse = pam_config.get('limit_password_reuse', True)
    password_reuse_limit = pam_config.get('password_reuse_limit', 5)
    configure_hashing_algorithm = pam_config.get('configure_hashing_algorithm', True)

    # Start with an empty script and build it up
    script = """
#!/bin/bash

# Ensure the pam_pwquality module is installed
echo "Installing pam_pwquality module..."
sudo apt install libpam-pwquality -y

# Configure password quality requirements in /etc/security/pwquality.conf
echo "Configuring password policies..."

pwquality_conf="/etc/security/pwquality.conf"
sudo cp "$pwquality_conf" "$pwquality_conf.bak"
echo "minlen = {}" | sudo tee -a "$pwquality_conf"
""".format(minimum_password_length)

    if required_password_level == 'strong':
        script += """
sudo sed -i '/^dcredit = /d' "$pwquality_conf"
sudo sed -i '/^ucredit = /d' "$pwquality_conf"
sudo sed -i '/^ocredit = /d' "$pwquality_conf"
sudo sed -i '/^lcredit = /d' "$pwquality_conf"
echo "dcredit = -1" | sudo tee -a "$pwquality_conf"
echo "ucredit = -1" | sudo tee -a "$pwquality_conf"
echo "ocredit = -1" | sudo tee -a "$pwquality_conf"
echo "lcredit = -1" | sudo tee -a "$pwquality_conf"
"""
    elif required_password_level == 'medium':
        script += """
sudo sed -i '/^minclass = /d' "$pwquality_conf"
echo "minclass = 3" | sudo tee -a "$pwquality_conf"
"""
    # Add further conditions for 'weak' or 'stronger' if required

    if limit_password_reuse:
        script += """
# Limit password reuse
common_password="/etc/pam.d/common-password"
sudo sed -i '/pam_unix.so/ s/remember=[0-9]*/remember={}/' "$common_password"
""".format(password_reuse_limit)

    if configure_hashing_algorithm:
        script += """
# Configure hashing algorithm
sudo sed -i '/pam_unix.so/ s/\bmd5\b/yescrypt/' "$common_password"
login_defs="/etc/login.defs"
sudo sed -i '/^ENCRYPT_METHOD /c\ENCRYPT_METHOD yescrypt' "$login_defs"
"""

    script += "echo \"PAM configurations have been applied successfully.\""

    return script

if __name__ == "__main__":
    config = config_file.init()
    generated_script = get_script(config)
    print(generated_script)
