import time
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify

def main():
    if interface == "GUI":
        pass
    elif interface == "CUI":
        print(config.war + 'You are currently in the python executor scripter, script a chain of python instructions to run, enter for a newline, CTRL-C to finish ' \
                     '\n(only works if python execute component is loaded)')
        try:
            command = ''
            while True:
                line = '\n' + input('Python Executor Scripter >>> ')
                command += line
        except EOFError:
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                print()
                '\n' + config.pos + 'Done'
                return command
        except KeyboardInterrupt:
            print()
            '\n' + config.pos + 'Done'
            print(command)
            return command
