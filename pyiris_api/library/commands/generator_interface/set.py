# API
# done
import pyiris_api.library.modules.check_loaded_components as check_loaded_components


def main(self, key, val):
    try:
        self.config.scout_values[key][0] = str(val)
        self.log.pos('Set "' + str(key) + '" to "' + str(val) + '"')
        check_loaded_components.main(self)
        return {"status": "ok", "message": 'Set "' + str(key) + '" to "' + str(val) + '"', "data": {"scout_values": self.config.scout_values}}
    except (IndexError, KeyError):
        self.log.err('Please specify a valid option and value')
        return {"status": "error", "message": 'Please specify a valid option and value', "data": None}