# This File Reads the TOML File and Generates the Rules File
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

def ConfUtile(parsed_data,test_directory):
    #print(parsed_data)
    # Check if the 'enable' key is present and set to True
    enable = parsed_data['physical-ports']['enable']
    if not enable:
        temp_disable_file = os.path.join(test_directory, 'disable_usbguard.tmp')
        with open(temp_disable_file, 'w') as file:
            file.write("disable")
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
                        rules_content += "allow "
                        if 'id' in rule:
                            rules_content += f"{rule['id']} "
                        if 'name' in rule:
                            rules_content += f"name  \"{rule['name']}\" "
                        if 'port' in rule:
                            rules_content += f"via-port \"{rule['port']}\"\n"
                        else:
                            rules_content += "\n"
                    else:
                        rules_content += "reject "
                        if 'id' in rule:
                            rules_content += f"reject {rule['id']} "
                        if 'name' in rule:
                            rules_content += f"name \"{rule['name']}\" "
                        if 'port' in rule:
                            rules_content += f"via-port {rule['port']}\n"
                        else:
                            rules_content += "\n"
    return rules_content



# Parse the TOML configuration file
parsed_data = parse_toml_file(config_file_path)
rules_content = ConfUtile(parsed_data,test_directory)
print(rules_content)


