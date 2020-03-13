import socket
import library.modules.config as config
config.main()
interface = config.interface

def main(scout_id):
    try:
        if interface == "GUI":
            config.scout_database[scout_id][0].sendall('g ping'.encode())
        elif interface == "CUI":
            config.scout_database[scout_id][0].sendall('c ping'.encode())
        data = config.scout_database[scout_id][0].recv(999999).decode()
        if interface == "GUI":
            config.app.logger.info("[library/commands/direct_interface/ping] - Message from scout: " + str(data))
        elif interface == "CUI":
            print(data)
        return True
    except socket.error:
        if interface == "GUI":
            config.app.logger.error("[library/commands/direct_interface/ping] - Scout is dead, removing from database...")
        elif interface == "CUI":
            print(config.neg + 'Scout is dead, removing from database...')
        del (config.scout_database[scout_id])
        config.change = True
        return False
