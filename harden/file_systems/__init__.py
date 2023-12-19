from harden.file_systems import aide, cramfs, dev_shm, squashfs, tmp, udf

def get_script(config):
    script = ""
    script += aide.get_script(config)
    script += cramfs.get_script(config)
    script += dev_shm.get_script(config)
    script += squashfs.get_script(config)
    script += tmp.get_script(config)
    script += udf.get_script(config)
    return script