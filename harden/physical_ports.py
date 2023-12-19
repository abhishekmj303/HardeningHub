import subprocess
from harden import config_file


def _generate_policy():
    return subprocess.check_output(
        ["usbguard", "generate-policy"]
    ).decode("utf-8")


def get_devices(all_config):
    config = all_config["physical-ports"]
    device_rules = config["device-rules"]
    port_rules = config["port-rules"]
    devices = {device["id"]: device for device in device_rules}
    ports = {port["id"]: port for port in port_rules}
    
    for id in ports:
        ports[id]["name"] = "No Device Connected"

    try:
        policy = _generate_policy().splitlines()
    except:
        return all_config
    
    rules = filter(lambda x: "via-port" in x, policy)
    for rule in rules:
        rule_split = rule.split()
        
        device_id = rule_split[rule_split.index("id") + 1]
        if device_id in devices:
            continue
        device_name = rule_split[rule_split.index("name") + 1].strip('"')
        devices[device_id] = {"id": device_id, "name": device_name, "allow": True}

        port_id = rule_split[rule_split.index("via-port") + 1].strip('"')
        if port_id in ports:
            ports[port_id]["name"] = device_name
        else:
            ports[port_id] = {"id": port_id, "name": device_name, "allow": True}
    
    config.update({"device-rules": list(devices.values()), "port-rules": list(ports.values())})
    return all_config


def get_script(all_config):
    config = all_config["physical-ports"]
    script = ""
    if not config["enable"]:
        return "sudo systemctl disable --now usbguard\n"

    script += "cat > rules.conf << EOF\n"

    for device in config["device-rules"]:
        if not device["allow"]:
            continue
        script += f"allow id {device['id']} name \"{device['name']}\"\n"
    
    for port in config["port-rules"]:
        script += f"allow via-port \"{port['id']}\"\n"

    script += "EOF\n"

    script += "sudo install -m 0600 -o root -g root rules.conf /etc/usbguard/rules.conf\n"
    script += "sudo systemctl restart usbguard\n"
    script += "sudo systemctl enable usbguard\n"

    return script

if __name__ == "__main__":
    print(get_script(config_file.init()))