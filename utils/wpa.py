import subprocess
import string
import shlex

WPA_CONF = "/etc/wpa_supplicant/wpa_supplicant.conf"
BEGIN_MARKER = "## Added by smoothie-wifi"
END_MARKER = "## End config by smoothie-wifi"

def _build_config(ssid, psk):
    ret = ["network={"]

    ret.append('ssid="{}"'.format(ssid))
    ret.append('psk="{}"'.format(psk))

    ret.extend(["key_mgmt=WPA-PSK",
                "}"])

    return ret


def _wrap_config(lines):
    return [BEGIN_MARKER] + lines + [END_MARKER]


def _remove_existing(lines):
    ret = []
    keep = True
    for l in lines:
        if BEGIN_MARKER == l:
            keep = False
        elif END_MARKER == l:
            keep = True
        elif keep:
            ret.append(l)

    return ret


def _append_config(existing, ssid, psk):
    if BEGIN_MARKER in existing:
        existing = _remove_existing(existing)

    config = _build_config(ssid, psk)

    return existing + _wrap_config(config) + ['']


def _sanitize(s, string_name):
    """Sanitizes s by throwing an exception"""
    if any(c not in string.printable or c == "\n" or c == "\r" for c in s):
        raise Exception("{} contains non-printable characters or newline!".format(string_name))


def activate_config():
    subprocess.check_call(shlex.split("/sbin/wpa_cli -i wlan0 reconfigure"))


def secure_config():
    subprocess.check_call(shlex.split("/bin/chown root:root {}".format(WPA_CONF)))
    subprocess.check_call(shlex.split("/bin/chmod 400 {}".format(WPA_CONF)))


def add_config(ssid, psk):
    existing = None

    _sanitize(ssid, "SSID/Network Name")
    _sanitize(psk, "Password/Key")

    with open(WPA_CONF) as f:
        existing = [l.strip() for l in f.readlines()]

    new = _append_config(existing, ssid, psk)

    with open(WPA_CONF, "w") as f:
        f.write("\n".join(new))

    secure_config()
    activate_config()


def remove_existing_config():
    existing = None

    with open(WPA_CONF) as f:
        existing = [l.strip() for l in f.readlines()]

    new = _remove_existing(existing)

    with open(WPA_CONF, "w") as f:
        f.write("\n".join(new))

    secure_config()
    activate_config()
