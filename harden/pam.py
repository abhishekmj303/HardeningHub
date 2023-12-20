from harden import config_file

def get_script(config):
    pam_config = config["pam"]

    required_password_level = pam_config.get('required_password_level', 'medium')
    minimum_password_length = pam_config.get('minimum_password_length', 14)

    # Start with an empty script and build it up
    script = """
#!/bin/bash

# Ensure the pam_pwquality module is installed
echo "Installing pam_pwquality module..."
sudo apt install libpam-pwquality -y

# Configure password quality requirements in /etc/security/pwquality.conf
echo "Configuring password policies..."

pwquality_conf="/etc/security/pwquality.conf"

# Create a backup of the original pwquality.conf file
sudo cp "$pwquality_conf" "$pwquality_conf.bak"

# Set minimum password length
sudo sed -i '/^minlen = /d' "$pwquality_conf"  # Remove existing minlen settings
echo "minlen = {}" | sudo tee -a "$pwquality_conf"
""".format(minimum_password_length)

    if required_password_level == 'strong':
        # Strong password complexity settings
        script += """
# Strong password complexity requirements
sudo sed -i '/^dcredit = /d' "$pwquality_conf"  # Remove existing dcredit settings
sudo sed -i '/^ucredit = /d' "$pwquality_conf"  # Remove existing ucredit settings
sudo sed -i '/^ocredit = /d' "$pwquality_conf"  # Remove existing ocredit settings
sudo sed -i '/^lcredit = /d' "$pwquality_conf"  # Remove existing lcredit settings
echo "dcredit = -1" | sudo tee -a "$pwquality_conf"
echo "ucredit = -1" | sudo tee -a "$pwquality_conf"
echo "ocredit = -1" | sudo tee -a "$pwquality_conf"
echo "lcredit = -1" | sudo tee -a "$pwquality_conf"
"""

    elif required_password_level == 'medium':
        # Medium password complexity settings
        # (Adjust as needed based on your definition of medium complexity)
        script += """
# Medium password complexity requirements
sudo sed -i '/^minclass = /d' "$pwquality_conf"  # Remove existing minclass settings
echo "minclass = 3" | sudo tee -a "$pwquality_conf"
"""

    # Add further conditions for 'weak' or 'stronger' if required

    script += """
echo "PAM password policies have been configured successfully."
"""

    return script

if __name__ == "__main__":
    config = config_file.init()
    generated_script = get_script(config)
    print(generated_script)
