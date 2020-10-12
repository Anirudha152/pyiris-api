# GUI + CUI
# done
import collections
import library.modules.config as config
import library.modules.key_from_val as key_from_val
import library.modules.generator_id_parser as generator_id_parser


config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify
    import library.modules.log as log


def unload_com(load_off):
    if load_off == 'all':
        if config.scout_values['Windows'][0] == 'True':
            config.loaded_components = collections.OrderedDict()
            config.loaded_components['base'] = config.win_base_to_use
            if interface == "GUI":
                log.log_normal("Unloaded all loaded windows components")
            elif interface == "CUI":
                print(config.pos + 'Unloaded all loaded windows components')
        else:
            config.loaded_components = collections.OrderedDict()
            config.loaded_components['base'] = config.lin_base_to_use
            if interface == "GUI":
                log.log_normal("Unloaded all loaded linux components")
            elif interface == "CUI":
                print(config.pos + 'Unloaded all loaded linux components')
    else:
        if load_off == 'base' or key_from_val.main(config.loaded_components, load_off) == 'base':
            if interface == "GUI":
                log.log_warning("Do not unload base components, loading another base component will automatically replace the already loaded base component as there can only be one base component")
            elif interface == "CUI":
                print(config.war + 'Do not unload base components, loading another base component will automatically replace the already loaded base component as there can only be one base component')
            raise KeyError
        try:
            name = config.loaded_components[load_off]
            del (config.loaded_components[load_off])
            if interface == "GUI":
                log.log_normal("Unloaded : " + name)
            elif interface == "CUI":
                print(config.pos + 'Unloaded : ' + name)
            return
        except KeyError:
            del (config.loaded_components[key_from_val.main(config.loaded_components, load_off)])
            if interface == "GUI":
                log.log_normal("Unloaded : " + load_off)
            elif interface == "CUI":
                print(config.pos + 'Unloaded : ' + load_off)
            return


def main(command):
    try:
        load_off = command.split(' ', 1)[1]
        load_off = generator_id_parser.main(load_off, 'components', 'unload')
        load_off = list(map(str, load_off))
        for i in load_off:
            if interface == "GUI":
                log.log_normal("Unloading : " + str(i))
            elif interface == "CUI":
                print(config.inf + 'Unloading : ' + str(i))
            unload_com(str(i))
        if interface == "GUI":
            return jsonify({"output": "Success", "output_message": "", "data": ""})
    except (KeyError, IndexError):
        if interface == "GUI":
            log.log_error("Invalid component ID")
            return jsonify({"output": "Fail", "output_message": "Invalid component ID", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid component to unload or "all" to load all components. \x1b[1m\x1b[31mNote : "base" component cannot be unloaded\x1b[0m')
