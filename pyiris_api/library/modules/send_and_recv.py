# API
# done
import pyiris_api.library.modules.recv_all as recv_all
import pyiris_api.library.modules.send_all as send_all


def main(self, data, scout_id):
    send_all.main(self.config.scout_database[scout_id][0], data)
    data = recv_all.main(self.config.scout_database[scout_id][0])
    return data
