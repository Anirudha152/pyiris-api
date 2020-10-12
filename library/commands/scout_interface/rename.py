# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(command):
    if interface == "GUI":
        try:
            id = command.split(' ', 2)[1]
            new_name = command.split(' ', 2)[2]
            config.scout_database[id][4] = new_name
            log.log_normal("Successfully renamed scout " + str(id) + " to " + str(new_name))
            config.change = True
            return jsonify({"output": "Success", "output_message": "Successfully renamed scout", "data": ""})
        except (IndexError, KeyError):
            log.log_error("Invalid Scout ID")
            config.change = True
            return jsonify({"output": "Fail", "output_message": "Invalid Scout ID", "data": ""})
    elif interface == "CUI":
        try:
            id = command.split(' ', 2)[1]
            new_name = command.split(' ', 2)[2]
            config.scout_database[id][4] = new_name
            print(config.pos + 'Successfully renamed scout')
        except (IndexError, KeyError):
            print(config.neg + 'Please specify valid values, a valid ID and new name')
