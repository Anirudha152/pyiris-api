# API
# done
import collections
import pyiris_api.library.modules.key_from_val as key_from_val
import pyiris_api.library.modules.generator_id_parser as generator_id_parser


def unload_com(self, load_off):
    if load_off == 'all':
        if self.config.scout_values['Windows'][0] == 'True':
            self.config.loaded_components = collections.OrderedDict()
            self.config.loaded_components['base'] = self.config.win_base_to_use
            self.log.pos("Unloaded all loaded windows components")
            return {"status": "ok", "message": "Unloaded all loaded windows components", "data": None}
        else:
            self.config.loaded_components = collections.OrderedDict()
            self.config.loaded_components['base'] = self.config.lin_base_to_use
            self.log.pos("Unloaded all loaded linux components")
            return {"status": "ok", "message": "Unloaded all loaded linux components", "data": None}
    else:
        if load_off == 'base' or key_from_val.main(self.config.loaded_components, load_off) == 'base':
            self.log.war("Do not unload base components, loading another base component will automatically replace the already loaded base component as there can only be one base component")
            raise KeyError
        try:
            name = self.config.loaded_components[load_off]
            del (self.config.loaded_components[load_off])
            self.log.pos("Unloaded : " + name)
            return {"status": "ok", "message": "Unloaded : " + name, "data": None}
        except KeyError:
            del (self.config.loaded_components[key_from_val.main(self.config.loaded_components, load_off)])
            self.log.pos("Unloaded : " + load_off)
            return {"status": "ok", "message": "Unloaded : " + load_off, "data": None}


def main(self, command):
    try:
        load_off = command
        load_off = generator_id_parser.main(self, load_off, 'components', 'unload')["data"]
        load_off = list(map(str, load_off))
        for i in load_off:
            self.log.inf("Unloading : " + str(i))
            unload_com(self, str(i))
        return {"status": "ok", "message": "Unloaded components successfully", "data": {"loaded_components": self.config.loaded_components}}
    except (KeyError, IndexError):
        self.log.err('Please specify a valid component to unload or "all" to load all components. \x1b[1m\x1b[31mNote : "base" component cannot be unloaded\x1b[0m')
        return {"status": "error", "message": 'Please specify a valid component to unload or "all" to load all components. \x1b[1m\x1b[31mNote : "base" component cannot be unloaded\x1b[0m', "data": None}
