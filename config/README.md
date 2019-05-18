# Bluetooth Config

| File                    | Path on raspi                               | Purpose                                                                                                |
| ---                     | ---                                         | ---                                                                                                    |
| bt-agent.service        | /etc/systemd/system/bt-agent.service        | Starts agent to handle authentication                                                                  |
| bt-wifi-manager.service | /etc/systemd/system/bt-wifi-manager.service | Starts wifi manager to handle incoming Bluetooth serial connections                                    |
| bluetooth.service       | /lib/systemd/system/bluetooth.service       | Override bluetooth.service on the raspi for compatibility and to add Serial Port profile for discovery |

# Setup

1. Copy the files to their paths on the raspi
2. Update systemd:

```
sudo systemctl daemon-reload
```

# Start these services

```
sudo systemctl enable bt-agent
sudo systemctl start bt-agent
sudo systemctl enable bt-wifi-manager
sudo systemctl start bt-wifi-manager
```

# Bluetooth configuration

I had to make bluetooth always be discoverable, so that a user can
always connect to it. (User will not have a mouse/keyboard attached to
the raspi)

Uncomment these two in `/etc/bluetooth/main.conf`

```
DiscoverableTimeout = 0
PairableTimeout = 0
```

# Other commands

Set bluetooth to be discoverable

```
sudo hciconfig hci0 piscan
```

Set bluetooth alias

```
sudo hciconfig hci0 name smoothie
```

Change bluetooth name: `/etc/bluetooth/main.conf` uses the hostname,
so edit `/etc/hosts` and `/etc/hostname` to change the hostname to
whatever you prefer.
