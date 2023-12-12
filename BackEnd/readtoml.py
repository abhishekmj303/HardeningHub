import subprocess
from tomlkit import loads
import os

# Set file paths
test_directory = os.path.dirname(os.path.abspath(__file__))
absolute_path = os.path.join(test_directory, '..', 'config', 'sampleconfig.toml')
config_file_path = absolute_path
rules_file_path = os.path.join(test_directory, '..', 'BackEnd', 'rules.conf')

# Check if the configuration file exists
if not os.path.exists(config_file_path):
    print("Error: Configuration file not found.")
    exit(1)

# Define the parse_toml_file function
def parse_toml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            toml_content = file.read()
            parsed_data = loads(toml_content)
            return parsed_data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

# Parse the TOML configuration file
parsed_data = parse_toml_file(config_file_path)

# Check if the 'enable' key is present and set to True
enable = parsed_data.get('enable', False)

# Check if USBGuard should be disabled
if not enable:
    subprocess.run(["sudo", "systemctl", "disable", "--now", "usbguard"])
    exit()

# Generate rules based on parsed data
rules_content = ""
allow_all = parsed_data.get('allow-all', False)

if allow_all:
    rules_content = "allow-all:\n  allow\n"
else:
    for rule in parsed_data.get('rules', []):
        rules_content += f"  allow {rule['id']} name \"{rule['name']}\" via-port \"{rule['port']}\"\n"

# Write rules to rules.conf
with open(rules_file_path, 'w') as rules_file:
    rules_file.write(rules_content)

# Install rules
subprocess.run(["sudo", "install", "-m", "0600", "-o", "root", "-g", "root", rules_file_path, "/etc/usbguard/rules.conf"])

# Restart and enable USBGuard
subprocess.run(["sudo", "systemctl", "restart", "usbguard"])
subprocess.run(["sudo", "systemctl", "enable", "usbguard"])

