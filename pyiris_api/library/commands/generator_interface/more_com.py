# API
# done
import pyiris_api.library.modules.generator_id_parser as generator_id_parser


def check_imports(self):
    global tmp_win
    tmp_win = list(self.config.win_components.values())
    for i in tmp_win:
        exec("global " + i.replace('/', '_'), globals())
        exec(f"{i.replace('/', '_')} = __import__('pyiris_api.components', globals(), locals(), ['{i.replace('/', '.')}']).{i.replace('/', '.')}", globals())
    self.log.pos('Loaded all windows components info - OK')
    global tmp_lin
    tmp_lin = list(self.config.lin_components.values())
    for i in tmp_lin:
        exec("global " + i.replace('/', '_'), globals())
        exec(f"{i.replace('/', '_')} = __import__('pyiris_api.components', globals(), locals(), ['{i.replace('/', '.')}']).{i.replace('/', '.')}", globals())
    self.log.pos('Loaded all linux components info - OK')


def more_com(self, load_on):
    if self.config.scout_values['Windows'][0] == 'True':
        sample_space = list(set(tmp_win + list(self.config.loaded_components.values())))
        if load_on in sample_space:
            info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
        else:
            load_on = dict(list(self.config.win_components.items()) + list(self.config.loaded_components.items()))[load_on]
            info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
    else:
        sample_space = list(set(tmp_lin + list(self.config.loaded_components.values())))
        if load_on in sample_space:
            info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
        else:
            load_on = dict(list(self.config.lin_components.items()) + list(self.config.loaded_components.items()))[load_on]
            info = exec_with_return(load_on.replace('/', '_') + '.main(self, "info")', self=self)
    return info


def main(self, comp_str):
    try:
        load_on = comp_str
        if load_on == 'all':
            info = {}
            if self.config.scout_values['Windows'][0] == 'True':
                sample_space = list(set(tmp_win + list(self.config.loaded_components.values())))
            else:
                sample_space = list(set(tmp_lin + list(self.config.loaded_components.values())))
            sample_space.sort()
            for idx, i in enumerate(sample_space):
                if i in sample_space:
                    info[idx] = exec_with_return(i.replace('/', '_') + '.main(self, "info")', self=self)
                else:
                    i = dict(list(self.config.win_components.items()) + list(self.config.loaded_components.items()))[i]
                    info[idx] = exec_with_return(i.replace('/', '_') + '.main(self, "info")', self=self)
        else:
            info = {}
            load_on = generator_id_parser.main(self, load_on, 'components', None)["data"]
            load_on = list(map(str, load_on))
            for i in load_on:
                info[i] = more_com(self, str(i))
        return {"status": "ok", "message": "Retrieved Component Info", "data": {"component_info": info}}
    except (IndexError, KeyError):
        self.log.err('Please specify a valid component to show more info for')
        return {"status": "error", "message": 'Please specify a valid component to show more info for', "data": None}


def exec_with_return(code, **kwargs):
    for key, value in kwargs.items():
        exec(key + " = value")
    exec('global exec_return_stuff; exec_return_stuff = %s' % code)
    global exec_return_stuff
    return exec_return_stuff