# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(command):
    try:
        id = command.split(' ', 2)[1]
        new_name = command.split(' ', 2)[2]
        config.listener_database[id][2] = new_name
        if interface == "GUI":
            log.log_normal("Successfully renamed listener " + str(id) + " to " + str(new_name))
            config.change = True
            return jsonify({"output": "Success", "output_message": "Renamed listener", "data": ""})
        elif interface == "CUI":
            print(config.pos + 'Successfully renamed listener')
    except (IndexError, KeyError) as e:
        if interface == "GUI":
            log.log_error("Error: " + str(e))
            config.change = True
            return jsonify({"output": "Fail", "output_message": e, "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify valid values, a valid ID and new name')
