import library.modules.config as config
from cryptography.fernet import Fernet
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(option, filepath=None):
    if not filepath:
        filepath = config.scout_values['Path'][0]
    if option == 'encode':
        try:
            imported_modules = ['from cryptography.fernet import Fernet']
            with open(filepath, 'r') as f:
                data = f.read().replace(';', '\n')
            source = data.split('\n')
            for i in source:
                if 'import' in i and i != 'from cryptography.fernet import Fernet':
                    imported_modules.append(i)
            key = Fernet.generate_key()
            if interface == "GUI":
                config.app.logger.info("[encoders/aes_stream_encoder] - Fernet generated cipher key for AES symmetrical encryption : " + key.decode())
            elif interface == "CUI":
                print('   ' + config.inf + 'Fernet generated cipher key for AES symmetrical encryption : ' + key.decode())
            cipher_suite = Fernet(key)
            encoded_source = cipher_suite.encrypt(('\n'.join(source).encode()))
            obfuscated = ';'.join(
                imported_modules) + ';cipher_suite = Fernet(b"' + key.decode() + '");exec(cipher_suite.decrypt(b"' + encoded_source.decode() + '"))'
            with open(filepath, 'w') as f:
                f.write(obfuscated)
                if interface == "GUI":
                    config.app.logger.info("[encoders/aes_stream_encoder] - Encoded scout and overwrote raw file with AES encrypted file contents using Fernet")
                elif interface == "CUI":
                    print('   ' + config.inf + 'Encoded scout and overwrote raw file with AES encrypted file contents using Fernet')
        except SyntaxError:
            if interface == "GUI":
                config.app.logger.error("\x1b[1m\x1b[31m[encoders/aes_stream_encoder] - Could not encode scout\x1b[0m")
            elif interface == "CUI":
                print('   ' + config.neg + 'Could not encode scout')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "AES Encoder",
                "Required Modules": "cryptography",
                "Description": "Uses Fernet to AES encrypt the scout"}
        elif interface == "CUI":
            print('\nName             : AES Encoder' \
                  '\nRequired Modules : cryptography' \
                  '\nDescription      : Uses Fernet to AES encrypt the scout\n')
