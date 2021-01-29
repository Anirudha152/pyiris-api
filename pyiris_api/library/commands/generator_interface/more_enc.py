# API
# done
import pyiris_api.library.modules.generator_id_parser as generator_id_parser


def check_imports(self):
    tmp_enc = list(self.config.encoders.values())
    for i in tmp_enc:
        exec("global " + i.replace('/', '_'), globals())
        exec(f"{i.replace('/', '_')} = __import__('pyiris_api.encoders', globals(), locals(), ['{i.replace('/', '.')}']).{i.replace('/', '.')}", globals())
    self.log.pos('Loaded all encoders info - OK')


def more_enc(self, load_on):
    if load_on in self.config.encoders:
        load_on = self.config.encoders[load_on]
    else:
        if load_on in list(self.config.encoders.values()):
            pass
        else:
            raise KeyError
    info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
    return info


def main(self, comp_str):
    try:
        load_on = comp_str
        if load_on == 'all':
            output = {}
            for i in self.config.encoders.keys(): # this could be config.encoders.values()... need to find out what angus did
                output[i] = more_enc(self, str(i))
        else:
            load_on = generator_id_parser.main(self, load_on, 'encoders', None)["data"]
            load_on = list(map(str, load_on))
            output = {}
            for i in load_on:
                output[i] = more_enc(self, str(i))
        return {"status": "ok", "message": "Retrieved Encoder Info", "data": {"encoder_info": output}}
    except (IndexError, KeyError) as e:
        self.log.err('Please specify a valid encoder to show more info for')
        return {"status": "error", "message": 'Please specify a valid encoder to show more info for', "data": None}


def exec_with_return(code, **kwargs):
    for key, value in kwargs.items():
        exec(key + " = value")
    exec('global exec_return_stuff; exec_return_stuff = %s' % code)
    global exec_return_stuff
    return exec_return_stuff