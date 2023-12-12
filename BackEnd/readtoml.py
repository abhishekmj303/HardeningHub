import subprocess
from tomlkit import parse
from tomlkit import dumps
from tomlkit import table
import os
# Read the configuration file
test_directory = os.path.dirname(os.path.abspath(__file__))
absolute_path = os.path.join(test_directory, '..', 'config', 'sampleconfig.toml')
config_file_path = absolute_path 

rules_file_path = os.path.join(test_directory, '..', 'BackEnd', 'rules.conf')

# Check if the configuration file exists
if not os.path.exists(config_file_path):
    print("Error: Configuration file not found.")
    exit(1)


def parse_toml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            toml_content = file.read()
            print(toml_content)
            parsed_data = tomlkit.loads(toml_content)
            return parsed_data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except tomlkit.exceptions.ParseError as e:
        print(f"Error parsing TOML file: {e}")
        return None

# Example usage
toml_file_path = config_file_path  # Replace with the actual path to your TOML file

parsed_data = parse_toml_file(toml_file_path)
print(parsed_data)



''' 
enable_usbguard = len(re.findall(r'enable\s*=\s*true', config_content, re.IGNORECASE))
if enable_usbguard == 0:
    subprocess.run(['sudo', 'systemctl', 'disable', '--now', 'readtoml'])
    exit(0)

# Generate rules.conf
with open(rules_file_path, 'w') as rules_file:
    rules_file.write("# USBGuard rules.conf\n")

allow_all = len(re.findall(r'allow-all\s*=\s*true', config_content, re.IGNORECASE))

# Allow all or generate rules based on configuration
if allow_all == 1:
    with open('rules.conf', 'a') as rules_file:
        rules_file.write("allow\n")
else:
    # Loop through each rule and add it to rules.conf
    allow_rules = re.findall(r'^\s*allow\s*{.*?}', config_content, re.DOTALL | re.MULTILINE)
    for rule in allow_rules:
        id_value = re.search(r'id\s*=\s*"(.*?)"', rule).group(1)
        name_value = re.search(r'name\s*=\s*"(.*?)"', rule).group(1)
        port_value = re.search(r'port\s*=\s*"(.*?)"', rule).group(1)
        with open('rules.conf', 'a') as rules_file:
            rules_file.write(f'allow {id_value} name "{name_value}" via-port "{port_value}"\n')

# Install rules and restart USBGuard
subprocess.run(['sudo', 'install', '-m', '0600', '-o', 'root', '-g', 'root', 'rules.conf', '/etc/usbguard/rules.conf'])
subprocess.run(['sudo', 'systemctl', 'restart', 'usbguard'])
subprocess.run(['sudo', 'systemctl', 'enable', 'usbguard'])

print("USBGuard configured successfully.")
'''