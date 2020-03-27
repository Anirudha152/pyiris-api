import socket
import library.modules.config as config
import library.modules.recv_all as recv_all
config.main()
interface = config.interface

def main(scout_id):
    try:
        if interface == "GUI":
            recv_all.main_send("g ping", config.scout_database[scout_id][0])
        elif interface == "CUI":
            recv_all.main_send("c ping", config.scout_database[scout_id][0])
        data = recv_all.main_recv(config.scout_database[scout_id][0])
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
