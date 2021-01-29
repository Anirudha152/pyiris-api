# API
# done
import pyiris_api.library.modules.keygen as keygen
import os


def main(self, key=None):
    move_back_to = os.getcwd()
    os.chdir(self.config.started_at)
    to_return = keygen.main(self, True, key)
    os.chdir(move_back_to)
    return to_return
