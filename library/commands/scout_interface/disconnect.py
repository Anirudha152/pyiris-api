import socket
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify

def main(scout_id):
    if interface == "GUI":
        try:
            scout_id = scout_id.split(' ', 1)[1]
            if scout_id == 'all':
                for i in list(config.scout_database.keys()):
                    try:
                        config.app.logger.info("[library/commands/scout_interface/disconnect] - Disconnecting scout of ID : " + str(i))
                        config.scout_database[i][0].sendall('g disconnect'.encode())
                        data = config.scout_database[i][0].recv(999999).decode()
                        config.app.logger.info("[library/commands/scout_interface/disconnect] - Message from scout: " + str(data))
                        del (config.scout_database[i])
                        config.change = True
                        return jsonify({"output": "Success", "output_message": "Disconnected scout", "data": ""})
                    except socket.error:
                        config.app.logger.error("[library/commands/scout_interface/disconnect] - Scout is dead, removing from database...")
                        del (config.scout_database[i])
                        config.change = True
                        return jsonify({"output": "Success", "output_message": "Scout is dead, removing from database...", "data": ""})
            else:
                config.app.logger.info("[library/commands/scout_interface/disconnect] - Disconnecting scout of ID : " + str(scout_id))
                config.scout_database[scout_id][0].sendall('g disconnect'.encode())
                data = config.scout_database[scout_id][0].recv(999999).decode()
                config.app.logger.info("[library/commands/scout_interface/disconnect] - Message from scout: " + str(data))
                del (config.scout_database[scout_id])
                config.change = True
                return jsonify({"output": "Success", "output_message": "Disconnected scout", "data": ""})
        except (IndexError, KeyError):
            config.app.logger.error("[library/commands/scout_interface/disconnect] - Invalid Scout ID")
            return jsonify({"output": "Fail", "output_message": "Please enter a valid scout ID", "data": ""})
        except socket.error:
            config.app.logger.error("[library/commands/scout_interface/disconnect] - Scout is dead, removing from database...")
            del (config.scout_database[scout_id])
            config.change = True
            return jsonify({"output": "Fail", "output_message": "Scout is dead, removing from database...", "data": ""})
    elif interface == "CUI":
        try:
            scout_id = scout_id.split(' ', 1)[1]
            if scout_id == 'all':
                for i in list(config.scout_database.keys()):
                    try:
                        print(config.inf + 'Disconnecting scout of ID : ' + i)
                        config.scout_database[i][0].sendall('c disconnect'.encode())
                        data = config.scout_database[i][0].recv(999999).decode()
                        print(data)
                        del (config.scout_database[i])
                    except socket.error:
                        print(config.neg + 'Scout is dead, removing from database...')
                        del (config.scout_database[i])
            else:
                config.scout_database[scout_id][0].sendall('c disconnect'.encode())
                data = config.scout_database[scout_id][0].recv(999999).decode()
                print(data)
                del (config.scout_database[scout_id])
        except (IndexError, KeyError):
            print(config.neg + 'Please enter a valid scout ID')
            return
        except socket.error:
            print(config.neg + 'Scout is dead, removing from database...')
            del (config.scout_database[scout_id])
