# Physical Ports

USBGuard: https://usbguard.github.io/documentation/rule-language.html

## UI

- checkbox: enable/disable usbguard service
  - `systemctl status usbguard`
  - grey out all other controls if disabled
- checkbox: allow all devices
- on load, refresh button: get devices from connected ports and current rules
  - `usbguard generate-policy` + from config file
  - `grep 'via-port'`
  - get ids of each device
     - `grep -oP ' id \K\S+'`
  - get names of each device
     - `grep -oP ' name "\K[^"]+'`
  - get port ids of each device
     - `grep -oP ' via-port "\K[^"]+'`
  <!-- - get name of each ids
     - `lsusb -d <id>`
     - `grep -oP ' ID [0-9a-f]+:[0-9a-f]+ \K.*'` -->
- table(list): display the list of devices
  - checkbox: allowed(true) or blocked(false)
  - device id
  - device name
  - port id
  - checkbox: port-specific rule(true) or global rule(false)
  - delete button
- table(list): display the list of ports (? how to get all port ids)
  - checkbox: allowed(true) or blocked(false)
  - port id

## Config File

```toml
[physical-ports]
enable = true
device-rules = [
    {allow = true, id = "1a2c:4c5e", name = "USB Keyboard"}, # allow only at that port
    {allow = true, id = "04f3:0c00", name = "ELAN:ARM-M4"}
]
port-rules = [
    {allow = false, id = "1-3"} # block all devices at that port
]
```

## Backend

- if not `enable`:
  - `sudo systemctl disable --now usbguard`
  - return
- generate `rules.conf`:
  - if `allow-all`:
     - `allow`
  - else:
     - for each rule: `allow $id name "$name" via-port "$port"`
- install rules:
  - `sudo install -m 0600 -o root -g root rules.conf /etc/usbguard/rules.conf`
  - `sudo systemctl restart usbguard`
  - `sudo systemctl enable usbguard`

