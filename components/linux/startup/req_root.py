# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface
if interface == "GUI":
    from json import loads
    import library.modules.log as log


def main(option, prompt=None):
    if option == 'generate':
        config.import_statements.append('import os')
        config.startup.append('req_root_startup()')
        if interface == "GUI":
            conditions = loads(prompt)
            if (conditions['request_root_message'] == ''):
                message = 'ERROR - This file must be run as root to work'
            else:
                message = str(conditions['request_root_message'])
            log.log_normal("Set startup message to \"" + message + "\"")
        elif interface == "CUI":
            print(config.war + 'Manual intervention required for req_root startup component')
            message = input('\x1b[1m\x1b[37m[\x1b[0m\033[92m' +
                            '\x1b[1m\x1b[31mlinux/startup/req_root\x1b[0m' +
                            '\x1b[1m\x1b[37m > ]\x1b[0m ' + 'Social engineering message to display to the user to request for root [Enter for default message] : ')
            if not message:
                message = 'ERROR - This file must be run as root to work'
        config.functions.append('''
def req_root_startup():
    if os.getuid() == 0:
        return
    else:
        print ("''' + message + '''")
        exit()
''')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Request root startup component",
                "OS": "Linux",
                "Required Modules": "os",
                "Commands": "NIL (Runs at startup)",
                "Description": "Makes the script request for root before running"
            }
        elif interface == "CUI":
            print('\nName             : Request root startup component' \
                  '\nOS               : Linux' \
                  '\nRequired Modules : os' \
                  '\nCommands         : NIL (Runs at startup)' \
                  '\nDescription      : Makes the script request for root before running\n')