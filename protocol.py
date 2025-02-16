import re
import os
LENGTH_FIELD_SIZE = 4

def check_cmd(data):
    """
    Check for commands defined in protocol, including all parameters.
    """
    legal_cmd = ["DIR", "DELETE", "COPY", "EXECUTE", "TAKE_SCREENSHOT", "SEND_PHOTO", "EXIT"]
    data_split = data.split(" ")
    cmd = data_split[0]
    del data_split[0]
    paths = data_split
    try:
        path1 = paths[0]
    except:
        path1 = ""
    try:
        path2 = paths[1]
    except:
        path2 = ""
    if not cmd in legal_cmd:
        return False
    if len(paths) > 2:
        return False
    if cmd == "DIR" and path1 != "" and path2 == "":
        if os.path.exists(path1):
            return True
        return False
    if cmd == "DELETE" and path1 != "" and path2 == "":
        if os.path.isfile(path1):
            return True
        return False
    if cmd == "COPY" and path1 != "" and path2 != "":
        if os.path.isfile(path1) and os.path.exists(path2):
            return True
        return False
    if cmd == "EXECUTE" and path1 != "" and path2 == "":
        if os.path.isfile(path1):
            return True
        return False
    if cmd == "TAKE_SCREENSHOT" and path1 == "" and path2 == "":
        return True
    if cmd == "SEND_PHOTO" and path1 == "" and path2 == "":
        return True
    if cmd == "EXIT":
        return True
    return False

def create_msg(data):
    """
    Create a valid protocol message, with length field.
    """
    length_filed = len(str(data))
    str_length_filed = str(length_filed)
    while len(str_length_filed) < 4:
        str_length_filed = "0" + str_length_filed
    return str_length_filed + str(data)


def get_msg(my_socket):
    """
    Extract message from protocol, without length field.
    If length field does not include a number, you will get "Error".
    """
    try:
        length_filed = int(my_socket.recv(4).decode())
        msg = ""
        while length_filed > 0:
            msg += my_socket.recv(1024).decode()
            if length_filed < 1024:
                break
            length_filed -= 1024
    except my_socket.error:
        print("*SocketError*")
        return False, "ERROR"
    except ValueError:
        print("*ValueError*")
        return False, "ERROR"
    return True, msg