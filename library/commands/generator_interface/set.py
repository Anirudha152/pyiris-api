# GUI + CUI
# done
import library.modules.config as config

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def main(command):
    try:
        config.scout_values[command.split(' ')[1]][0] = command.split(' ', 2)[2]
        if interface == "CUI":
            print(config.pos + 'Set "' + command.split(' ')[1] + '" to "' + command.split(' ', 2)[2] + '"')
            if config.scout_values['Windows'][0] == 'True':
                config.generator_prompt = '\x1b[1m\x1b[37mPyIris (\x1b[0m\033[92m' + '\x1b[1m\x1b[32mGenerator\x1b[0m' + '\x1b[1m\x1b[37m@\x1b[0m\033[92m' + '\x1b[1m\x1b[32mWindows\x1b[0m' + '\x1b[1m\x1b[37m) > \x1b[0m'
            else:
                config.generator_prompt = '\x1b[1m\x1b[37mPyIris (\x1b[0m\033[92m' + '\x1b[1m\x1b[32mGenerator\x1b[0m' + '\x1b[1m\x1b[37m@\x1b[0m\033[92m' + '\x1b[1m\x1b[32mLinux\x1b[0m' + '\x1b[1m\x1b[37m) > \x1b[0m'
        elif interface == "GUI":
            log.log_normal('Set "' + command.split(' ')[1] + '" to "' + command.split(' ', 2)[2] + '"')
            return jsonify({"output": "Success", "output_message": "", "data": config.scout_values})
    except (IndexError, KeyError):
        print(config.neg + 'Please specify a valid option and value')
