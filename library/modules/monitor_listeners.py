import library.modules.config as config
import time
import logging
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify

def check():
    if config.listener_database == {} and config.scout_database == {}:
        output = jsonify({"output": "Success", "output_message": "Li Empty Sc Empty", "data": ""})
    elif config.listener_database == {}:
        toReturn = {}
        keys = list(config.scout_database.keys())
        keys.sort()
        for i in keys:
            toReturn[i] = [i, config.scout_database[i][1], config.scout_database[i][2],
                           config.scout_database[i][3], config.scout_database[i][4],
                           config.scout_database[i][5], config.scout_database[i][6]]
        output = jsonify({"output": "Success", "output_message": "Li Empty Sc Data", "data": toReturn})
    elif config.scout_database == {}:
        output = jsonify({"output": "Success", "output_message": "Li Data Sc Empty", "data": config.listener_database})
    else:
        toReturn = {}
        keys = list(config.scout_database.keys())
        keys.sort()
        for i in keys:
            toReturn[i] = [i, config.scout_database[i][1], config.scout_database[i][2],
                           config.scout_database[i][3], config.scout_database[i][4],
                           config.scout_database[i][5], config.scout_database[i][6]]
        output = jsonify(
            {"output": "Success", "output_message": "Li Data Sc Data", "data": [config.listener_database, toReturn]})
    return output

def main():
    if interface == "GUI":
        config.app.logger.info("[library/modules/monitor_listeners] - Started Monitor")
        while True:
            config.monitoring = True
            if not config.AbruptEnd:
                try:
                    try:
                        message = config.thread_message
                        config.thread_message = ""
                        output = False
                        if message[0] == "neg":
                            output = jsonify({"output": "Fail", "output_message": "Msg", "data": message[1]})
                        elif message[0] == "pos":
                            output = jsonify({"output": "Success", "output_message": "Msg", "data": message[1]})
                        if output:
                            config.app.logger.info("[library/modules/monitor_listeners] - Received output from listener thread. Exiting Monitor")
                            return output
                    except:
                        pass
                    if config.change:
                        config.app.logger.info("[library/modules/monitor_listeners] - Change Detected")
                        config.change = False
                        output = check()
                        config.app.logger.info("[library/modules/monitor_listeners] - Exiting Monitor")
                        config.monitoring = False
                        return output
                except Exception as e:
                    config.app.logger.error("[library/modules/monitor_listeners] - Error: " + str(e))
                    return jsonify({"output": "Fail", "output_message": str(e), "data": ""})
            else:
                for handler in logging.root.handlers[:]:
                    logging.root.removeHandler(handler)
                logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s > %(message)s")
                config.app.logger.info("[library/modules/monitor_listeners] - Forced Thread Shutdown")
                config.AbruptEnd = False
                config.monitoring = False
                return jsonify({"output": "Success", "output_message": "Forced Shutdown", "data": ""})
