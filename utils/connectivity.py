import socket

def can_connect(addr):
    try:
        socket.create_connection((addr, 53), 0.5)
        return True
    except socket.error:
        return False
    except socket.timeout:
        return False


def is_connected_to_internet():
    reliable_addresses = [
        "8.8.8.8",
        "1.1.1.1",
    ]
    return any(can_connect(a) for a in reliable_addresses)
