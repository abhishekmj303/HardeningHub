#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/../harden/file_systems/squashfs.py"
echo "Python script path: $PYTHON_SCRIPT"

# Check if the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script not found."
    exit 1
fi

# Run the Python script and capture its output
echo "Running the Python script..."
script_output=$(python3 "$PYTHON_SCRIPT")

# Check the exit status of the Python script
if [ $? -ne 0 ]; then
    echo "Python script execution failed."
    exit 1
fi

# Optionally, print the output for verification
echo "Python script output:"
echo "$script_output"

# Execute the output as a Bash script
# WARNING: Executing scripts directly can be risky, especially with sudo commands.
# Ensure you thoroughly understand and trust the script before executing.
echo "Executing the generated Bash script..."
bash -c "$script_output"

echo "Script executed successfully."
