# API
# done
import pyiris_api.library.modules.check_loaded_components as check_loaded_components


def main(self, command):
    try:
        if self.config.scout_values['Windows'][0] == 'True':
            load_on = str(command)
            if load_on in list(self.config.win_bases.keys()):
                load_on = self.config.win_bases[load_on]
            if load_on in list(self.config.win_bases.values()):
                if load_on == self.config.win_base_to_use:
                    self.log.war("Base already loaded")
                    return {"status": "warning", "message": "Base already loaded", "data": None}
                else:
                    self.config.win_base_to_use = load_on
                    self.log.pos("Replaced the loaded on base with new base : " + load_on)
                    check_loaded_components.main(self)
                    return {"status": "ok", "message": "Replaced the loaded on base with new base : " + load_on, "data": {"loaded_base": load_on}}
            return {"status": "error", "message": "Invalid base ID/Name", "data": None}
        else:
            load_on = str(command)
            if load_on in list(self.config.lin_bases.keys()):
                load_on = self.config.lin_bases[load_on]
            if load_on in list(self.config.lin_bases.values()):
                if load_on == self.config.lin_base_to_use:
                    self.log.war("Base already loaded")
                    return {"status": "warning", "message": "Base already loaded", "data": None}
                else:
                    self.config.lin_base_to_use = load_on
                    self.log.pos("Replaced the loaded on base with new base : " + load_on)
                    check_loaded_components.main(self)
                    return {"status": "ok", "message": "Replaced the loaded on base with new base : " + load_on, "data": {"loaded_base": load_on}}
            return {"status": "error", "message": "Invalid base ID/Name", "data": None}
    except ValueError:
        self.log.err("Generator found no IDs")
        return {"status": "error", "message": "Invalid base ID", "data": None}