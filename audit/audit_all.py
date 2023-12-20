import subprocess
import os

def run_bash_scripts(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if the file is a Bash script
        if os.path.isfile(file_path) and file_path.endswith('.sh'):
            print(f"Executing script: {filename}")
            try:
                result = subprocess.run(['bash', file_path], capture_output=True, text=True)
                print(f"Output of {filename}:\n{result.stdout}")
                if result.stderr:
                    print(f"Error in {filename}:\n{result.stderr}")
            except Exception as e:
                print(f"Error executing {filename}: {e}")

if __name__ == "__main__":
    audit_directory = 'HardeningHub/audit'  # Replace with the path to your audit directory
    run_bash_scripts(audit_directory)
