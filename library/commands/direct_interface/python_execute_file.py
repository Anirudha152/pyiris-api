# GUI + CUI
# done
import library.modules.send_and_recv as send_and_recv
import os
import library.modules.config as config

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(data, scout_id):
    file_path = data.split(' ', 1)[1]
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            data = f.read()
        if interface == "GUI":
            log.log_normal("Read in data from script file : " + file_path)
            log.log_normal("Sending file data to scout")
            log.log_normal("Attempting to run on scout...")
            output = send_and_recv.main('g exec_py ' + data, scout_id)
            log.log_normal("Message from scout: " + output)
            return jsonify({"output": "Success", "output_message": "Command Output", "data": output})
        elif interface == "CUI":
            print(config.pos + 'Read in data from script file : ' + file_path)
            print(config.inf + 'Sending file data to scout')
            print(config.inf + 'Attempting to run on scout...')
            print(send_and_recv.main('c exec_py ' + data, scout_id))
    else:
        if interface == "GUI":
            log.log_error("Invalid file path supplied")
            return jsonify(
                {"output": "Success", "output_message": "Command Output", "data": "[-]Invalid file path supplied"})
        elif interface == "CUI":
            print(config.neg + 'Invalid file path supplied')
