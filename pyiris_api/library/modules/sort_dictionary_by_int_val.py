# API
# done
import collections


def main(dictionary):
    tmp_dict = collections.OrderedDict()
    try:
        tmp_list = list(dictionary.keys())
        for i in sorted(map(int, tmp_list)):
            tmp_dict[str(i)] = dictionary[str(i)]
        return tmp_dict
    except TypeError:
        return dictionary
