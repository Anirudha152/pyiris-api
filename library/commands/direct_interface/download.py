import library.modules.recv_all as recv_all
from ntpath import basename
from base64 import b64decode
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(sock):
    if interface == "GUI":
        try:
            config.app.logger.info("[library/commands/direct_interface/download] - Receiving data...")
            data = recv_all.main(sock).split(' ')
            if data[0].startswith('[-]') or data[0].startswith('[!]'):
                config.app.logger.error("[library/commands/direct_interface/download] - ".join(data))
                return jsonify({"output": "Fail", "output_message": "[!]Error while downloading", "data": data})
            config.app.logger.info("[library/commands/direct_interface/download] - Done, writing file...")
            name = basename(' '.join(data[:-1]))
            contents = b64decode(data[-1])
            with open(name, 'wb') as f:
                f.write(contents)
            config.app.logger.info("[library/commands/direct_interface/download] - Downloaded file : " + name)
            return jsonify({"output": "Success", "output_message": "Downloaded successfully", "data": "[+]Downloaded file : " + name})
        except (TypeError, KeyError):
            config.app.logger.error("[library/commands/direct_interface/download] - " + data)
            return jsonify({"output": "Fail", "output_message": "[!]Error while downloading", "data": data})
        except Exception as e:
            config.app.logger.error("[library/commands/direct_interface/download] - Error while downloading file : " + str(e))
            return jsonify({"output": "Fail", "output_message": "[!]Error while downloading", "data": str(e)})
    elif interface == "CUI":
        try:
            print(config.inf + 'Receiving data...')
            data = recv_all.main(sock).split(' ')
            if data[0].startswith('[-]') or data[0].startswith('[!]'):
                print (' '.join(data))
                return
            print(config.pos + 'Done, writing file...')
            name = basename(' '.join(data[:-1]))
            contents = b64decode(data[-1])
            with open(name, 'wb') as f:
                f.write(contents)
            print(config.pos + 'Downloaded file : ' + name)
        except (TypeError, KeyError):
            print(data)
        except Exception as e:
            print(config.neg + 'Error while downloading file : ' + str(e))
