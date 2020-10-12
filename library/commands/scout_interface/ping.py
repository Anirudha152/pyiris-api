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
                        log.log_normal('Pinging scout of ID : ' + i)
                        send_all.main(config.scout_database[i][0], 'g ping')
                        data = recv_all.main(config.scout_database[i][0])
                        if not data:
                            raise socket.error
                        log.log_normal("Message from scout: " + str(data))
                    except socket.error:
                        log.log_error('Scout is dead, removing from database...')
                        del (config.scout_database[i])
                        config.change = True
                return jsonify({"output": "Success", "output_message": "Pinged all scouts, output in server logs", "data": ""})
            else:
                send_all.main(config.scout_database[scout_id][0], 'g ping')
                data = recv_all.main(config.scout_database[scout_id][0])
                log.log_normal("Message from scout: " + str(data))
                return jsonify({"output": "Success", "output_message": data[3:], "data": ""})
        except (IndexError, KeyError):
            log.log_error('Please enter a valid scout ID')
            return jsonify({"output": "Fail", "output_message": "Invalid scout ID", "data": ""})
        except socket.error:
            log.log_error('Scout is dead, removing from database...')
            del (config.scout_database[scout_id])
            config.change = True
            return jsonify({"output": "Fail", "output_message": "Scout is dead... Removed from database", "data": ""})
    elif interface == "CUI":
        try:
            scout_id = scout_id.split(' ', 1)[1]
            if scout_id == 'all':
                for i in list(config.scout_database.keys()):
                    try:
                        print(config.inf + 'Pinging scout of ID : ' + i)
                        send_all.main(config.scout_database[i][0], 'ping')
                        data = recv_all.main(config.scout_database[i][0])
                        if not data:
                            raise socket.error
                        print(data)
                    except socket.error:
                        print(config.neg + 'Scout is dead, removing from database...')
                        del (config.scout_database[i])
            else:
                send_all.main(config.scout_database[scout_id][0], 'ping')
                data = recv_all.main(config.scout_database[scout_id][0])
                print(data)
        except (IndexError, KeyError):
            print(config.neg + 'Please enter a valid scout ID')
            return
        except socket.error:
            print(config.neg + 'Scout is dead, removing from database...')
            del (config.scout_database[scout_id])
