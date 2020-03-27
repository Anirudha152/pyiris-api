import library.modules.send_and_recv as send_and_recv
from base64 import b64encode
from ntpath import basename
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(scoutId, filepath):
    if interface == "GUI":
        try:
            filepath = filepath.split(' ', 1)[1]
            config.app.logger.info("[library/commands/direct_interface/upload] - Reading file...")
            with open(filepath, 'rb') as f:
                data = f.read()
            config.app.logger.info("[library/commands/direct_interface/upload] - Sending file data to scout...")
            response = send_and_recv.main("g upload " + basename(filepath) + ' ' + b64encode(data).decode(), scoutId)
            config.app.logger.info("[library/commands/direct_interface/upload] - Message from scout: " + response)
            return jsonify({"output": "Success", "output_message": "Command Output", "data": response})
        except IOError:
            config.app.logger.error("[library/commands/direct_interface/upload] - File does not exist, cannot upload")
            return jsonify(
                {"output": "Success", "output_message": "Command Output", "data": "[!]Error while uploading: File does not exist, cannot upload"})
        except IndexError:
            config.app.logger.error("[library/commands/direct_interface/upload] - Please supply valid arguments for the command you are running")
            return jsonify(
                {"output": "Success", "output_message": "Command Output",
                 "data": "[!]Error while uploading: Please supply valid arguments for the command you are running"})
        except Exception as e:
            config.app.logger.error("[library/commands/direct_interface/upload] - Error while uploading file : " + str(e))
            return jsonify({"output": "Success", "output_message": "Command Output",
                            "data": "[!]Error while uploading: " + str(e)})
    elif interface == "CUI":
        try:
            filepath = filepath.split(' ', 1)[1]
            print(config.inf + 'Reading file...')
            with open(filepath, 'rb') as f:
                data = f.read()
            print(config.inf + 'Sending file data to scout...')
            response = send_and_recv.main("c upload " + basename(filepath) + ' ' + b64encode(data).decode(), scoutId)
            print(response)
        except IOError:
            print(config.neg + 'File does not exist, cannot upload')
        except IndexError:
            print(config.neg + 'Please supply valid arguments for the command you are running')
        except Exception as e:
            print(config.neg + 'Error while uploading file : ' + str(e))
