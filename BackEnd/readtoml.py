import subprocess
from tomlkit import loads
import os

def run_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as error:
        print(error)
        exit(1)


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
print(parsed_data)
# Check if the 'enable' key is present and set to True
enable = parsed_data['physical-ports']['enable']
#print(enable)
# Check if USBGuard should be disabled
if not enable:
    subprocess.run(["sudo", "systemctl", "disable", "--now", "usbguard"])
    exit()

# Generate rules based on parsed data
rules_content = ""
allow_all = parsed_data['physical-ports']['allow-all']
#print(allow_all)
if allow_all:
    rules_content = "allow\n"
else:
    for rule in parsed_data['physical-ports']['rules']:
        for key in rule:
            if key == 'allow':
                if rule[key]:
                    if 'id' in rule:
                        rules_content += f"allow id {rule['id']} "
                    if 'name' in rule:
                        rules_content += f"name {rule['name']} "
                    if 'port' in rule:
                        rules_content += f"via-port {rule['port']}\n"
                    else:
                        rules_content += "\n"
                else:
                    rules_content += "reject \n"

# Write rules to rules.conf
print(rules_content)
with open(rules_file_path, 'w') as rules_file:
    rules_file.write(rules_content)

# Install rules
run_command(["sudo", "install", "-m", "0600", "-o", "root", "-g", "root", rules_file_path, "rules.conf"])

# Restart and enable USBGuard
#run_command(["sudo", "systemctl", "daemon-reload"])
#run_command(["sudo", "systemctl", "restart", "usbguard"])
#run_command(["sudo", "systemctl", "enable", "usbguard"])

