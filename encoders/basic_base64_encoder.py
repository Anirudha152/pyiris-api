# GUI + CUI
# done
import library.modules.config as config
from base64 import b64encode

config.main()
interface = config.interface
if interface == "GUI":
    import library.modules.log as log


def main(option, filepath=None):
    if not filepath:
        filepath = config.scout_values['Dir'][0]
    if option == 'encode':
        try:
            imported_modules = ['from base64 import b64decode']
            with open(filepath, 'r') as f:
                data = f.read().replace(';', '\n')
            source = data.split('\n')
            for i in source:
                if 'import' in i and i != 'from base64 import b64decode':
                    imported_modules.append(i)
            encoded_soure = b64encode(('\n'.join(source)).encode()).decode()
            obfuscated = ';'.join(imported_modules) + ';exec(b64decode("' + encoded_soure + '").decode())'
            with open(filepath, 'w') as f:
                f.write(obfuscated)
                if interface == "GUI":
                    log.log_normal("Encoded scout and overwrote raw file with Base64 encoded file contents")
                elif interface == "CUI":
                    print('   ' + config.inf + 'Encoded scout and overwrote raw file with Base64 encoded file contents')
        except SyntaxError:
            if interface == "GUI":
                log.log_error("Could not encode scout")
            elif interface == "CUI":
                print('   ' + config.neg + 'Could not encode scout')
    elif option == 'info':
        if interface == "GUI":
            return {
                "Name": "Basic Base 64 Encoder",
                "Required Modules": "base64",
                "Description": "Uses the standard Base64 algorithm and alphabet to obfuscate the scout source"}
        elif interface == "CUI":
            print('\nName             : Basic Base 64 Encoder' \
                  '\nRequired Modules : base64' \
                  '\nDescription      : Uses the standard Base64 algorithm and alphabet to obfuscate the scout source\n')