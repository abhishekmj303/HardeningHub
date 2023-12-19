from harden import config_file

"""
remove_avahi = true
remove_cups = true
remove_dhcp = true
remove_ldap = true
remove_nfs = true
remove_ftp = true
remove_http = true
remove_imap_pop3 = true
remove_samba = true
remove_http_proxy = true
remove_snmp = true
remove_nis = true
remove_rsync = true
"""
def get_script(config):
    file_systems_config = config["services"]
    # Start with an empty script and build it up

    script = """"""
    if file_systems_config['remove_avahi']:
        script += """
systemctl stop avahi-daaemon.service
systemctl stop avahi-daemon.socket
sudo apt purge avahi-daemon
"""
    if file_systems_config['remove_cups']:
        script += """
sudo apt purge cups
"""
    if file_systems_config['remove_dhcp']:
        script += """
sudo apt purge isc-dhcp-server
"""
    if file_systems_config['remove_ldap']:
        script += """
sudo apt purge slapd
"""
    if file_systems_config['remove_nfs']:
        script += """
sudo apt purge nfs-kernel-server
"""
    if file_systems_config['remove_ftp']:
        script += """
sudo apt purge vsftpd
"""
    if file_systems_config['remove_http']:
        script += """
sudo apt purge apache2
"""
    if file_systems_config['remove_imap_pop3']:
        script += """
sudo apt purge dovecot-imapd dovecot-pop3d
"""
    if file_systems_config['remove_samba']:
        script += """
sudo apt purge samba
"""
    if file_systems_config['remove_http_proxy']:
        script += """
sudo apt purge squid
"""
    if file_systems_config['remove_snmp']:
        script += """
sudo apt purge snmp
"""
    if file_systems_config['remove_nis']:
        script += """
sudo apt purge nis
"""
    if file_systems_config['remove_rsync']:
        script += """   
sudo apt purge rsync
"""


if __name__ == "__main__":
    config = config_file.read()
    print(get_script(config))
