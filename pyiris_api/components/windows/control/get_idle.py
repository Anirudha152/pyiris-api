# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from ctypes import Structure, windll, c_uint, sizeof, byref')
        self.config.functions.append('''
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def idle(data):
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    send_all(s,'[+]User has been inactive for : ' + str(millis / 1000.0) + ' seconds')''')
        self.config.logics.append('''
            elif command == "idle":
                idle(data)''')
        self.config.help_menu['idle'] = 'Get amount of time user has not pressed a key or moved mouse/ get the idle time of system'
    elif option == 'info':
        self.log.blank('\nName             : Get Idle component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : ctypes' \
                       '\nCommands         : idle' \
                       '\nDescription      : Get amount of time user has not pressed a key or moved mouse/ get the idle time of system\n')
        return {
                "Name": "Get Idle component",
                "OS": "Windows",
                "Required Modules": "ctypes",
                "Commands": "idle>",
                "Description": "Get amount of time user has not pressed a key or moved mouse/ get the idle time of system"}