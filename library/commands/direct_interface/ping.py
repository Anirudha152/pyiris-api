# GUI + CUI
# done
import socket
import library.modules.config as config
import library.modules.send_all as send_all
import library.modules.recv_all as recv_all

config.main()
interface = config.interface
if interface == "GUI":
    import library.modules.log as log


def main(scout_id):
    try:
        if interface == "GUI":
            send_all.main(config.scout_database[scout_id][0], 'g ping')
        elif interface == "CUI":
            send_all.main(config.scout_database[scout_id][0], 'c ping')
        data = recv_all.main(config.scout_database[scout_id][0])
        if interface == "GUI":
            log.log_normal("Message from scout: " + str(data))
        elif interface == "CUI":
            print(data)
        return True
    except socket.error:
        if interface == "GUI":
            log.log_error("Scout is dead, removing from database...")
            config.change = True
        elif interface == "CUI":
            print(config.neg + 'Scout is dead, removing from database...')
        del (config.scout_database[scout_id])
        return False
