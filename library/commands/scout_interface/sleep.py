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
    try:
        slp_scout_id = scout_id.split(' ', 2)[1]
        sleep_dur = scout_id.split(' ', 2)[2]
        if slp_scout_id == 'all':
            for i in list(config.scout_database.keys()):
                try:
                    if interface == "GUI":
                        log.log_normal("Sleeping scout of ID : " + str(i))
                    elif interface == "CUI":
                        print(config.inf + 'Sleeping scout of ID : ' + i)
                    data = send_and_recv.main('g sleep ' + sleep_dur, i)
                    if interface == "GUI":
                        log.log_normal("Message from scout: " + str(data))
                    elif interface == "CUI":
                        print(data)
                    del (config.scout_database[i])
                    config.change = True
                    if interface == "GUI":
                        return jsonify({"output": "Success", "output_message": data[3:], "data": ""})
                except socket.error:
                    if interface == "GUI":
                        log.log_error("Scout is dead, removing from database...")
                    elif interface == "CUI":
                        print(config.neg + 'Scout is dead, removing from database...')
                    del (config.scout_database[i])
                    config.change = True
                    if interface == "GUI":
                        return jsonify({"output": "Fail", "output_message": "Scout is dead, removing from database...",
                                        "data": ""})
        else:
            if interface == "GUI":
                log.log_normal("Sleeping scout of ID : " + str(slp_scout_id))
            elif interface == "CUI":
                print(config.inf + 'Sleeping scout of ID : ' + str(slp_scout_id))
            data = send_and_recv.main('g sleep ' + sleep_dur, slp_scout_id)
            if interface == "GUI":
                log.log_normal("Message from scout: " + str(data))
            elif interface == "CUI":
                print(data)
            del (config.scout_database[slp_scout_id])
            config.change = True
            if interface == "GUI":
                return jsonify({"output": "Success", "output_message": data[3:], "data": ""})
    except KeyError:
        if interface == "GUI":
            log.log_error("Invalid Scout ID")
        elif interface == "CUI":
            print(config.neg + 'Please enter a valid scout ID')
        return
    except IndexError:
        if interface == "GUI":
            log.log_error('Please enter valid arguments')
        elif interface == "CUI":
            print(config.neg + 'Please enter valid arguments')
    except socket.error:
        if interface == "GUI":
            log.log_error("Scout is dead, removing from database...")
        elif interface == "CUI":
            print(config.neg + 'Scout is dead, removing from database...')
        del (config.scout_database[slp_scout_id])
        config.change = True
        if interface == "GUI":
            return jsonify({"output": "Fail", "output_message": "Scout is dead... Removed from database", "data": ""})
