# API
# done
import socket
import pyiris_api.library.modules.send_all as send_all
import pyiris_api.library.modules.recv_all as recv_all


def main(self, scout_id):
    try:
        if scout_id == 'all':
            error = False
            for i in list(self.config.scout_database.keys()):
                try:
                    self.log.inf('Pinging scout of ID : ' + i)
                    send_all.main(self.config.scout_database[i][0], 'ping')
                    data = recv_all.main(self.config.scout_database[i][0])
                    if not data:
                        raise socket.error
                    self.log.blank(data)
                except socket.error:
                    self.log.err('Scout is dead, removing from database...')
                    error = True
                    try:
                        del (self.config.scout_database[i])
                        self.config.change = True
                    except IndexError:
                        self.log.err('Scout does not exist in database!')
            if error:
                return {"status": "error", "message": "1 or more scouts are dead", "data": {"scout_database": self.config.scout_database}}
            else:
                return {"status": "ok", "message": "All scouts are alive", "data": None}
        else:
            self.log.inf('Pinging scout of ID : ' + scout_id)
            send_all.main(self.config.scout_database[scout_id][0], 'ping')
            data = recv_all.main(self.config.scout_database[scout_id][0])
            self.log.blank(data)
            return {"status": "ok", "message": data, "data": None}
    except (IndexError, KeyError):
        self.log.err('Please enter a valid scout ID')
        return {"status": "error", "message": "Please enter a valid scout ID", "data": None}
    except socket.error:
        try:
            self.log.err('Scout is dead, removing from database...')
            del (self.config.scout_database[scout_id])
            self.config.change = True
        except IndexError:
            self.log.err('Scout does not exist in database!')
        return {"status": "error", "message": "Scout is already dead", "data": None}
