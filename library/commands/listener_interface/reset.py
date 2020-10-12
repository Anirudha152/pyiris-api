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
        local_static_values = {'Interface': ['0.0.0.0', 'The local interface to start a listener'],
                               'Port': ['9999', 'The local port to start a listener'],
                               'Name': ['Listener', 'Name of the listener'],
                               'Reply': ['',
                                         'The reply to send back in the case of a failed listener authentication/ connection']}
        option = command.split(' ', 1)[1]
        if option in local_static_values:
            config.listener_values[option] = local_static_values[option]
            if interface == "GUI":
                log.log_normal("Reset option " + str(option))
                return jsonify({"output": "Success", "output_message": "", "data": config.listener_values})
            elif interface == "CUI":
                print(config.pos + 'Reset option : ' + option)
        elif option == 'all':
            config.listener_values = {'Interface': ['0.0.0.0', 'The local interface to start a listener'],
                                      'Port': ['9999', 'The local port to start a listener'],
                                      'Name': ['Listener', 'Name of the listener'],
                                      'Reply': ['',
                                                'The reply to send back in the case of a failed listener authentication/ connection']}
            if interface == "GUI":
                log.log_normal("Reset all options")
                return jsonify({"output": "Success", "output_message": "", "data": config.listener_values})
            elif interface == "CUI":
                print(config.pos + 'Reset all options')
        else:
            if interface == "GUI":
                log.log_error("Invalid option")
                return jsonify({"output": "Fail", "output_message": "Invalid option", "data": ""})
            elif interface == "CUI":
                print(config.neg + 'Please specify a valid option to reset')
    except IndexError:
        if interface == "GUI":
            log.log_error("Index Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": e, "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid option to reset')
