# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(command):
    if interface == "GUI":
        try:
            list_type = command.split(' ', 1)[1]
            if list_type == 'wh':
                return jsonify({'output': "Success", "output_message": "", "data": config.white_list})
            elif list_type == 'bl':
                return jsonify({'output': "Success", "output_message": "", "data": config.black_list})
            elif list_type == 'all':
                return jsonify({'output': "Success", "output_message": "", "data": [config.white_list, config.black_list]})
            elif list_type == 'key':
                with open('resources/PyIris.cred', 'r') as f:
                    return jsonify({'output': 'Success', 'output_message': "", "data": f.read()})
            else:
                config.app.logger.error("\x1b[1m\x1b[31m[library/commands/home_interface/show] - Invalid Command: " + str(command) + "\x1b[0m")
                return jsonify({'output': "Fail", "output_message": "Invalid command", "data": ""})
        except IndexError as e:
            config.app.logger.error("\x1b[1m\x1b[31m[library/commands/home_interface/show] - Index Error: " + str(e) + "\x1b[0m")
            return jsonify({'output': "Fail", "output_message": "Invalid command", "data": ""})
    elif interface == "CUI":
        try:
            list_type = command.split(' ', 1)[1]
            if list_type == 'wh':
                print('\n' + config.pos + 'Whitelisted hosts : ')
                for i in config.white_list:
                    print('   ' + i)
                print('\n')
            elif list_type == 'bl':
                print('\n' + config.pos + 'Blacklisted hosts : ')
                for i in config.black_list:
                    print('   ' + i)
                print('\n')
            elif list_type == 'all':
                print('\n' + config.pos + 'Whitelisted hosts : ')
                for i in config.white_list:
                    print('   ' + i)
                print('\n' + config.pos + 'Blacklisted hosts : ')
                for i in config.black_list:
                    print('   ' + i)
                print('\n')
            elif list_type == 'key':
                print(config.inf + 'Currently used key : \n   ' + config.key)
            else:
                raise IndexError
        except IndexError:
            print(config.neg + 'Please specify a valid object to show, ["wh"|"bl"|"all"|"key"]')

