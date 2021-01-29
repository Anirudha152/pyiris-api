# API
# done
from base64 import b64encode


def main(self, option):
    if option == 'encode':
        try:
            imported_modules = ['from base64 import b64decode']
            with open("payload.py", 'r') as f:
                data = f.read().replace(';', '\n')
            source = data.split('\n')
            for i in source:
                if 'import' in i and i != 'from base64 import b64decode':
                    imported_modules.append(i)
            encoded_soure = b64encode(('\n'.join(source)).encode()).decode()
            obfuscated = ';'.join(imported_modules) + ';exec(b64decode("' + encoded_soure + '").decode())'
            with open("payload.py", 'w') as f:
                f.write(obfuscated)
                self.log.inf("Encoded scout and overwrote raw file with Base64 encoded file contents")
        except SyntaxError:
            self.log.err("Could not encode scout")
    elif option == 'info':
        self.log.blank('\nName             : Basic Base 64 Encoder' \
                       '\nRequired Modules : base64' \
                       '\nDescription      : Uses the standard Base64 algorithm and alphabet to obfuscate the scout source\n')
        return {
            "Name": "Basic Base 64 Encoder",
            "Required Modules": "base64",
            "Description": "Uses the standard Base64 algorithm and alphabet to obfuscate the scout source"}