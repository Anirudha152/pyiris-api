# WEB + COM
import time
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify

def main(command):
    try:
        if interface == "GUI":
            try:
                config.listener_values[command.split(' ')[1]][0] = command.split(' ', 2)[2]
                config.app.logger.info("[library/commands/listener_interface/set] - Set " + command.split(' ')[1] + " to " + command.split(' ', 2)[2])
            except:
                config.listener_values[command.split(' ')[1]][0] = ""
                config.app.logger.info("[library/commands/listener_interface/set] - Set " + command.split(' ')[1] + " to <empty_string>")
            return jsonify({"output": "Success", "output_message": "", "data": config.listener_values})
        elif interface == "CUI":
            config.listener_values[command.split(' ')[1]][0] = command.split(' ', 2)[2]
            print(config.pos + 'Set "' + command.split(' ')[1] + '" to "' + command.split(' ', 2)[2] + '"')
    except IndexError as e:
        if interface == "GUI":
            config.app.logger.error("[library/commands/listener_interface/set] - Index Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": "", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid option and value')
    except KeyError as e:
        if interface == "GUI":
            config.app.logger.error("[library/commands/listener_interface/set] - Key Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": "", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid option and value')
