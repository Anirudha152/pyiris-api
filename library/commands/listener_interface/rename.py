# WEB

import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(command):
    try:
        id = command.split(' ', 2)[1]
        new_name = command.split(' ', 2)[2]
        config.listener_database[id][2] = new_name
        if interface == "GUI":
            config.app.logger.info("[library/commands/listener_interface/rename] - Successfully renamed listener " + str(id) + " to " + str(new_name))
            return jsonify({"output": "Success", "output_message": "Renamed listener", "data": ""})
        elif interface == "CUI":
            print(config.pos + 'Successfully renamed listener')
    except (IndexError, KeyError) as e:
        if interface == "GUI":
            config.app.logger.error("[library/commands/listener_interface/rename] - Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": e, "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify valid values, a valid ID and new name')

