# GUI + CUI
# done
import library.modules.recv_all as recv_all
from ntpath import basename
from base64 import b64decode
import library.modules.config as config

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(sock):
    if interface == "GUI":
        try:
            log.log_normal("Receiving data...")
            data = recv_all.main(sock).split(' ')
            if data[0].startswith('[-]') or data[0].startswith('[!]'):
                log.log_error("".join(data))
                return jsonify({"output": "Fail", "output_message": "[!]Error while downloading", "data": data})
            log.log_normal("Done, writing file...")
            name = basename(' '.join(data[:-1]))
            contents = b64decode(data[-1])
            with open(name, 'wb') as f:
                f.write(contents)
            log.log_normal("Downloaded file : " + name)
            return jsonify({"output": "Success", "output_message": "Downloaded successfully", "data": "[+]Downloaded file : " + name})
        except (TypeError, KeyError):
            log.log_error(data)
            return jsonify({"output": "Success", "output_message": "Command Output", "data": "[!]Error while downloading: " + data})
        except Exception as e:
            log.log_error("Error while downloading file : " + str(e))
            return jsonify({"output": "Success", "output_message": "Command Output", "data": "[!]Error while downloading: " + str(e)})
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