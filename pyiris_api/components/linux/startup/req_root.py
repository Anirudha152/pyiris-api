# API
# done


def main(self, option, extra_input=None):
    if option == 'generate':
        self.config.import_statements.append('import os')
        self.config.startup.append('req_root_startup()')
        conditions = extra_input
        if 'request_root_message' in conditions:
            if conditions['request_root_message'] == '':
                message = 'ERROR - This file must be run as root to work'
            else:
                message = str(conditions['request_root_message'])
            self.log.pos("Set startup message to \"" + message + "\"")
        self.config.functions.append('''
def req_root_startup():
    if os.getuid() == 0:
        return
    else:
        print ("''' + message + '''")
        exit()
''')
    elif option == 'info':
        self.log.blank('\nName             : Request root startup component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : os' \
                       '\nCommands         : NIL (Runs at startup)' \
                       '\nDescription      : Makes the script request for root before running\n')
        return {
            "Name": "Request root startup component",
            "OS": "Linux",
            "Required Modules": "os",
            "Commands": "NIL (Runs at startup)",
            "Description": "Makes the script request for root before running"
        }