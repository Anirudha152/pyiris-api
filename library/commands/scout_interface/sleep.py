import socket
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify

def main(scout_id):
    try:
        slp_scout_id = scout_id.split(' ', 2)[1]
        sleep_dur = scout_id.split(' ', 2)[2]
        if slp_scout_id == 'all':
            for i in list(config.scout_database.keys()):
                try:
                    if interface == "GUI":
                        config.app.logger.info("[library/commands/scout_interface/sleep] - Sleeping scout of ID : " + str(i))
                    elif interface == "CUI":
                        print(config.inf + 'Sleeping scout of ID : ' + i)
                    config.scout_database[i][0].sendall(('sleep ' + sleep_dur).encode())
                    data = config.scout_database[i][0].recv(999999).decode()
                    if interface == "GUI":
                        config.app.logger.info("[library/commands/scout_interface/sleep] - Message from scout: " + str(data))
                    elif interface == "CUI":
                        print(data)
                    del (config.scout_database[i])
                    config.change = True
                    if interface == "GUI":
                        return jsonify({"output": "Success", "output_message": data[3:], "data": ""})
                except socket.error:
                    if interface == "GUI":
                        config.app.logger.error("[library/commands/scout_interface/sleep] - Scout is dead, removing from database...")
                    elif interface == "CUI":
                        print(config.neg + 'Scout is dead, removing from database...')
                    del (config.scout_database[i])
                    config.change = True
                    if interface == "GUI":
                        return jsonify({"output": "Fail", "output_message": "Scout is dead, removing from database...", "data": ""})
        else:
            if interface == "GUI":
                config.app.logger.info("[library/commands/scout_interface/sleep] - Sleeping scout of ID : " + str(scout_id))
            elif interface == "CUI":
                print(config.inf + 'Sleeping scout of ID : ' + str(scout_id))
            config.scout_database[slp_scout_id][0].sendall(('sleep ' + sleep_dur).encode())
            data = config.scout_database[slp_scout_id][0].recv(999999).decode()
            if interface == "GUI":
                config.app.logger.info("[library/commands/scout_interface/sleep] - Message from scout: " + str(data))
            elif interface == "CUI":
                print(data)
            del (config.scout_database[slp_scout_id])
            config.change = True
            if interface == "GUI":
                return jsonify({"output": "Success", "output_message": data[3:], "data": ""})
    except KeyError:
        if interface == "GUI":
            config.app.logger.error("[library/commands/scout_interface/sleep] - Invalid Scout ID")
        elif interface == "CUI":
            print(config.neg + 'Please enter a valid scout ID')
        return
    except IndexError:
        print(config.neg + 'Please enter valid arguments')
    except socket.error:
        if interface == "GUI":
            config.app.logger.error("[library/commands/scout_interface/sleep] - Scout is dead, removing from database...")
        elif interface == "CUI":
            print(config.neg + 'Scout is dead, removing from database...')
        del (config.scout_database[scout_id])
        config.change = True
        if interface == "GUI":
            return jsonify({"output": "Fail", "output_message": "Scout is dead... Removed from database", "data": ""})
