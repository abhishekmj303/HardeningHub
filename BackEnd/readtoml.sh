#!/bin/bash
# Read the configuration file
config_file="git gsample.config.toml"  # Replace with the actual file path

# Check if the configuration file exists
if [ ! -e "$config_file" ]; then
    echo "Error: Configuration file not found."
    exit 1
fi

# Check if USBGuard is enabled
enable_usbguard=$(grep -i 'enable = true' "$config_file" | wc -l)
if [ "$enable_usbguard" -eq 0 ]; then
    sudo systemctl disable --now usbguard
    exit 0
fi

# Generate rules.conf
echo "# USBGuard rules.conf" > rules.conf

allow_all=$(grep -i 'allow-all = true' "$config_file" | wc -l)

# Allow all or generate rules based on configuration
if [ "$allow_all" -eq 1 ]; then
    echo "allow" >> rules.conf
else
    # Loop through each rule and add it to rules.conf
    while read -r rule; do
        id=$(echo "$rule" | awk -F= '/id/{gsub(/[ "]+/, "", $2); print $2}')
        name=$(echo "$rule" | awk -F= '/name/{gsub(/[ "]+/, "", $2); print $2}')
        port=$(echo "$rule" | awk -F= '/port/{gsub(/[ "]+/, "", $2); print $2}')
        echo "allow $id name \"$name\" via-port \"$port\"" >> rules.conf
    done < <(grep -E '^\s*allow' "$config_file" | sed 's/[{}]//g')
fi

# Install rules and restart USBGuard
sudo install -m 0600 -o root -g root rules.conf /etc/usbguard/rules.conf
sudo systemctl restart usbguard
sudo systemctl enable usbguard

echo "USBGuard configured successfully."
