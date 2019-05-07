import subprocess
import re

def do_iwconfig():
    p = subprocess.Popen(["/sbin/iwconfig", "wlan0"], stdout=subprocess.PIPE)

    # The first line is just some meta info
    return p.communicate()[0].decode().splitlines()


def parse_network(lines):
    data = {}

    for l in lines:
        if ":" in l:
            parts = [p.strip() for p in l.split(":", 1)]
            data.update(dict([parts]))

    if data["ESSID"]:
        # Because iwlist surrounds ESSID with double quotes
        data["ESSID"] = data["ESSID"].strip('"').rstrip('"')

    return data


def parse_iwconfig():
    lines = [l.strip().replace("=", ":") for l in do_iwconfig()]
    lines = [e.strip() for l in lines for e in l.split("  ")]
    lines = [l for l in lines if len(l) > 0]
    data = parse_network(lines)
    return data


def parse_iwconfig_selected():
    data = parse_iwconfig()
    return { k: data[k] for k in ["ESSID", "Link Quality", "Frequency"] }
