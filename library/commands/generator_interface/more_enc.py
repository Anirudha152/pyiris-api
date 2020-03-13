# WEB + COM
# done
import library.modules.config as config
import library.modules.generator_id_parser as generator_id_parser
config.main()
interface = config.interface
if interface == "GUI":
    from flask import jsonify

tmp_enc = list(config.encoders.values())
for i in tmp_enc:
    exec ('import encoders.' + i.replace('/', '.') + ' as ' + i.replace('/', '_'))
print(config.pos + 'Loaded all encoders info - OK')


def more_enc(load_on):
    if load_on in config.encoders:
        load_on = config.encoders[load_on]
    else:
        if load_on in list(config.encoders.values()):
            pass
        else:
            raise KeyError
    if interface == "GUI":
        output = my_exec(load_on.replace('/', '_') + '.main("info")')
        return output
    elif interface == "CUI":
        exec(load_on.replace('/', '_') + '.main("info")')


def main(command):
    try:
        load_on = command.split(' ', 1)[1]
        if load_on == 'all':
            output = {}
            for i in config.encoders.keys():
                if interface == "GUI":
                    output[i] = more_enc(str(i))
                elif interface == "CUI":
                    more_enc(str(i))
        else:
            load_on = generator_id_parser.main(load_on, 'encoders', None)
            load_on = list(map(str, load_on))
            for i in load_on:
                if interface == "GUI":
                    output = more_enc(str(i))
                elif interface == "CUI":
                    more_enc(str(i))
        if interface == "GUI":
            return jsonify({"output": "Success", "output_message": "", "data": output})
    except (IndexError, KeyError) as e:
        if interface == "GUI":
            config.app.logger.error("[library/commands/generator_interface/more_enc] - Error: " + str(e))
            return jsonify({"output": "Fail", "output_message": "Invalid component ID", "data": ""})
        elif interface == "CUI":
            print(config.neg + 'Please specify a valid encoder to show more info for')

def my_exec(code):
    exec('global j; j = %s' % code)
    global j
    return j