# API
# done
import pyiris_api.library.modules.generator_id_parser as generator_id_parser


def load_enc(self, load_on):
    if load_on in self.config.encoders:
        load_on = self.config.encoders[load_on]
    else:
        if load_on in list(self.config.encoders.values()):
            pass
        else:
            raise KeyError
    self.log.pos('Loaded : ' + load_on)
    self.config.loaded_encoders.append(load_on)


def main(self, command):
    try:
        load_on = command
        load_on = generator_id_parser.main(self, load_on, 'encoders', 'load')["data"]
        load_on = list(map(str, load_on))
        for i in load_on:
            self.log.inf('Loading : ' + i)
            load_enc(self, str(i))
        return {"status": "ok", "message": "Loaded encoders successfully", "data": {"loaded_encoders": self.config.loaded_encoders}}
    except (KeyError, IndexError) as e:
        self.log.err('Please specify a valid encoder to load')
        return {"status": "error", "message": "Please specify a valid encoder to load", "data": None}
