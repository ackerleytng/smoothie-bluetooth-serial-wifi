#!/usr/bin/env python3

import select
import queue

from bluetooth import (
    BluetoothSocket,
    PORT_ANY,
    BluetoothError
)

from commands import commands


def build_help(command, meta):
    if "arguments" in meta:
        args = " " + " ".join(["<<{}>>".format(a) for a in meta["arguments"]])
    else:
        args = ""
    description = meta["description"]

    return "  + {}{}: {}".format(command, args, description)


def help_message():
    return "\n".join(["Commands:"] + [build_help(k, v) for k, v in commands.items()])


def handle_input(input_):
    input_ = input_.strip()
    if not input_:
        # input is blank
        return help_message()

    command = input_.split()[0]
    meta = commands.get(command, None)
    if meta is None:
        return help_message()
    else:
        return meta["handler"](input_)


def send(connection, string):
    connection.send((string + "\n").encode())


def main():
    server = BluetoothSocket()
    server.bind(("", PORT_ANY))
    server.listen(1)

    inputs = [server]
    outputs = []
    message_queues = {}

    port = server.getsockname()[1]

    print("Waiting for connection on RFCOMM channel {}".format(port))

    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)

        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                print("Accepted connection from {}".format(client_address))
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = queue.Queue()
                send(connection, "Welcome!")
                send(connection, help_message())
            else:
                data = None
                try:
                    data = s.recv(1024).decode().rstrip()
                except BluetoothError as e:
                    # pybluez is implemented in an unpythonic way, hence this hackiness
                    # 104: Connection reset by peer
                    if not str(e).startswith("(104"):
                        raise e

                    print("Client disconnected")

                if data:
                    message_queues[s].put(handle_input(data))
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    if s in inputs:
                        inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else:
                send(s, next_msg)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


if __name__ == "__main__":
    main()
