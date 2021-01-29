# API
# done
import pyiris_api.library.modules.send_and_recv as send_and_recv
import os


def main(self, scout_id, file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            data = f.read()
        self.log.pos('Read in data from script file : ' + file_path)
        self.log.inf('Sending file data to scout')
        self.log.inf('Attempting to run on scout...')
        data = send_and_recv.main(self, 'exec_py ' + data, scout_id)
        self.log.blank(data)
        return {"status": "ok", "message": "", "data": {"scout_output": data}}
    else:
        self.log.err("Invalid file path supplied")
        return {"status": "error", "message": "", "data": {"scout_output": "[-]Invalid file path supplied"}}
