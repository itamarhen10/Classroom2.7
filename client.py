import socket
import sys
from email.quoprimime import decode

import protocol
from PIL import Image

IP = '127.0.0.1'
SAVED_PHOTO_LOCATION = r'' #received image here


def handle_server_response(my_socket, cmd):
    completed, data = protocol.get_msg(my_socket)
    if not completed:
        print("Error. Didn't get message from server.")
        return
    if cmd != "SEND_PHOTO" and cmd != "EXIT":
        print(data[1:].replace("'", ''))
        return
    if cmd == "SEND_PHOTO":
        file_size = int(data)
        bytes_received = 0
        photo = b""
        while bytes_received < file_size:
            chunk = my_socket.recv(min(file_size - bytes_received, 1024))
            if not chunk:
                break
            photo += chunk
            bytes_received += len(chunk)
        with open(SAVED_PHOTO_LOCATION, 'wb') as img:
            img.write(photo)
        print(f"Photo saved at {SAVED_PHOTO_LOCATION}")
        image = Image.open(SAVED_PHOTO_LOCATION)
        image.show()

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, 8820))
    print('Welcome to RemoteControl by Itamar Hen. You may use any of the following:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR <path>\nDELETE <file>\nCOPY <src> <dst>\nEXECUTE <file>\nEXIT')
    while True:
        cmd = input("Please enter a command:\n")
        if protocol.check_cmd(cmd):

            packet = protocol.create_msg(cmd)
            my_socket.send(packet.encode())
            if cmd == "EXIT":
                break
            handle_server_response(my_socket, cmd)
        else:
            print("Invalid command or missing parameters...")
    my_socket.close()

if __name__ == 'main':
    main()