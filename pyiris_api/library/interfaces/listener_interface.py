# API
#
import pyiris_api.library.commands.listener_interface.kill as kill
import pyiris_api.library.commands.listener_interface.more as more
import pyiris_api.library.commands.listener_interface.rename as rename
import pyiris_api.library.commands.listener_interface.reset as reset
import pyiris_api.library.commands.listener_interface.run as run
import pyiris_api.library.commands.listener_interface.set as set
import pyiris_api.library.commands.listener_interface.show as show
import pyiris_api.library.modules.socket_connector as socket_connector
import pyiris_api.library.modules.decorators as decorators


class Main:
    """The listener functions of pyiris"""
    def __init__(self, pyiris_self):
        self.config = pyiris_self.config
        self.log = pyiris_self.log

    @decorators.reset_bridged
    def kill_listener(self, to_kill):
        return kill.main(self, to_kill)

    @decorators.reset_bridged
    def more_listener(self, to_show):
        return more.main(self, to_show)

    @decorators.reset_bridged
    def rename_listener(self, to_rename, rename_val):
        return rename.main(self, to_rename, rename_val)

    @decorators.reset_bridged
    def reset_listener_values(self, to_reset):
        return reset.main(self, to_reset)

    @decorators.reset_bridged
    def run_listener(self):
        return run.main(self)

    @decorators.reset_bridged
    def set_listener_values(self, to_set, set_val):
        return set.main(self, to_set, set_val)

    @decorators.reset_bridged
    def show(self, to_show):
        return show.main(self, to_show)

    @decorators.reset_bridged
    def bind(self, host, port):
        return socket_connector.main(self, host, port)