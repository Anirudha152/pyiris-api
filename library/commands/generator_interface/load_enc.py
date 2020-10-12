# GUI + CUI
# done
import library.modules.config as config
import library.modules.generator_id_parser as generator_id_parser

config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    from json import loads
    import library.modules.log as log


def load_enc(load_on):
    if load_on in config.encoders:
        load_on = config.encoders[load_on]
    else:
        if load_on in list(config.encoders.values()):
            pass
        else:
            raise KeyError
    if interface == "GUI":
        log.log_normal("Loaded : " + load_on)
    elif interface == "CUI":
        print(config.pos + 'Loaded : ' + load_on)
    config.loaded_encoders.append(load_on)


def main(command):
    print(command)
    if interface == "GUI":
        try:
            config.loaded_encoders = []
            load_on = loads(command.split(' ', 1)[1])
            if not load_on:
                config.loaded_encoders = []
                return jsonify({"output": "Success", "output_message": "", "data": [config.loaded_encoders, config.encoders]})
            for to_load in load_on:
                log.log_normal("Loading : " + config.encoders[str(to_load)])
                config.loaded_encoders.append(config.encoders[str(to_load)])
                log.log_normal("Loaded : " + config.encoders[str(to_load)])
            return jsonify({"output": "Success", "output_message": "", "data": [config.loaded_encoders, config.encoders]})
        except (KeyError, IndexError) as e:
            log.log_error("Error: " + str(e))
            raise e
            return jsonify({"output": "Fail", "output_message": "Invalid encoder ID", "data": ""})
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
