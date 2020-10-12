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
            id = command.split(' ', 1)[1]
            if id in list(config.listener_database.keys()):
                del (config.listener_database[id])
                log.log_normal("Sent kill message to listener " + str(id))
                return jsonify({"output": "Success", "output_message": "Killing", "data": ""})
            elif id == 'all':
                config.listener_database = {}
                log.log_normal("Sent kill message to all listeners")
                return jsonify({"output": "Success", "output_message": "Killing", "data": ""})
        except IndexError as e:
            log.log_error("Index Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": e, "data": ""})
    elif interface == "CUI":
        try:
            id = command.split(' ', 1)[1]
            if id in list(config.listener_database.keys()):
                del (config.listener_database[id])
                print(config.inf + 'Sent kill message to listener of ID : ' + id + '...')
            elif id == 'all':
                print(config.inf + 'Sent kill message to all listeners')
                config.listener_database = {}
            else:
                print(config.neg + 'Listener of ID : ' + id + ' is not active')
        except IndexError:
            print(config.neg + 'Please specify the ID of the listener to kill, or specify "all"')
