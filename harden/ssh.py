from harden import config_file

def get_script(config):
    network_config = config["ssh"]
    # Start with an empty script and build it up
    script = ""

    configure_permissions = network_config['configure_permissions']

    if configure_permissions['sshd_config']:
        script += '''
chown root:root /etc/ssh/sshd_config
chmod og-rwx /etc/ssh/sshd_config
'''

    if configure_permissions['private_host_key']:
        script += '''
{
l_skgn="ssh_keys" # Group designated to own openSSH keys
l_skgid="$(awk -F: '($1 == "'"$l_skgn"'"){print $3}' /etc/group)"
awk '{print}' <<< "$(find /etc/ssh -xdev -type f -name 'ssh_host_*_key' -
exec stat -L -c "%n %#a %U %G %g" {} +)" | (while read -r l_file l_mode
l_owner l_group l_gid; do
[ -n "$l_skgid" ] && l_cga="$l_skgn" || l_cga="root"
[ "$l_gid" = "$l_skgid" ] && l_pmask="0137" || l_pmask="0177"
l_maxperm="$( printf '%o' $(( 0777 & ~$l_pmask )) )"
if [ $(( $l_mode & $l_pmask )) -gt 0 ]; then
echo -e " - File: \"$l_file\" is mode \"$l_mode\" changing to mode:
\"$l_maxperm\""
if [ -n "$l_skgid" ]; then
chmod u-x,g-wx,o-rwx "$l_file"
else
chmod u-x,go-rwx "$l_file"
fi
fi
if [ "$l_owner" != "root" ]; then
echo -e " - File: \"$l_file\" is owned by: \"$l_owner\" changing
owner to \"root\""
chown root "$l_file"
fi
if [ "$l_group" != "root" ] && [ "$l_gid" != "$l_skgid" ]; then
echo -e " - File: \"$l_file\" is owned by group \"$l_group\" should
belong to group \"$l_cga\""
chgrp "$l_cga" "$l_file"
fi
done
)
}
'''

    if configure_permissions['public_host_key']:
        script += '''
find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec chmod u-x,go-wx {} \;
find /etc/ssh -xdev -type f -name 'ssh_host_*_key.pub' -exec chown root:root {} \;
'''

    script += f'''
user_list = {" ".join(network_config['allow_users'])}
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^AllowUsers" "$config_file"; then
    sed -i "s/^AllowUsers.*/AllowUsers $user_list/" "$config_file"
else
    echo "AllowUsers $user_list" >> "$config_file"
fi
'''
    script += f'''
group_list = {" ".join(network_config['allow_groups'])}
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^AllowGroups" "$config_file"; then
    sed -i "s/^AllowGroups.*/AllowGroups $group_list/" "$config_file"
else
    echo "AllowGroups $group_list" >> "$config_file"
fi
'''
    script += f'''
log_level = {network_config['log_level']}
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^LogLevel" "$config_file"; then
    sed -i "s/^LogLevel.*/LogLevel $log_level/" "$config_file"
else
    echo "LogLevel $log_level" >> "$config_file"
fi
'''
    if network_config['enable_pam']:
        script += f'''
use_pam = yes
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^UsePAM" "$config_file"; then
    sed -i "s/^UsePAM.*/UsePAM $use_pam/" "$config_file"
else
    echo "UsePAM $use_pam" >> "$config_file"
fi
'''
    if network_config['disable_root_login']:
        script += f'''
permit_root_login = no
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^PermitRootLogin" "$config_file"; then
    sed -i "s/^PermitRootLogin.*/PermitRootLogin $permit_root_login/" "$config_file"
else
    echo "PermitRootLogin $permit_root_login" >> "$config_file"
fi
'''
    if network_config['disable_host_based_auth']:
        script += f'''
host_based_auth = no
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^HostbasedAuthentication" "$config_file"; then
    sed -i "s/^HostbasedAuthentication.*/HostbasedAuthentication $host_based_auth/" "$config_file"
else
    echo "HostbasedAuthentication $host_based_auth" >> "$config_file"
fi
'''
        
    if network_config['disable_permit_empty_passwords']:
        script += f'''
permit_empty_passwords = no
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^PermitEmptyPasswords" "$config_file"; then
    sed -i "s/^PermitEmptyPasswords.*/PermitEmptyPasswords $permit_empty_passwords/" "$config_file"
else
    echo "PermitEmptyPasswords $permit_empty_passwords" >> "$config_file"
fi
'''
    if network_config['disable_permit_user_env']:
        script += f'''
permit_user_env = no
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^PermitUserEnvironment" "$config_file"; then
    sed -i "s/^PermitUserEnvironment.*/PermitUserEnvironment $permit_user_env/" "$config_file"
else
    echo "PermitUserEnvironment $permit_user_env" >> "$config_file"
fi
'''
    if network_config['enable_ignore_rhosts']:
        script += f'''
ignore_rhosts = yes
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^IgnoreRhosts" "$config_file"; then
    sed -i "s/^IgnoreRhosts.*/IgnoreRhosts $ignore_rhosts/" "$config_file"
else
    echo "IgnoreRhosts $ignore_rhosts" >> "$config_file"
fi
'''
    if network_config['disable_x11_forwarding']:
        script += f'''
x11_forwarding = no
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^X11Forwarding" "$config_file"; then
    sed -i "s/^X11Forwarding.*/X11Forwarding $x11_forwarding/" "$config_file"
else
    echo "X11Forwarding $x11_forwarding" >> "$config_file"
fi
'''
    if network_config['enable_strong_ciphers']:
        script += f'''
ciphers = chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^Ciphers" "$config_file"; then
    sed -i "s/^Ciphers.*/Ciphers $ciphers/" "$config_file"
else
    echo "Ciphers $ciphers" >> "$config_file"
fi
'''
    if network_config['enable_strong_mac_algorithms']:
        script += f'''
macs = hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,hmac-sha2-512,hmac-sha2-256
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^MACs" "$config_file"; then
    sed -i "s/^MACs.*/MACs $macs/" "$config_file"
else
    echo "MACs $macs" >> "$config_file"
fi
'''
    if network_config['enable_strong_key_exchange_algorithms']:
        script += f'''
kex_algorithms = curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group14-sha256,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,ecdh-sha2-nistp521,ecdh-sha2-nistp384,ecdh-sha2-nistp256,diffie-hellman-group-exchange-sha256 
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^KexAlgorithms" "$config_file"; then
    sed -i "s/^KexAlgorithms.*/KexAlgorithms $kex_algorithms/" "$config_file"
else
    echo "KexAlgorithms $kex_algorithms" >> "$config_file"
fi
'''
    if network_config['disable_tcp_forwarding']:
        script += f'''
allow_tcp_forwarding = no
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^AllowTcpForwarding" "$config_file"; then
    sed -i "s/^AllowTcpForwarding.*/AllowTcpForwarding $allow_tcp_forwarding/" "$config_file"
else
    echo "AllowTcpForwarding $allow_tcp_forwarding" >> "$config_file"
fi
'''
    if network_config['configure_warning_banner']:
        script += f'''
warning_banner = /etc/issue.net
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^Banner" "$config_file"; then
    sed -i "s/^Banner.*/Banner $warning_banner/" "$config_file"
else
    echo "Banner $warning_banner" >> "$config_file"
fi
'''
    script += f'''
max_auth_tries = {network_config['max_auth_tries']}
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^MaxAuthTries" "$config_file"; then
    sed -i "s/^MaxAuthTries.*/MaxAuthTries $max_auth_tries/" "$config_file"
else
    echo "MaxAuthTries $max_auth_tries" >> "$config_file"
fi
'''
    if network_config['configure_max_startups']:
        script += f'''
max_startups = 10:30:60
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^MaxStartups" "$config_file"; then
    sed -i "s/^MaxStartups.*/MaxStartups $max_startups/" "$config_file"
else
    echo "MaxStartups $max_startups" >> "$config_file"
fi
'''
    script += f'''
max_sessions = {network_config['max_sessions']}
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^MaxSessions" "$config_file"; then
    sed -i "s/^MaxSessions.*/MaxSessions $max_sessions/" "$config_file"
else
    echo "MaxSessions $max_sessions" >> "$config_file"
fi
'''
    script += f'''
login_grace_time = {network_config['login_grace_time']}
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^LoginGraceTime" "$config_file"; then
    sed -i "s/^LoginGraceTime.*/LoginGraceTime $login_grace_time/" "$config_file"
else
    echo "LoginGraceTime $login_grace_time" >> "$config_file"
fi
'''
    script += f'''
client_alive_interval = {network_config['client_alive_interval']}
client_alive_count_max = {network_config['client_alive_count_max']}
config_file="/etc/ssh/sshd_config"

cp "$config_file" "$config_file.bak"

if grep -q "^ClientAliveInterval" "$config_file"; then
    sed -i "s/^ClientAliveInterval.*/ClientAliveInterval $client_alive_interval/" "$config_file"
else
    echo "ClientAliveInterval $client_alive_interval" >> "$config_file"
fi

if grep -q "^ClientAliveCountMax" "$config_file"; then
    sed -i "s/^ClientAliveCountMax.*/ClientAliveCountMax $client_alive_count_max/" "$config_file"
else
    echo "ClientAliveCountMax $client_alive_count_max" >> "$config_file"
fi
'''
    return script

if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))

    



