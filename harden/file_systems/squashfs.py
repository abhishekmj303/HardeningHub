import subprocess
from harden import config_file

def get_script(config):
    file_systems_config = config["file-systems"]

    # Start with an empty script and build it up
    script = ""

    if 'squashfs'in file_systems_config['block']:
        # Each file system gets its own set of commands
        script += f"""
l_mname="squashfs" # set module name
if ! modprobe -n -v "$l_mname" | grep -P --
'^\h*install
\/bin\/(true|false)'; then
echo -e " - setting module: \"$l_mname\" to be not loadable"
echo -e "install $l_mname /bin/false" >>
/etc/modprobe.d/"$l_mname".conf
fi
if lsmod | grep "$l_mname" > /dev/null 2>&1; then
echo -e " - unloading module \"$l_mname\""
modprobe -r "$l_mname"
fi
if ! grep -Pq --
"^\h*blacklist\h+$l_mname\b" /etc/modprobe.d/*; then
echo -e " - deny listing \"$l_mname\""
echo -e "blacklist $l_mname" >> /etc/modprobe.d/"$l_mname".conf
fi
"""
    return script

if __name__ == "__main__":
    config = config_file.read()
    print(get_script(config))
