import socket
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(scout_id):
    try:
        scout_id = scout_id.split(' ', 1)[1]
        if scout_id == 'all':
            for i in list(config.scout_database.keys()):
                try:
                    if interface == "GUI":
                        config.app.logger.info("[library/commands/scout_interface/kill] - Killing scout of ID : " + str(i))
                    elif interface == "CUI":
                        print(config.inf + 'Killing scout of ID : ' + str(i))
                    config.scout_database[i][0].sendall('g kill'.encode())
                    data = config.scout_database[i][0].recv(999999).decode()
                    if interface == "GUI":
                        config.app.logger.info("[library/commands/scout_interface/kill] - Message from scout: " + str(data))
                    elif interface == "CUI":
                        print(data)
                    del (config.scout_database[i])
                    config.change = True
                    if interface == "GUI":
                        return jsonify({"output": "Success", "output_message": "", "data": data})
                except socket.error:
                    if interface == "GUI":
                        config.app.logger.error("[library/commands/scout_interface/kill] - Scout is dead, removing from database...")
                    elif interface == "CUI":
                        print(config.neg + 'Scout is dead, removing from database...')
                    del (config.scout_database[i])
                    config.change = True
                    if interface == "GUI":
                        return jsonify({"output": "Success", "output_message": "", "data": ""})
        else:
            if interface == "GUI":
                config.app.logger.info("[library/commands/scout_interface/kill] - Killing scout of ID : " + str(scout_id))
            elif interface == "CUI":
                print(config.inf + 'Killing scout of ID : ' + scout_id)
            config.scout_database[scout_id][0].sendall('g kill'.encode())
            data = config.scout_database[scout_id][0].recv(999999).decode()
            if interface == "GUI":
                config.app.logger.info("[library/commands/scout_interface/kill] - Message from scout: " + str(data))
            elif interface == "CUI":
                print(data)
            del (config.scout_database[scout_id])
            config.change = True
            if interface == "GUI":
                return jsonify({"output": "Success", "output_message": "", "data": data})
    except (IndexError, KeyError) as e:
        if interface == "GUI":
            config.app.logger.error("[library/commands/scout_interface/kill] - Invalid scout ID")
        elif interface == "CUI":
            print(config.neg + 'Please enter a valid scout ID')
        if interface == "GUI":
            return jsonify({"output": "Fail", "output_message": "Invalid scout ID", "data": ""})
    except socket.error:
        if interface == "GUI":
            config.app.logger.error("[library/commands/scout_interface/kill] - Scout is dead, removing from database...")
        elif interface == "CUI":
            print(config.neg + 'Scout is dead, removing from database...')
        del (config.scout_database[scout_id])
        config.change = True
        if interface == "GUI":
            return jsonify({"output": "Fail", "output_message": "Scout is dead, removing from database...", "data": ""})
