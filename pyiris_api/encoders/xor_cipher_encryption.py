# API
# done
import base64
from itertools import cycle
import pyiris_api.library.modules.return_random_string as return_random_string


def xor_encoder(plaintext, cipher):
    encrypted = []
    for (char_1, char_2) in zip(plaintext, cycle(cipher)):
        encrypted.append(chr(ord(char_1) ^ ord(char_2)))
    return "".join(encrypted)


def main(self, option):
    if option == 'encode':
        try:
            imported_modules = ['from itertools import cycle', 'from base64 import b64decode']
            with open("payload.py", 'r') as f:
                data = f.read().replace(';', '\n')
            source = data.split('\n')
            for i in source:
                if 'import' in i and i != 'from itertools import cycle':
                    imported_modules.append(i)
            key = return_random_string.main(50)
            self.log.inf("Random 50 length XOR cipher key : " + key)
            encoded_source = base64.b64encode((xor_encoder('\n'.join(source), key)).encode()).decode()
            obfuscated = ';'.join(
                imported_modules) + ';exec("".join(chr(ord(c1)^ord(c2)) for (c1,c2) in zip(b64decode("' + encoded_source + '").decode(),cycle("' + key + '"))))'
            with open("payload.py", 'w') as f:
                f.write(obfuscated)
                self.log.inf("Encoded scout and overwrote raw file with XOR encoded file contents")
        except SyntaxError:
            self.log.err("Could not encode scout")
    elif option == 'info':
        self.log.blank('\nName             : XOR Cipher Encoder' \
                       '\nRequired Modules : itertools, base64' \
                       '\nDescription      : Uses XOR cipher encryption to obfuscate the scout source' \
                       '\nNote             : Requires base64 module to encode raw bytes as text so the scout is able to base64 decode itself into raw bytes to XOR decrypt itself\n')
        return {
            "Name": "XOR Cipher Encoder",
            "Required Modules": "itertools, base64",
            "Description": "Uses XOR cipher encryption to obfuscate the scout source"}