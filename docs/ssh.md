# SSH

sshd_config: https://v.gd/b3j7GR

## Config File

```toml
[ssh]
enable = true
port = 22
permit-empty-passwords = false
password-authentication = false
permit-root-login = false
client-alive-interval = 300
client-alive-count-max = 2
allow-users = ["user1", "user2"]
allow-groups = ["group1", "group2"]
x11-forwarding = false
```