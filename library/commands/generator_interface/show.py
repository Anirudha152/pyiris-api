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
            to_show = command.split(' ', 1)[1]
            if to_show == 'options':
                return jsonify({"output": "Success", "output_message": "", "data": config.scout_values})
            elif to_show == 'loaded':
                if config.scout_values['Windows'][0] == 'True':
                    win = True
                    #config.app.logger.info("[library/commands/generator_interface/show] - Generator is set to generate Windows specific scout")
                else:
                    win = False
                    #config.app.logger.info("[library/commands/generator_interface/show] - Generator is set to generate Linux specific scout")
                if win:
                    return jsonify({"output": "Success", "output_message": "", "data": [config.loaded_encoders, config.loaded_components, config.encoders, config.win_components]})
                else:
                    return jsonify({"output": "Success", "output_message": "", "data": [config.loaded_encoders, config.loaded_components, config.encoders, config.lin_components]})
            else:
                config.app.logger.error("[library/commands/generator_interface/show] - Error: Invalid command")
                return jsonify({"output": "Fail", "output_message": "Invalid command", "data": ""})
        except IndexError as e:
            config.app.logger.error("[library/commands/generator_interface/show] - Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": "Invalid command", "data": ""})
    elif interface == "CUI":
        try:
            to_show = command.split(' ', 1)[1]
            if to_show == 'options':
                header = [['    Option', 'Value', 'Info'], ['    ======', '=====', '====']]

                for o, v in config.scout_values.items():
                    header.append(['    ' + o, str(v[0]), v[1]])
                print('\n')
                l = [len(max(i, key=len)) for i in zip(*header)]
                print('\n'.join('     '.join(item[i].ljust(l[i]) for i in range(len(l)))
                                for item in header) + '\n')
            elif to_show == 'components':
                if config.scout_values['Windows'][0] == 'True':
                    print('\n' + config.inf + 'Generator is set to generate Windows scout')
                    print(config.inf + 'All loadable Windows components :')
                    for i in config.win_components:
                        print('   [' + i + '] ' + config.win_components[i])
                    print('')
                else:
                    print('\n' + config.inf + 'Generator is set to generate Linux scout')
                    print(config.inf + 'All loadable Linux components :')
                    for i in config.lin_components:
                        print('   [' + i + '] ' + config.lin_components[i])
                    print('')
            elif to_show == 'encoders':
                print('')
                print(config.inf + 'All encoders :')
                for i in config.encoders:
                    print('   [' + i + '] ' + config.encoders[i])
                print('')
            elif to_show == 'loaded':
                if config.scout_values['Windows'][0] == 'True':
                    print('\n' + config.inf + 'Generator is set to generate Windows specific scout')
                else:
                    print(config.inf + 'Generator is set to generate Linux specific scout')
                print(config.inf + 'Loaded components : ')
                for i in config.loaded_components:
                    if config.loaded_components[i].endswith('/base'):
                        print('   [-] ' + i)
                    else:
                        print('   [' + i + '] ' + config.loaded_components[i])
                print(
                    '\n' + config.inf + 'Encoder stack (Scout is encoded by the top encoder first then the next all the way to the bottom) : ')
                for i in range(len(config.loaded_encoders)):
                    print('   [' + str(i) + '] ' + config.loaded_encoders[i])
                print('')
            else:
                print(config.neg + 'Please specify a valid argument, ["options"|"components"|"loaded"|"encoders"]')
        except IndexError:
            print(config.neg + 'Please specify what to show, ["options"|"components"|"loaded"|"encoders"]')
