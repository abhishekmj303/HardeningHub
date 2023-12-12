import subprocess
import re
import os
# Read the configuration file
test_directory = os.path.dirname(os.path.abspath(__file__))
absolute_path = os.path.join(test_directory, '..', 'config', 'sampleconfig.toml')
config_file = absolute_path 

print(config_file)
rules_file_path = os.path.join(test_directory, '..', 'BackEnd', 'rules.conf')


# Check if the configuration file exists
if not os.path.exists(config_file):
    print("Error: Configuration file not found.")
    exit(1)

# Check if USBGuard is enabled
with open(config_file, 'r') as file:
    config_content = file.read()
    print(config_content)

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
