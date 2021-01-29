# API
# done
import pyiris_api.library.commands.scout_interface.disconnect as disconnect
import pyiris_api.library.commands.scout_interface.kill as kill
import pyiris_api.library.commands.scout_interface.more as more
import pyiris_api.library.commands.scout_interface.ping as ping
import pyiris_api.library.commands.scout_interface.rename as rename
import pyiris_api.library.commands.scout_interface.show as show
import pyiris_api.library.commands.scout_interface.sleep as sleep
import pyiris_api.library.modules.decorators as decorators


class Main:
    """The scout functions of pyiris"""
    def __init__(self, pyiris_self):
        self.config = pyiris_self.config
        self.log = pyiris_self.log

    def disconnect_scout(self, scout_id):
        return disconnect.main(self, scout_id)

    def kill_scout(self, scout_id):
        return kill.main(self, scout_id)

    def more_scout(self, to_show):
        return more.main(self, to_show)

    def ping_scout(self, scout_id):
        return ping.main(self, scout_id)

    def rename_scout(self, to_rename, rename_val):
        return rename.main(self, to_rename, rename_val)

    def show(self, to_show):
        return show.main(self, to_show)

    def sleep_scout(self, scout_id, sleep_dur):
        return sleep.main(self, scout_id, sleep_dur)

    def bridge_scout(self, scout_id):
        if str(scout_id) in self.config.scout_database.keys():
            self.config.bridged_to = str(scout_id)
            return {"status": "ok", "message": "Successfully bridged", "data": None}
        else:
            return {"status": "error", "message": "Invalid Scout ID", "data": None}
