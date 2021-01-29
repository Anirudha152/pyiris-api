# API
# done
# Version 2.0.0

import pyiris_api.library.modules.config_initialiser as config_initialiser
import pyiris_api.library.interfaces.global_interface as global_interface
import pyiris_api.library.interfaces.home_interface as home_interface
import pyiris_api.library.interfaces.generator_interface as generator_interface
import pyiris_api.library.interfaces.listener_interface as listener_interface
import pyiris_api.library.interfaces.scout_interface as scout_interface
import pyiris_api.library.interfaces.direct_interface as direct_interface
import pyiris_api.library.modules.bootstrap as bootstrap
import pyiris_api.library.modules.log as log


class Main:
    def __init__(self, log_handler=None, **kwargs):
        config_initialiser.main(self, **kwargs)
        if not log_handler:
            log_handler = log.Main
        self.log = log_handler(self)
        output = bootstrap.main(self)
        if output["status"] == "error":
            quit()
        self.global_functions = global_interface.Main(self)
        self.home = home_interface.Main(self)
        self.generator = generator_interface.Main(self)
        self.listener = listener_interface.Main(self)
        self.direct = direct_interface.Main(self)
        self.scout = scout_interface.Main(self)
