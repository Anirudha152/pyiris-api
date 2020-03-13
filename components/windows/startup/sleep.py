# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option, prompt = None):
    if option == 'generate':
        config.import_statements.append('from time import sleep')
        if interface == "GUI":
            prompt = prompt.split(" ")
            if prompt[3] == "1":
                if prompt[5] == "1":
                    sleep_duration = int(prompt[7])
                else:
                    sleep_duration = int(prompt[6])
            else:
                if prompt[4] == "1":
                    sleep_duration = int(prompt[6])
                else:
                    sleep_duration = int(prompt[5])
            print("Sleep duration set to", str(sleep_duration))
        elif interface == "CUI":
            print(config.war + 'Manual intervention required for python_execute component')
            while True:
                try:
                    sleep_duration = input('\x1b[1m\x1b[37m[\x1b[0m\033[92m' +
                                           '\x1b[1m\x1b[31mwindows/startup/sleep\x1b[0m' +
                                           '\x1b[1m\x1b[37m > ]\x1b[0m ' + 'Input duration (in seconds) for scout to sleep for before starting [CTRL-C /ENTER for default sleep of 60 seconds] : ')
                    if not sleep_duration and sleep_duration != 0:
                        print(config.pos + 'Sleep duration set to 60 seconds')
                        sleep_duration = 60
                        break
                    sleep_duration = int(sleep_duration)
                    print(config.pos + 'Sleep duration set to ' + str(sleep_duration) + ' seconds')
                    break
                except ValueError:
                    print(config.neg + 'Input a valid integer')
                except EOFError:
                    try:
                        time.sleep(2)
                    except KeyboardInterrupt:
                        print('\n' + config.pos + 'Sleep duration set to 60 seconds')
                        sleep_duration = 60
                        break
                except KeyboardInterrupt:
                    print('\n' + config.pos + 'Sleep duration set to 60 seconds')
                    sleep_duration = 60
                    break
        config.startup_start.append('sleep(' + str(sleep_duration) + ')')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Sleep startup component",
                "OS": "Windows",
                "Required Modules": "time",
                "Commands": "NIL (Runs at startup)",
                "Description": "Sleeps the scout before running any other processes to avoid and timeout malware detection systems"}
        elif interface == "CUI":
            print('\nName             : Sleep startup component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : time' \
                  '\nCommands         : NIL (Runs at startup)' \
                  '\nDescription      : Sleeps the scout before running any other processes to avoid and timeout malware detection systems')
