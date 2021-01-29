# CUI
# done
import os


def main(self):
    try:
        self.log.inf('Opening python interpreter on local system')
        os.system('python')
    except KeyboardInterrupt:
        pass
    self.log.inf('Exiting...')
