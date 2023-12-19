from harden import config_file

"""
[service_clients] # Service Clients
remove_nis = true
remove_rsh = true
remove_talk = true
remove_telnet = true
remove_ldap = true
remove_rpc = true
"""
def get_script(config):
    file_systems_config = config["service_clients"]
    # Start with an empty script and build it up

    script = ""
    if file_systems_config['remove_nis']:
        script += """
sudo apt purge nis
"""
    if file_systems_config['remove_rsh']:
        script += """
sudo apt purge rsh-client
"""
    if file_systems_config['remove_talk']:
        script += """
sudo apt purge talk
"""
    if file_systems_config['remove_telnet']:
        script += """
sudo apt purge telnet
"""
    if file_systems_config['remove_ldap']:
        script += """
apt purge ldap-utils
"""
    if file_systems_config['remove_rpc']:
        script += """
apt purge rpcbind
""" 

    return script


if __name__ == "__main__":
    config = config_file.init()
    print(get_script(config))
