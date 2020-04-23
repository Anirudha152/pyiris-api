import socket
import library.modules.config as config
import library.modules.should_listener_die as should_listener_die
import library.modules.return_random_string as return_random_string
import library.modules.recv_all as recv_all
from datetime import datetime
config.main()
interface = config.interface


def main(host, port, name, reply):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        s.settimeout(2)
        local_copy_of_id = config.incremented_listener_id
        config.listener_database[str(config.incremented_listener_id)] = [host, str(port), name,
                                                                         datetime.now().strftime('%Y-%m-%d %H:%M:%S'), []]
        config.incremented_listener_id += 1
        config.change = True
        if interface == "GUI":
            config.app.logger.info("[library/modules/socket_listener] - Successfully started listener thread at : " + host + ":" + str(port))
        elif interface == "CUI":
            print(config.pos + 'Successfully started listener thread at : ' + host + ':' + str(port))
        config.thread_message = ['pos', 'Successfully started listener thread at : ' + host + ':' + str(port)]
        while True:
            try:
                if should_listener_die.main(str(local_copy_of_id)):
                    if interface == "GUI":
                        config.app.logger.info("[library/modules/socket_listener] - Listener at : " + host + ":" + str(port) + " , received kill message, exiting...")
                    elif interface == "CUI":
                        print('\n' + config.pos + 'Listener at : ' + host + ':' + str(port) + ' , received kill message, exiting...')
                    config.change = True
                    return
                else:
                    try:
                        conn, addr = s.accept()
                    except (socket.timeout, socket.error):
                        continue
                    if config.white_list:
                        if addr[0] not in config.white_list:
                            recv_all.main_send(reply, conn)
                            conn.close()
                            continue
                    elif config.black_list:
                        if addr[0] in config.black_list:
                            recv_all.main_send(reply, conn)
                            conn.close()
                            continue
                    if conn:
                        conn.settimeout(5)
                        await_key = recv_all.main_recv(conn)
                        conn.settimeout(None)
                        if await_key == config.key:
                            if interface == "GUI":
                                config.app.logger.info("[library/modules/socket_listener] - Connection received from scout : " + addr[0] + ":" + str(addr[1]) + " -> " + host + ":" + str(port))
                            elif interface == "CUI":
                                print('\n' + config.pos + 'Connection received from scout : ' + addr[0] + ':' + str(
                                    addr[1]) + ' -> ' + host + ':' + str(port))
                            config.thread_message = ['pos', 'Connection received from scout : ' + addr[0] + ':' + str(
                                addr[1]) + ' -> ' + host + ':' + str(port)]
                            config.scout_database[str(config.incremented_scout_id)] = [conn, addr[0], str(addr[1]),
                                                                                       host + ':' + str(port),
                                                                                       return_random_string.main(5),
                                                                                       datetime.now().strftime(
                                                                                           '%Y-%m-%d %H:%M:%S'),
                                                                                       'Reverse']
                            config.listener_database[str(local_copy_of_id)][4].append(addr[0] + ':' + str(addr[1]))
                            config.incremented_scout_id += 1
                            config.change = True
                        else:
                            recv_all.main_send(reply, conn)
                            conn.close()
                    else:
                        conn.close()
            except socket.error:
                continue
    except Exception as e:
        if interface == "GUI":
            config.app.logger.error("\x1b[1m\x1b[31m[library/modules/socket_listener] - Error in listener thread : " + str(e) + ", killing thread...\x1b[0m")
        elif interface == "CUI":
            print('\n' + config.war + 'Error in listener thread : ' + str(e) + ', killing thread...')
        config.thread_message = ['neg', 'Error in listener thread : ' + str(e) + ', killing thread']
        config.change = True
        try:
            del (config.listener_database[str(local_copy_of_id)])
        except (IndexError, ValueError, UnboundLocalError):
            pass
