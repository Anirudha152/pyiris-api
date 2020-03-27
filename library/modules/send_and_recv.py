import library.modules.config as config
import library.modules.recv_all as recv_all
config.main()
interface = config.interface


def main(data, scout_id):
    recv_all.main_send(data, config.scout_database[scout_id][0])
    data = recv_all.main_recv(config.scout_database[scout_id][0])
    return data
