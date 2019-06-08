import re
import subprocess

from utils.connectivity import is_connected_to_internet
from utils.wifi_list import scan_wifi_aps
from utils.wpa import add_config, remove_existing_config
from utils.state import refresh_chromium


def connected_handler(_):
    if is_connected_to_internet():
        return "Connected!"
    else:
        return "Not connected. Check the network name and password you specified?"


def _quality_to_float(d):
    quality = d["Quality"]
    parts = quality.split("/")
    return float(parts[0]) / float(parts[1])


def networks_handler(_):
    ap_info = sorted(scan_wifi_aps(), key=_quality_to_float, reverse=True)
    key_info = [(ap["ESSID"], ap["Quality"]) for ap in ap_info]
    lines = ["  + {} - strength: {}".format(ssid, quality) for
             (ssid, quality) in key_info]

    return "\n".join(lines)


def _parse_connect_request(input_):
    match = re.search(r"connect\s+<<(.*?)>>\s+<<(.*?)>>", input_)
    if match:
        return match.group(1), match.group(2)


def connect_handler(input_):
    if is_connected_to_internet():
        return "You're already connected!"

    parsed = _parse_connect_request(input_)
    if parsed is None:
        return ("Couldn't find network name and password in your request! "
                "Did you get the format right? Remember << and >>")

    ssid, psk = parsed
    add_config(ssid, psk)

    return "Added {} to wifi, you should be connected now!".format(ssid)


def disconnect_handler(_):
    remove_existing_config()
    return "Removed existing wifi configuration"


def refresh_handler(_):
    refresh_chromium()
    return "smoothie should have been refreshed! Give it some time!"


def restart_handler(_):
    subprocess.Popen(["/sbin/reboot"])
    return "smoothie has started rebooting! Give it some time!"


def shutdown_handler(_):
    subprocess.Popen(["/sbin/poweroff"])
    return "smoothie has started shutting down! Give it some time!"


commands = {
    "connected?": {
        "description": "check if smoothie is connected to the internet",
        "handler": connected_handler,
    },
    "networks": {
        "description": "list wifi networks available",
        "handler": networks_handler,
    },
    "connect": {
        "arguments": ["network_name", "password"],
        "description": "list wifi networks available",
        "handler": connect_handler,
    },
    "disconnect": {
        "description": "disconnect from wifi",
        "handler": disconnect_handler,
    },
    "refresh": {
        "description": "refresh smoothie after connecting to wifi",
        "handler": refresh_handler,
    },
    "restart": {
        "description": "restart (reboot) smoothie",
        "handler": restart_handler,
    },
    "shutdown": {
        "description": "shutdown smoothie before unplugging power!",
        "handler": shutdown_handler,
    },
}
