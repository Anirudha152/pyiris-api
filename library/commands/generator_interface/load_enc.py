# WEB + COM
# done
import library.modules.config as config
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
elif interface == "CUI":
    import library.modules.generator_id_parser as generator_id_parser

def load_enc(load_on):
    if load_on in config.encoders:
        load_on = config.encoders[load_on]
    else:
        if load_on in list(config.encoders.values()):
            pass
        else:
            raise KeyError
    if interface == "GUI":
        config.app.logger.info("[library/commands/generator_interface/load_enc] - Loaded : " + load_on)
    elif interface == "CUI":
        print(config.pos + 'Loaded : ' + load_on)
    config.loaded_encoders.append(load_on)


def main(command):
    if interface == "GUI":
        try:
            config.loaded_encoders = []
            load_on = command.split(' ', 1)[1]
            if load_on == "":
                config.loaded_encoders = []
                return jsonify({"output": "Success", "output_message": "", "data": [config.loaded_encoders, config.encoders]})
            load_on = load_on.split(',')
            for to_load in load_on:
                config.app.logger.info("[library/commands/generator_interface/load_enc] - Loading : " + config.encoders[to_load])
                config.loaded_encoders.append(config.encoders[to_load])
                config.app.logger.info("[library/commands/generator_interface/load_enc] - Loaded : " + config.encoders[to_load])
            return jsonify({"output": "Success", "output_message": "", "data": [config.loaded_encoders, config.encoders]})
        except (KeyError, IndexError) as e:
            config.app.logger.error("\x1b[1m\x1b[31m[library/commands/generator_interface/load_enc] - Error: " + str(e) + "\x1b[0m")
            return jsonify({"output": "Fail", "output_message": "Invalid component ID", "data": ""})
    elif interface == "CUI":
        try:
            load_on = command.split(' ', 1)[1]
            load_on = generator_id_parser.main(load_on, 'encoders', 'load')
            load_on = list(map(str, load_on))
            for i in load_on:
                print(config.inf + 'Loading : ' + i)
                load_enc(str(i))
        except (KeyError, IndexError):
            print(config.neg + 'Please specify a valid encoder to load')

