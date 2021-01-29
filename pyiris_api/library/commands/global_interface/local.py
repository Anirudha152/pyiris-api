# CUI
# done
import os
import subprocess
import time


def main(self, prompt):
    try:
        self.log.blank("\n")
        self.log.err('Executing locally...\n')
        if prompt[:3] == 'cd ':
            try:
                os.chdir(prompt[3:])
                self.log.pos('Changed to directory : ' + prompt[3:] + '\n')
            except (WindowsError, OSError):
                self.log.err('Could not change to directory : ' + prompt[3:] + '\n')
        else:
            result = subprocess.Popen(prompt, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      stdin=subprocess.PIPE)
            result = result.stdout.read() + result.stderr.read()
            self.log.blank(result.decode())
    except EOFError:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            self.log.inf('Cancelled local command execution')
    except KeyboardInterrupt:
        self.log.inf('Cancelled local command execution')
