# WEB + COM
# done
import os
import library.modules.config as config
import library.modules.keygen as keygen

config.main()
interface = config.interface


def main(prompt = None):
    if interface == "GUI":
        command = prompt.split(' ', 1)
        move_back_to = os.getcwd()
        os.chdir(config.started_at)
        if len(command) == 1:
            output = keygen.main('user_initiated')
        elif len(command) == 2:
            output = keygen.main('user_initiated', command[1])
        os.chdir(move_back_to)
        return output
    elif interface == "CUI":
        move_back_to = os.getcwd()
        os.chdir(config.started_at)
        keygen.main('user_initiated')
        os.chdir(move_back_to)
