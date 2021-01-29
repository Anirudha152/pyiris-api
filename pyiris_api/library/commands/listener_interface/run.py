# API
# done
import threading
import time
import pyiris_api.library.modules.socket_listener as socket_listener


def main(self):
    try:
        host = self.config.listener_values['Interface'][0]
        port = int(self.config.listener_values['Port'][0])
        name = self.config.listener_values['Name'][0]
        reply = self.config.listener_values['Reply'][0]
        t = threading.Thread(target=socket_listener.main,
                             args=(self, host, port, name, reply))
        t.start()
        time.sleep(3)
        return {"status": "ok", "message": 'Started Listener', "data": None}
    except (IndexError, ValueError):
        self.log.err('Please use valid values')
        return {"status": "error", "message": 'Please use valid values', "data": None}
