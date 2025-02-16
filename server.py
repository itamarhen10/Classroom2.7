import glob
import os
import shutil
import subprocess
import pyautogui
import protocol

ADDR = ('0.0.0.0', 8820)
PHOTO_PATH = r'' #img.png

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)
SERVER.listen(1)


def check_client_request(cmd):
    valid = protocol.check_cmd(cmd)
    split_cmd = cmd.split(" ")
    command = split_cmd[0]
    params = split_cmd[1:] if len(split_cmd) > 1 else []
    return valid, command, params


def handle_client_request(command, params):
    if command == "DIR":
        response = ", ".join(glob.glob(params[0] + r"\."))
        return response.encode()

    if command == "DELETE":
        try:
            os.remove(params[0])
            response = "Succeeded"
        except:
            response = "Failed"
        return response.encode()

    if command == "COPY":
        try:
            shutil.copy(params[0], params[1])
            response = "Succeeded"
        except:
            response = "Failed"
        return response.encode()

    if command == "EXECUTE":
        try:
            subprocess.call(params[0])
            response = "Succeeded"
        except:
            response = "Failed"
        return response.encode()

    if command == "TAKE_SCREENSHOT":
        try:
            img = pyautogui.screenshot()
            img.save(PHOTO_PATH)
            response = "Screenshot succeeded"
        except:
            response = "Failed to take screenshot"
        return response.encode()

    if command == "SEND_PHOTO":
        with open(PHOTO_PATH, 'rb') as img:
            response = img.read()
        file_size = len(response)
        return file_size, response


def main():
    print("Waiting for connections...")
    client_socket, client_address = SERVER.accept()
    print(f"Client {client_address} connected.")

    while True:
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if not valid_protocol:
            client_socket.send(protocol.create_msg("Packet not according to protocol").encode())
            continue

        valid_cmd, command, params = check_client_request(cmd)
        if not valid_cmd:
            client_socket.send(protocol.create_msg("Bad command or parameters").encode())
            continue

        if command == "EXIT":
            break

        if command == "SEND_PHOTO":
            size, file_to_send = handle_client_request(command, params)
            client_socket.send(protocol.create_msg(str(size)).encode())
            client_socket.sendall(file_to_send)
        else:
            response = handle_client_request(command, params)
            client_socket.send(protocol.create_msg(response).encode())

    print("Closing connection...")
    client_socket.close()


if __name__ == 'main':
    main()
    SERVER.close()