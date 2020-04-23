# WEB + COM
# done
import library.modules.key_from_val as key_from_val
import library.modules.config as config
import library.modules.generator_id_parser as generator_id_parser
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify


def load_com(load_on):
    if config.scout_values['Windows'][0] == 'True':
        if load_on in list(config.win_components.keys()):
            if config.win_components[load_on].startswith('windows/bases/') and config.win_components[load_on] not in list(config.loaded_components.values()):
                config.win_base_to_use = config.win_components[load_on]
                if interface == "GUI":
                    config.app.logger.info("[library/commands/generator_interface/load_com] - Replaced the loaded on base with new base : " + config.win_components[load_on])
                elif interface == "CUI":
                    print(config.pos + 'Replaced the loaded on base with new base : ' + config.win_components[load_on])
                return
            else:
                load_on = config.win_components[load_on]
        if load_on in list(config.loaded_components.values()):
            if interface == "GUI":
                config.app.logger.warning("[library/commands/generator_interface/load_com] - Component already loaded")
            elif interface == "CUI":
                print(config.neg + 'Component already loaded')
        else:
            id = key_from_val.main(config.win_components, load_on)
            if not id:
                raise KeyError
            if load_on.startswith('windows/bases/'):
                config.win_base_to_use = load_on
                if interface == "GUI":
                    config.app.logger.info("[library/commands/generator_interface/load_com] - Replaced the loaded on base with new base : " + load_on)
                elif interface == "CUI":
                    print(config.pos + 'Replaced the loaded on base with new base : ' + load_on)
                return
            else:
                config.loaded_components[id] = load_on
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/load_com] - Loaded : " + load_on)
            elif interface == "CUI":
                print(config.pos + 'Loaded : ' + load_on)
    else:
        if load_on in list(config.lin_components.keys()):
            if config.lin_components[load_on].startswith('linux/bases/') and config.lin_components[load_on] not in list(config.loaded_components.values()):
                config.lin_base_to_use = config.lin_components[load_on]
                if interface == "GUI":
                    config.app.logger.info("[library/commands/generator_interface/load_com] - Replaced the loaded on base with new base : " + config.lin_components[load_on])
                elif interface == "CUI":
                    print(config.pos + 'Replaced the loaded on base with new base : ' + config.lin_components[load_on])
                return
            else:
                load_on = config.lin_components[load_on]
        if load_on in list(config.loaded_components.values()):
            if interface == "GUI":
                config.app.logger.warning("[library/commands/generator_interface/load_com] - Component already loaded")
            elif interface == "CUI":
                print(config.neg + 'Component already loaded')
        else:
            id = key_from_val.main(config.lin_components, load_on)
            if not id:
                raise KeyError
            if load_on.startswith('linux/bases/'):
                config.win_base_to_use = load_on
                if interface == "GUI":
                    config.app.logger.info(
                        "[library/commands/generator_interface/load_com] - Replaced the loaded on base with new base : " + load_on)
                elif interface == "CUI":
                    print(config.pos + 'Replaced the loaded on base with new base : ' + load_on)
                return
            config.loaded_components[id] = load_on
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/load_com] - Loaded : " + load_on)
            elif interface == "CUI":
                print(config.pos + 'Loaded : ' + load_on)


def main(command):
    try:
        load_on = command.split(' ', 1)[1]
        load_on = generator_id_parser.main(load_on, 'components', 'load')
        load_on = list(map(str, load_on))
        for i in load_on:
            if interface == "GUI":
                config.app.logger.info("[library/commands/generator_interface/load_com] - Loading : " + i)
            elif interface == "CUI":
                print(config.inf + 'Loading : ' + i)
            load_com(str(i))
        if interface == "GUI":
            return jsonify({"output": "Success", "output_message": "", "data": ""})
    except (KeyError, IndexError) as e:
        if interface == "GUI":
            config.app.logger.error("\x1b[1m\x1b[31m[library/commands/generator_interface/load_com] - Error: " + str(e) + "\x1b[0m")
            return jsonify({"output": "Fail", "output_message": "Invalid component ID", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid component to load or "all" to load all components. \x1b[1m\x1b[31mNote : the default component, */base is loaded by default\x1b[0m')
