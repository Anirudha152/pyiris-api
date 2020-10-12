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
            if list_type == 'wh':
                hostname = config.white_list[int(command.split(' ', 2)[2])]
                config.white_list.remove(hostname)
                log.log_normal("Removed " + str(hostname) + " from whitelist")
                return jsonify({'output': "Success", "output_message": "", "data": config.white_list})
            elif list_type == 'bl':
                hostname = config.black_list[int(command.split(' ', 2)[2])]
                config.black_list.remove(hostname)
                log.log_normal("Removed " + str(hostname) + " from blacklist")
                return jsonify({'output': "Success", "output_message": "", "data": config.black_list})
            else:
                raise IndexError
        except IndexError as e:
            log.log_error("Index Error: " + str(e))
            return jsonify({'output': "Fail", "output_message": "Hostname is invalid", "data": ""})
        except ValueError as e:
            log.log_error("Value Error: " + str(e))
            return jsonify({'output': "Fail", "output_message": "Hostname is invalid", "data": ""})
    elif interface == "CUI":
        try:
            list_type = command.split(' ')[1]
            hostname = command.split(' ', 2)[2]
            if list_type == 'wh':
                config.white_list.remove(hostname)
                print(config.pos + 'Removed from whitelist')
            elif list_type == 'bl':
                config.black_list.remove(hostname)
                print(config.pos + 'Removed from blacklist')
            else:
                raise IndexError
        except IndexError:
            print(config.neg + 'Please specify a valid list and a hostname to remove from a list')
        except ValueError:
            print(config.neg + 'Item user wants to remove does not exist')
