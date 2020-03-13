import threading
import time
import library.modules.config as config
import library.modules.socket_listener as socket_listener
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.monitor_listeners as monitor_listeners
def main():
    if interface == "GUI":
        try:
            host = config.listener_values['Interface'][0]
            port = int(config.listener_values['Port'][0])
            name = config.listener_values['Name'][0]
            reply = config.listener_values['Reply'][0]
            t = threading.Thread(target=socket_listener.main,
                                 args=(host, port, name, reply))
            t.start()
            time.sleep(3)
            return jsonify({"output": "Success", "output_message": "Listener Started", "data": ""})
        except (IndexError, ValueError):
            return jsonify({"output": "Fail", "output_message": "Unknown error occurred", "data": ""})

    elif interface == "CUI":
        try:
            host = config.listener_values['Interface'][0]
            port = int(config.listener_values['Port'][0])
            name = config.listener_values['Name'][0]
            reply = config.listener_values['Reply'][0]
            t = threading.Thread(target=socket_listener.main,
                                 args=(host, port, name, reply))
            t.start()
            time.sleep(3)
        except (IndexError, ValueError):
            print(config.neg + 'Please use valid values')