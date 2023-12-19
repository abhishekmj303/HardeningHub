from harden import config_file, physical_ports, file_systems\
    , process_hardening, apparmor, gdm, time_sync

def generate():
    config = config_file.read()
    script = "#/bin/bash\n\n"
    script += physical_ports.get_script(config)
    script += file_systems.get_script(config)
    script += process_hardening.get_script(config)
    script += apparmor.get_script(config)
    script += gdm.get_script(config)
    script += time_sync.get_script(config)
    return script

def save(file_path: str):
    with open(file_path, "w") as f:
        f.write(generate())

if __name__ == "__main__":
    config_file.init()
    save("script.sh")
    