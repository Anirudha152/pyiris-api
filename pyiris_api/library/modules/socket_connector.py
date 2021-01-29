# API
# done
import pyiris_api.library.modules.return_random_string as return_random_string
import pyiris_api.library.modules.recv_all as recv_all
import socket
from datetime import datetime


def main(self, host, port):
    try:
        host = str(host)
        port = int(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        self.log.pos('Established a TCP connection to ' + host + ':' + str(port))
        if self.config.white_list:
            if host not in self.config.white_list:
                s.close()
                self.log.err("Connection aborted because " + str(host) + " is not in whitelist")
                return {"status": "error", "message": "Connection aborted because " + str(host) + " is not in whitelist", "data": None}
        elif self.config.black_list:
            if host in self.config.black_list:
                s.close()
                self.log.err("Connection aborted because " + str(host) + " is in blacklist")
                return {"status": "error", "message": "Connection aborted because " + str(host) + " is in blacklist", "data": None}
        try:
            await_key = recv_all.main(s, 5)
        except (socket.timeout, socket.error):
            self.log.err("Established connection to " + host + ":" + str(port) + " but no data received!")
            return {"status": "error", "message": "Established connection to " + host + ":" + str(port) + " but no data received!", "data": None}
        s.settimeout(None)
        if await_key == self.config.key:
            self.log.pos('Key from scout matches, connection is allowed')
            self.config.scout_database[str(self.config.incremented_scout_id)] = [s, host, str(port),
                                                                       host + ':' + str(port),
                                                                       return_random_string.main(5),
                                                                       datetime.now().strftime(
                                                                           '%Y-%m-%d %H:%M:%S'),
                                                                       'Bind']
            self.log.inf('Entry added to database')
            self.config.thread_message = "Connection Established to " + str(host) + ":" + str(port)
            self.config.change = True
            self.config.incremented_scout_id += 1
            return {"status": "ok", "message": "Connection Established to " + str(host) + ":" + str(port), "data": {"scout_database": {i: [self.config.scout_database[i][1], self.config. scout_database[i][2], self.config.scout_database[i][3], self.config.scout_database[i][4], self.config.scout_database[i][5], self.config.scout_database[i][6]] for i in self.config.scout_database.keys()}}}
        else:
            self.log.err("Invalid key was supplied from scout, denying connection...")
            s.close()
            return {"status": "error", "message": "Invalid key was supplied from scout, denying connection...", "data": None}
    except (socket.timeout, socket.error):
        self.log.err("Unable to establish bind TCP connection to " + host + ":" + str(port))
        return {"status": "error", "message": "Unable to establish bind TCP connection to " + host + ":" + str(port), "data": None}
    except (IndexError, ValueError):
        self.log.err("Please specify a valid hostname and port number")
        return {"status": "error", "message": "Please specify a valid hostname and port number", "data": None}