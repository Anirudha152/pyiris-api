# API
# done
import pyiris_api.library.modules.sort_dictionary_by_int_val as sort_dictionary_by_int_val
import collections


def main(self):
    if self.config.scout_values['Windows'][0] == 'True':
        self.config.loaded_components['base'] = self.config.win_base_to_use
        self.config.loaded_components = sort_dictionary_by_int_val.main(self.config.loaded_components)
        for i in self.config.loaded_components.values():
            if i.startswith('linux/'):
                self.config.loaded_components = collections.OrderedDict()
                self.config.loaded_components['base'] = self.config.win_base_to_use
                return
    else:
        self.config.loaded_components['base'] = self.config.lin_base_to_use
        self.config.loaded_components = sort_dictionary_by_int_val.main(self.config.loaded_components)
        for i in self.config.loaded_components.values():
            if i.startswith('windows/'):
                self.config.loaded_components = collections.OrderedDict()
                self.config.loaded_components['base'] = self.config.lin_base_to_use
                return
