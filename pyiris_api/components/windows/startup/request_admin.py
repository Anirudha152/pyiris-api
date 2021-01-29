# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import ctypes')
        self.config.import_statements.append('import sys')
        self.config.import_statements.append('import os')
        self.config.startup.append('req_admin_startup()')
        self.config.functions.append('''
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def req_admin_startup():
    if is_admin():
        return
    else:
        ctypes.windll.shell32.ShellExecuteW(None, u"runas", sys.executable, __file__, None, 1)
        os._exit(1)
''')
    elif option == 'info':
        self.log.blank('\nName             : Request admin startup component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : ctypes, sys' \
                       '\nCommands         : NIL (Runs at startup)' \
                       '\nDescription      : Makes the script request for admin before running\n')
        return {
            "Name": "Request admin startup component",
            "OS": "Windows",
            "Required Modules": "ctypes, sys",
            "Commands": "NIL (Runs at startup)",
            "Description": "Makes the script request for admin before running"}