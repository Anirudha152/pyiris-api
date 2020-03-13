import re
import library.modules.config as config
config.main()
interface = config.interface


def main(inp_data, context_type, operation):
    data = inp_data.replace(' ', '')
    if data == 'all':  # filter special cases
        if context_type == 'components' and operation == 'load':
            if config.scout_values['Windows'][0] == 'True':
                return [str(i) for i in list(config.win_components.keys()) if
                        not config.win_components[str(i)].startswith('windows/bases/')]
            else:
                return [str(i) for i in list(config.lin_components.keys()) if
                        not config.lin_components[str(i)].startswith('linux/bases/')]
        elif data == 'all' and operation == 'unload':
            return ['all']
        elif context_type == 'encoders' and operation == 'load':
            return list(config.encoders.keys())

    # Actual formatting occurs here

    error = False
    output_list = []  # final list of individual sorted values
    ranges = []  # ranges to process later
    non_ranges = []
    inp_data = inp_data.strip()  # strip input data of all leading and ending whitespace
    data = inp_data.split(',')  # split by comma
    if context_type == 'components':
        data = list(set(data))  # remove all duplicates after comma split

    for i in data:
        if re.match('^[0-9]+\-[0-9]+$',
                    i):  # initialize regex match to format of range IDs, matches "positive number-positive number"
            ranges.append(i)
        else:
            non_ranges.append(i)
    # process non ranges first
    for i in non_ranges:
        try:
            output_list.append(int(i))
        except:
            error = True  # indicate formatting error
            break
    if error and output_list:  # we hit an error however we still hit a match indicating invalid format
        if interface == "GUI":
            config.app.logger.error("[library/modules/generator_id_parser] - Invalid generator ID formatting : String detected while sorting for integer IDs")
        elif interface == "CUI":
            print(config.neg + 'Invalid generator ID formatting : String detected while sorting for integer IDs')
        return []
    elif error and not output_list and not ranges:  # nothing in non ranges is an integer and there are no proper ranges meaning string based input only
        if interface == "GUI":
            config.app.logger.info("[library/modules/generator_id_parser] - Generator found no IDs")
        elif interface == "CUI":
            print(config.inf + 'Generator found no IDs')
        if type(inp_data) is list:
            return inp_data
        return [inp_data]  # most probably a direct call for the component which we return

    # ERROR OUTPUT_LIST BOOLEAN CHEATSHEET
    # error and non zero output_list TT -> indicates that in non range some are ints others are not which is invalid formatting
    # no error and zero output_list FF -> not possible due to the nature of try: except, one or the other happens
    # error and zero output_list TF -> indicates that nothing in non ranges is an integer meaning string only or range only formatting
    # no error and non zero output_list FT -> indicates that everything in non ranges is integer

    # iterate range values to add to output
    try:
        for i in ranges:
            f_val, s_val = i.split('-', 1)
            # even if f_val and s_val are non zero numbers that start with digit 0, INTing them normalizes it
            f_val = int(f_val)
            s_val = int(s_val)
            # f_val and s_val are never negative since regex matches "positive number-positive number"
            if f_val > s_val:
                if interface == "GUI":
                    config.app.logger.error("[library/modules/generator_id_parser] - Invalid generator ID formatting : First range value is larger than second range value")
                elif interface == "CUI":
                    print(config.neg + 'Invalid generator ID formatting : First range value is larger than second range value')
                return []
            else:  # 0 < f < s
                mini_range = list(range(f_val, s_val + 1))  # add 1 to account for the final val
                output_list += mini_range  # fill each value in range of f and s into output
    except OverflowError:
        if interface == "GUI":
            config.app.logger.error("[library/modules/generator_id_parser] - Range value is too large")
        elif interface == "CUI":
            print(config.neg + 'Invalid generator ID formatting : Range value is too large')
        return []
    if context_type == 'components':
        output_list = list(set(output_list))  # remove all duplicates in the range addition section ^
        output_list.sort()  # sort for better eyecandy when loading components
    if interface == "GUI":
        config.app.logger.info("[library/modules/generator_id_parser] - Generator ID formatting successful")
    elif interface == "CUI":
        print(config.pos + 'Generator ID formatting successful')
    if type(output_list) is list:
        return output_list
    return [output_list]  # final function iterates through output
