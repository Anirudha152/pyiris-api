# API
# done
from cryptography.fernet import Fernet


def main(self, option):
    if option == 'encode':
        try:    
            imported_modules = ['from cryptography.fernet import Fernet']
            with open("payload.py", 'r') as f:
                data = f.read().replace(';', '\n')
            source = data.split('\n')
            for i in source:
                if 'import' in i and i != 'from cryptography.fernet import Fernet':
                    imported_modules.append(i)
            key = Fernet.generate_key()
            self.log.inf("Fernet generated cipher key for AES symmetrical encryption : " + key.decode())
            cipher_suite = Fernet(key)
            encoded_source = cipher_suite.encrypt(('\n'.join(source).encode()))
            obfuscated = ';'.join(
                imported_modules) + ';cipher_suite = Fernet(b"' + key.decode() + '");exec(cipher_suite.decrypt(b"' + encoded_source.decode() + '"))'
            with open("payload.py", 'w') as f:
                f.write(obfuscated)
            self.log.inf("Encoded scout and overwrote raw file with AES encrypted file contents using Fernet")
        except SyntaxError:
            self.log.err("Could not encode scout")
    elif option == 'info':
        self.log.blank('\nName             : AES Encoder' \
                       '\nRequired Modules : cryptography' \
                       '\nDescription      : Uses Fernet to AES encrypt the scout\n')
        return {
            "Name": "AES Encoder",
            "Required Modules": "cryptography",
            "Description": "Uses Fernet to AES encrypt the scout"}