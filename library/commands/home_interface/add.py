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
            list_type = command.split(' ')[1]
            hostname = command.split(' ', 2)[2]
            if list_type == 'wh':
                config.white_list.append(hostname)
                config.white_list = list(set(config.white_list))
                log.log_normal("Added " + str(hostname) + " to whitelist")
                return jsonify({'output': "Success", "output_message": "", "data": config.white_list})
            elif list_type == 'bl':
                config.black_list.append(hostname)
                config.black_list = list(set(config.black_list))
                log.log_normal("Added " + str(hostname) + " to blacklist")
                return jsonify({'output': "Success", "output_message": "", "data": config.black_list})
            else:
                raise IndexError
        except IndexError:
            log.log_error("Hostname: " + str(hostname) + " is invalid")
            return jsonify({'output': "Fail", "output_message": "Please specify a valid list and a hostname to add to the list", "data": ""})
    elif interface == "CUI":
        try:
            list_type = command.split(' ')[1]
            hostname = command.split(' ', 2)[2]
            if list_type == 'wh':
                config.white_list.append(hostname)
                config.white_list = list(set(config.white_list))
                print(config.pos + 'Added to whitelist')
            elif list_type == 'bl':
                config.black_list.append(hostname)
                config.black_list = list(set(config.black_list))
                print(config.pos + 'Added to blacklist')
            else:
                raise IndexError
        except IndexError:
            print(config.neg + 'Please specify a valid list and a hostname to add to the list')
