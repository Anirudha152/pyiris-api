# API
# done
import pyiris_api.library.modules.generator_id_parser as generator_id_parser


def check_imports(self):
    global tmp_win
    tmp_win = list(self.config.win_bases.values())
    for i in tmp_win:
        exec("global " + i.replace('/', '_'), globals())
        exec(f"{i.replace('/', '_')} = __import__('pyiris_api.components', globals(), locals(), ['{i.replace('/', '.')}']).{i.replace('/', '.')}", globals())
    self.log.pos('Loaded all windows bases info - OK')
    global tmp_lin
    tmp_lin = list(self.config.lin_bases.values())
    for i in tmp_lin:
        exec("global " + i.replace('/', '_'), globals())
        exec(f"{i.replace('/', '_')} = __import__('pyiris_api.components', globals(), locals(), ['{i.replace('/', '.')}']).{i.replace('/', '.')}", globals())
    self.log.pos('Loaded all linux bases info - OK')


def more_base(self, load_on):
    if self.config.scout_values['Windows'][0] == 'True':
        sample_space = list(set(tmp_win))
        if load_on in sample_space:
            info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
        else:
            load_on = self.config.win_bases[load_on]
            info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
    else:
        sample_space = list(set(tmp_lin))
        if load_on in sample_space:
            info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
        else:
            load_on = self.config.lin_bases[load_on]
            info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
    return info


def main(self, base_str):
    try:
        load_on = base_str

        info = {}
        load_on = generator_id_parser.main(self, load_on, 'bases', None)["data"]
        load_on = list(map(str, load_on))
        for i in load_on:
            info[i] = more_base(self, str(i))
        return {"status": "ok", "message": "Retrieved Base Info", "data": {"base_info": info}}
    except (IndexError, KeyError):
        self.log.err('Please specify a valid base to show more info for')
        return {"status": "error", "message": 'Please specify a valid base to show more info for', "data": None}


def exec_with_return(code, **kwargs):
    for key, value in kwargs.items():
        exec(key + " = value")
    exec('global exec_return_stuff; exec_return_stuff = %s' % code)
    global exec_return_stuff
    return exec_return_stuff
