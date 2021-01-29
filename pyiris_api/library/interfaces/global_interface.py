# API
# done
import pyiris_api.library.commands.global_interface.clear as clear
import pyiris_api.library.commands.global_interface.help as help
import pyiris_api.library.commands.global_interface.local as local
import pyiris_api.library.commands.global_interface.python as python
import pyiris_api.library.commands.global_interface.quit as quit


class Main:
    """The global functions of pyiris"""

    def __init__(self, pyiris_self):
        self.config = pyiris_self.config
        self.log = pyiris_self.log

    def clear(self):
        clear.main()

    def help(self, interface, command):
        help.main(self, interface, command)

    def local(self, prompt):
        local.main(self, prompt)

    def python(self):
        python.main(self)

    def quit(self):
        quit.main(self)
