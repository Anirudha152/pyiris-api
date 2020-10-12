# GUI + CUI
# done
import socket
import library.modules.config as config
import library.modules.send_all as send_all
import library.modules.recv_all as recv_all

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(scout_id):
    if interface == "GUI":
        try:
            scout_id = scout_id.split(' ', 1)[1]
            if scout_id == 'all':
                for i in list(config.scout_database.keys()):
                    try:
                        log.log_normal("Disconnecting scout of ID : " + str(i))
                        data = send_and_recv.main("g disconnect", i)
                        log.log_normal("Message from scout: " + str(data))
                        del (config.scout_database[i])
                        config.change = True
                    except socket.error:
                        log.log_error("Scout is dead, removing from database...")
                        del (config.scout_database[i])
                        config.change = True
                return jsonify({"output": "Success", "output_message": "Disconnected all scouts, output in server logs", "data": ""})
            else:
                log.log_normal("Disconnecting scout of ID : " + str(scout_id))
                data = send_and_recv.main("g disconnect", scout_id)
                log.log_normal("Message from scout: " + str(data))
                del (config.scout_database[scout_id])
                config.change = True
                return jsonify({"output": "Success", "output_message": "Disconnected scout", "data": ""})
        except (IndexError, KeyError):
            log.log_error("Invalid Scout ID")
            return jsonify({"output": "Fail", "output_message": "Please enter a valid scout ID", "data": ""})
        except socket.error:
            log.log_error("Scout is dead, removing from database...")
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
                        send_all.main(config.scout_database[i][0], 'c disconnect')
                        data = recv_all.main(config.scout_database[i][0])
                        print(data)
                        del (config.scout_database[i])
                    except socket.error:
                        print(config.neg + 'Scout is dead, removing from database...')
                        del (config.scout_database[i])
            else:
                send_all.main(config.scout_database[scout_id][0], 'c disconnect')
                data = recv_all.main(config.scout_database[scout_id][0])
                print(data)
                del (config.scout_database[scout_id])
        except (IndexError, KeyError):
            print(config.neg + 'Please enter a valid scout ID')
            return
        except socket.error:
            print(config.neg + 'Scout is dead, removing from database...')
            del (config.scout_database[scout_id])