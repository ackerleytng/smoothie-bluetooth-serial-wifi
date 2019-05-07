import subprocess
import re

def do_iwlist_scan():
    p = subprocess.Popen(["/sbin/iwlist", "wlan0", "scan"], stdout=subprocess.PIPE)

    # The first line is just some meta info
    return p.communicate()[0].decode().splitlines()[1:]


def split_list(l, pred):
    ret = []
    current = None
    for e in l:
        if pred(e):
            ret.append(current)
            current = [e]
        else:
            current.append(e)

    ret.append(current)

    return [e for e in ret if e and len(e) > 0]


def parse_network(lines):
    data = {}

    for l in lines:
        # Stuff to ignore
        if ("Mb/s;" in l or
            "Unknown:" in l or
            "Extra:" in l):
            continue
        elif l.startswith("Cell"):
            parts = re.sub(r"Cell \d+ -\s*", "", l).split(": ", 1)
            data.update(dict([parts]))
        elif "Quality=" in l:
            parts = [p.strip().split("=") for p in l.split("  ")]
            data.update(dict(parts))
        elif ":" in l:
            parts = [p.strip() for p in l.split(":", 1)]
            data.update(dict([parts]))

    if data["ESSID"]:
        # Because iwlist surrounds ESSID with double quotes
        data["ESSID"] = data["ESSID"].strip('"').rstrip('"')

    return data


def scan_wifi_aps():
    lines = [l.strip() for l in do_iwlist_scan()]
    networks = split_list(lines, lambda l: l.startswith("Cell"))
    return [parse_network(n) for n in networks]

