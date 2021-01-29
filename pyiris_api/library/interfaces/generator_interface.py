# API
# done
import pyiris_api.library.commands.generator_interface.load_com as load_com
import pyiris_api.library.commands.generator_interface.load_enc as load_enc
import pyiris_api.library.commands.generator_interface.more_com as more_com
import pyiris_api.library.commands.generator_interface.more_enc as more_enc
import pyiris_api.library.commands.generator_interface.reset as reset
import pyiris_api.library.commands.generator_interface.set as set
import pyiris_api.library.commands.generator_interface.show as show
import pyiris_api.library.commands.generator_interface.unload_com as unload_com
import pyiris_api.library.commands.generator_interface.unload_enc as unload_enc
import pyiris_api.library.commands.generator_interface.generate as generate
import pyiris_api.library.modules.decorators as decorators


class Main:
    """The generator functions of pyiris"""

    def __init__(self, pyiris_self):
        self.config = pyiris_self.config
        self.log = pyiris_self.log
        more_com.check_imports(self)
        more_enc.check_imports(self)
        generate.check_imports(self)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def load_component(self, component_str):
        return load_com.main(self, component_str)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def load_encoder(self, encoder_str):
        return load_enc.main(self, encoder_str)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def component_info(self, component_str):
        return more_com.main(self, component_str)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def encoder_info(self, encoder_str):
        return more_enc.main(self, encoder_str)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def reset_scout_values(self, to_reset):
        return reset.main(self, to_reset)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def set_scout_values(self, to_set, set_val):
        return set.main(self, to_set, set_val)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def show(self, to_show):
        return show.main(self, to_show)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def unload_component(self, component_str):
        return unload_com.main(self, component_str)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def unload_encoder(self, encoder_str):
        return unload_enc.main(self, encoder_str)

    @decorators.run_generator_append
    @decorators.reset_bridged
    def generate(self, generator_settings=None):
        return generate.main(self, generator_settings)
