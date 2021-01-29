# API
# done
import pyiris_api.library.modules.recv_all as recv_all
from base64 import b64encode
from ntpath import basename
import pyiris_api.library.modules.send_all as send_all


def main(self, sock, filepath):
    try:
        filepath = filepath.split(' ', 1)[1]
        self.log.inf('Reading file...')
        with open(filepath, 'rb') as f:
            data = f.read()
        self.log.inf('Sending file data to scout...')
        send_all.main(sock, 'c upload ' + basename(filepath) + ' ' + b64encode(data).decode())
        response = recv_all.main(sock)
        self.log.blank(response)
        return {"status": "ok", "message": "", "data": {"scout_output": response}}
    except IOError:
        self.log.err('File does not exist, cannot upload')
        return {"status": "error", "message": "", "data": {"scout_output": '[-]File does not exist, cannot upload'}}
    except IndexError:
        self.log.err('Please supply valid arguments for the command you are running')
        return {"status": "error", "message": "", "data": {"scout_output": '[-]Please supply valid arguments for the command you are running'}}
    except Exception as e:
        self.log.err('Error while uploading file : ' + str(e))
        return {"status": "error", "message": "", "data": {"scout_output": '[-]Error while uploading file : ' + str(e)}}
