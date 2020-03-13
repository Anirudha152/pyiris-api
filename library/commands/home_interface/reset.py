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
            list_type = command.split(' ')[1]
            if list_type == 'wh':
                config.white_list = []
                config.app.logger.info("[library/commands/home_interface/reset] - Reset whitelist")
                return jsonify({'output': "Success", "output_message": "", "data": config.white_list})
            elif list_type == 'bl':
                config.black_list = []
                config.app.logger.info("[library/commands/home_interface/reset] - Reset blacklist")
                return jsonify({'output': "Success", "output_message": "", "data": config.black_list})
        except ValueError as e:
            config.app.logger.error("[library/commands/home_interface/reset] - Value Error: " + str(e))
            return jsonify({'output': "Fail", "output_message": "Value Error", "data": ""})
    elif interface == "CUI":
        try:
            list_type = command.split(' ')[1]
            if list_type == 'wh':
                config.white_list = []
                print(config.pos + 'Reset whitelist')
            elif list_type == 'bl':
                config.black_list = []
                print(config.pos + 'Reset blacklist')
            elif list_type == 'all':
                config.white_list = []
                config.black_list = []
                print(config.pos + 'Reset all')
            else:
                raise IndexError
        except IndexError:
            print(config.neg + 'Please specify a valid list to reset')
        except ValueError:
            print(config.neg + 'Item user wants to reset does not exist')