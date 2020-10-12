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
        if interface == "GUI":
            try:
                config.listener_values[command.split(' ')[1]][0] = command.split(' ', 2)[2]
                log.log_normal("Set " + command.split(' ')[1] + " to " + command.split(' ', 2)[2])
            except:
                config.listener_values[command.split(' ')[1]][0] = ""
                log.log_normal("Set " + command.split(' ')[1] + " to <empty_string>")
            return jsonify({"output": "Success", "output_message": "", "data": config.listener_values})
        elif interface == "CUI":
            config.listener_values[command.split(' ')[1]][0] = command.split(' ', 2)[2]
            print(config.pos + 'Set "' + command.split(' ')[1] + '" to "' + command.split(' ', 2)[2] + '"')
    except (IndexError, KeyError) as e:
        if interface == "GUI":
            log.log_error("Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": str(e), "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid option and value')
