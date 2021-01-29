# API
# done
import pyiris_api.library.modules.generator_id_parser as generator_id_parser
from collections import OrderedDict


def unload_enc(self, load_off, loaded_encoders):
    if load_off == 'all':
        loaded_encoders = {}
        self.log.pos('Unloaded all encoders')
        return {"status": "ok", "message": "Unloaded all encoders", "data": {"loaded_encoders": loaded_encoders}}
    elif load_off in list(loaded_encoders.values()):
        found = False
        for key, val in loaded_encoders.items():
            if val == load_off:
                del(loaded_encoders[key])
                self.log.pos('Unloaded : ' + load_off)
                found = True
                break
        if not found:
            raise KeyError
        return {"status": "ok", "message": "Unloaded : " + load_off, "data": {"loaded_encoders": loaded_encoders}}
    else:
        x = loaded_encoders[load_off]
        self.log.pos('Unloaded : ' + loaded_encoders[load_off])
        del (loaded_encoders[load_off])
        return {"status": "ok", "message": "Unloaded : " + x, "data": {"loaded_encoders": loaded_encoders}}


def main(self, command):
    try:
        load_off = command
        load_off = generator_id_parser.main(self, load_off, 'encoders', 'unload')["data"]
        load_off = list(map(str, load_off))
        snapshot = self.config.loaded_encoders
        snapshot_dict = OrderedDict()
        for i in range(len(snapshot)):
            snapshot_dict[str(i)] = snapshot[i]
        for i in load_off:
            self.log.inf('Unloading : ' + i)
            snapshot_dict = unload_enc(self, str(i), snapshot_dict)["data"]["loaded_encoders"]
        self.config.loaded_encoders = list(snapshot_dict.values())
        return {"status": "ok", "message": "Unloaded encoders successfully", "data": {"loaded_encoders": self.config.loaded_encoders}}
    except (KeyError, IndexError, TypeError) as e:
        raise e
        # self.log.err('Please specify a valid encoder to unload')
        # self.config.loaded_encoders = list(snapshot_dict.values())
        # return {"status": "error", "message": 'Please specify a valid encoder to unload or "all" to load all encoders.', "data": None}