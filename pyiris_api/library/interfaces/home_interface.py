# API
# done
import pyiris_api.library.commands.home_interface.set as set
import pyiris_api.library.commands.home_interface.add as add
import pyiris_api.library.commands.home_interface.regen as regen
import pyiris_api.library.commands.home_interface.reset as reset
import pyiris_api.library.commands.home_interface.rm as rm
import pyiris_api.library.commands.home_interface.show as show
import pyiris_api.library.modules.decorators as decorators


class Main:
    """The home functions of pyiris"""

    def __init__(self, pyiris_self):
        self.config = pyiris_self.config
        self.log = pyiris_self.log

    @decorators.reset_bridged
    def set_list(self, list_type, to_set):
        return set.main(self, list_type, to_set)

    @decorators.reset_bridged
    def add_to_list(self, list_type, hostname):
        return add.main(self, list_type=list_type, hostname=hostname)

    @decorators.reset_bridged
    def regen_key(self, key=None):
        return regen.main(self, key)

    @decorators.reset_bridged
    def reset_list(self, list_type):
        return reset.main(self, list_type)

    @decorators.reset_bridged
    def remove_list(self, list_type, hostname):
        return rm.main(self, list_type, hostname)

    @decorators.reset_bridged
    def show(self, list_type):
        return show.main(self, list_type)
