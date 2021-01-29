# API
# done
import os


def main(self, to_reset):
    try:
        local_static_values = {'Host': [self.config.private_ip,
                                        'The local hostname to connect back to (Reverse) or the interface to listen on (Bind). You can set multiple hostnames to connect back to by separating them with commas'],
                               'Port': ['9999',
                                        'The local port to connect back on (Reverse) or the remote port to listen on (Bind)'],
                               'Timeout': ['5', 'The timeout value for the scout'],
                               'Windows': [['True' if os.name != "nt" else "False"][0], 'When "True", will generate a windows scout, else a linux scout'],
                               'Dir': [os.path.join(self.config.started_at, 'generated'),
                                        'Directory to generate payload in'],
                               'Compile': ['False',
                                           'When "True", will compile scout to EXE (windows) or ELF (Linux), '
                                           'else it will not compile']}
        option = to_reset
        if option in local_static_values:
            self.config.scout_values[option] = local_static_values[option]
            self.log.pos('Reset option : ' + option)
            return {"status": "ok", "message": "Reset option : " + option, "data": {"scout_values": self.config.scout_values}}
        elif option == 'all':
            self.config.scout_values = local_static_values
            self.log.pos('Reset all options')
            return {"status": "ok", "message": "Reset all options : " + option, "data": {"scout_values": self.config.scout_values}}
        else:
            self.log.err('Please specify a valid option to reset')
            return {"status": "error", "message": "Please specify a valid option to reset", "data": None}
    except IndexError:
        self.log.err('Please specify a valid option to reset')
        return {"status": "error", "message": "Please specify a valid option to reset", "data": None}
