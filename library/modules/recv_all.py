import socket


def main_recv(sock):
    sock.settimeout(None)
    try:
        data = sock.recv(1000000)
        processed_data = data.decode()
        target_length = int(processed_data.split("|",1)[0])
        data = data[len(str(target_length))+1:]
    except UnicodeDecodeError:
        target_length = int(data.decode(encoding='utf-8', errors='ignore').split("|",1)[0])
        data = data[len(str(target_length))+1:]

    received_data_length = len(data)
    if received_data_length >= target_length:
        try:
            return data.decode()
        except UnicodeDecodeError:
            return data

    sock.settimeout(3)
    while received_data_length < target_length:
        try:
            tmp_data = sock.recv(1000000)
            if not tmp_data:
                raise socket.error
            data += tmp_data
            received_data_length += 1000000
        except (socket.error, socket.timeout):
            break
    try:
        return data.decode()
    except UnicodeDecodeError:
        return data


def main_send(data, sock):
    try:
        sock.sendall((str(len(data)) + "|" + data).encode())
    except TypeError:
        sock.sendall(str(len(data)).encode() + b"|" + data)
