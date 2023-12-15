import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]
    # Start with an empty script and build it up
    script = ""

    if file_systems_config['enable_aide']:
        # Each file system gets its own set of commands
        script += """
apt install aide aide-common
aideinit
mv /var/lib/aide/aide.db.new /var/lib/aide/aide.db
"""
    return script

def run_bash_script(script):
    try:
        # Run the script and capture the output
        result = subprocess.run(script, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr

def test_bash_script():
    # Run the script and capture the output
    audit = "dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' aide aide-common"
    result = subprocess.run(audit, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

if __name__ == "__main__":
    config = config_file.read()
    bash_script = get_script(config)
    stdout, stderr = run_bash_script(bash_script)

    print("STDOUT:\n", stdout)
    print("STDERR:\n", stderr)

    stdout, stderr = test_bash_script()
    print("AUDIT:", stdout)
    print("AUDITERR:", stderr)
