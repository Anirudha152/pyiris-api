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
        scout_info = self.config.scout_database[self.config.bridged_to].copy()
        del scout_info[0]
        scout_info.insert(0, self.config.bridged_to)
        return {"status": "ok", "message": "", "data": {"scout_info": scout_info}}