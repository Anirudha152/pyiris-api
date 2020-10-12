# GUI + CUI
# done
import library.modules.dynamic_help_generator as dynamic_help_generator
import library.modules.compiler as compiler
import library.modules.config as config
import library.modules.clean_import_data as clean_import_data
import os
from datetime import datetime

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    from json import loads
    import library.modules.log as log
tmp_win = list(config.win_components.values())
tmp_win.append('windows/bases/reverse_tcp_base')
for i in tmp_win:
    exec('import components.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print(config.pos + 'Loaded all windows components into generator - OK')
tmp_lin = list(config.lin_components.values())
tmp_lin.append('linux/bases/reverse_tcp_base')
for i in tmp_lin:
    exec('import components.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print(config.pos + 'Loaded all linux components into generator - OK')
tmp_enc = list(config.encoders.values())
for i in tmp_enc:
    exec('import encoders.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print(config.pos + 'Loaded all encoders into generator - OK')


def main(prompt=None):
    try:
        original = os.getcwd()
        os.chdir(config.started_at)
        comp_list = sorted([i for i in config.loaded_components.values() if not i.endswith('_base')]) # this looks for *_base which is our base network components, appends them to the top  of the list
        for i in config.loaded_components.values():
            if i.endswith('_base'): # this looks for *_base which is our base network components, appends them to the top  of the list
                comp_list.insert(0, i)
        for i in comp_list:
            if interface == "GUI":
                log.log_normal("Loading and executing : " + i)
            elif interface == "CUI":
                print(config.pos + 'Loading and executing : ' + i)
            if interface == "GUI":
                if i == "windows/control/execute_python" or i == "linux/control/execute_python" or i == "windows/startup/sleep" or i == "linux/startup/sleep" or i == "linux/startup/req_root":
                    exec(i.replace('/', '_') + '.main("generate", \'' + prompt.split(' ', 1)[1] + '\')')
                else:
                    exec(i.replace('/', '_') + '.main("generate")')
            elif interface == "CUI":
                exec(i.replace('/', '_') + '.main("generate")')
        if interface == "GUI":
            log.log_normal("Reading contents from temporary written file...")
        elif interface == "CUI":
            print(config.inf + 'Reading contents from temporary written file...')
        with open(os.path.join(config.local_time_dir, 'payload.py'), 'r') as f:
            save_data = f.read()
        config.functions = list(set(config.functions))
        config.import_statements = list(set(config.import_statements))
        config.global_objs = list(set(config.global_objs))
        config.logics = list(set(config.logics))
        # change dir into the "root/datetime" folder for payload generation
        os.chdir(config.local_time_dir)
        with open('payload.py', 'w') as f:
            if interface == "GUI":
                log.log_normal("Writing in imports...")
            elif interface == "CUI":
                print(config.inf + 'Writing in imports...')
            f.write(clean_import_data.main(config.import_statements) + '\n\n')
            if interface == "GUI":
                log.log_normal("Writing in help menu...")
            elif interface == "CUI":
                print(config.inf + 'Writing in help menu...')
            f.write('help_menu = ' + "'''" + dynamic_help_generator.main() + "'''" + '\n')
            if interface == "GUI":
                log.log_normal("Writing in global variables...")
            elif interface == "CUI":
                print(config.inf + 'Writing in global variables...')
            for i in config.global_objs:
                f.write(i + '\n')
            if interface == "GUI":
                log.log_normal("Writing in components...")
            elif interface == "CUI":
                print(config.inf + 'Writing in components...')
            for i in config.functions:
                f.write(i + '\n')
            if interface == "GUI":
                log.log_normal("Writing in startup components...")
            elif interface == "CUI":
                print(config.inf + 'Writing in startup components...')
            for i in config.startup_start:
                f.write(i + '\n')
            for i in config.startup:
                f.write(i + '\n')
            for i in config.startup_end:
                f.write(i + '\n')
            if interface == "GUI":
                log.log_normal("Writing in component list for frontend...")
            elif interface == "CUI":
                print(config.inf + 'Writing in component list for frontend...')
            f.write("comp_list = " + str(comp_list) + "\n")
            if interface == "GUI":
                log.log_normal("Writing in base component...")
            elif interface == "CUI":
                print(config.inf + 'Writing in base component...')
            for i in config.logics:
                save_data = save_data.replace('#Statements#', '#Statements#' + i)
            save_data = save_data.replace('#Statements#', '')
            f.write(save_data)
        if config.loaded_encoders:
            for i in config.loaded_encoders:
                if interface == "GUI":
                    log.log_normal("Encoding with encoder : " + i)
                elif interface == "CUI":
                    print(config.pos + 'Encoding with encoder : ' + i)
                exec(i + '.main("encode")')
        if config.scout_values['Compile'][0] == 'True':
            if interface == "GUI":
                log.log_normal("Compiling scout...")
            elif interface == "CUI":
                print(config.inf + 'Compiling scout...')
            if interface == "GUI":
                output = compiler.main(conditions)
            elif interface == "CUI":
                compiler.main()
        if interface == "GUI":
            log.log_normal('Successfully generated scout python file to : ' + os.path.join(os.getcwd(), 'payload.py'))
        elif interface == "CUI":
            print(config.pos + 'Successfully generated scout python file to : ' + os.path.join(os.getcwd(), 'payload.py'))

        config.functions = []
        config.import_statements = []
        config.global_objs = []
        config.logics = []
        config.startup = []
        config.startup_end = []
        config.startup_start = []
        config.help_menu = {}
        # Bring us back to the original dir the user was in to not disrupt local operations
        os.chdir(original)
        if interface == "GUI":
            try:
                return output
            except:
                return jsonify({"output": "Success", "output_message": "Generation successful", "data": ""})
    except IOError:
        if interface == "GUI":
            log.log_error("File error (Is another process using a file of the same filepath?)")
            return jsonify({"output": "Fail",
                            "output_message": "File error (Is another process using a file of the same filepath?)",
                            "data": ""})
        elif interface == "CUI":
            print(config.neg + 'File error (Is another process using a file of the same filepath?)')
