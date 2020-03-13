import os
import time
import socket
import threading
import library.modules.config as config

config.main()


def main():
    try:
        confirm_exit = input('\n' + config.pro + 'Are you sure you want to exit[y/n] : ')
        if confirm_exit == 'y':
            print(config.inf + 'User requested shutdown...')
            if config.listener_database:
                print(config.lod + 'Killing all active listeners')
                print(config.inf + 'Sent kill message to all listeners...')
                print(config.inf + 'Waiting for response...')
                config.listener_database = {}
                while threading.active_count() > 1:
                    continue
                print(config.pos + 'Done')
            if config.scout_database:
                print(config.lod + 'Disconnecting all scouts')
                for i in config.scout_database:
                    try:
                        config.scout_database[i][0].send('disconnect'.encode())
                        config.scout_database[i][0].settimeout(5)
                        buffer_out_reply = config.scout_database[i][0].recv(999999999).decode()
                        config.scout_database[i][0].close()
                        print(config.pos + 'Closed connection to scout of ID : ' + i)
                    except (socket.error, socket.timeout):
                        print(config.neg + 'Could not close connection to scout of ID : ' + i)
                        pass
                print(config.pos + 'Done')
            print(config.pos + 'Exiting...')
            os._exit(1)
        else:
            pass
    except EOFError:
        try:
            time.sleep(2)
            quit()
        except KeyboardInterrupt:
            quit()
    except KeyboardInterrupt:
        quit()
