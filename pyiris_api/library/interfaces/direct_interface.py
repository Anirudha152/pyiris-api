# API
# done
import pyiris_api.library.commands.direct_interface.send as send


class Main:
    """The direct functions of pyiris"""

    def __init__(self, pyiris_self):
        self.config = pyiris_self.config
        self.log = pyiris_self.log
        send.check_imports(self)

    def send(self, command):
        return send.main(self, command)

    def get_bridged(self):
        try:
            scout_info = self.config.scout_database[str(self.config.bridged_to)].copy()
            del scout_info['conn_object']
            return {"status": "ok", "message": "", "data": {"scout_info": {self.config.bridged_to: scout_info}}}
        except KeyError:
            return {"status": "error", "message": "Not currently bridged to a scout", "data": None}