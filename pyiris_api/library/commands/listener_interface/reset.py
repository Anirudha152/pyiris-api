# API
# done


def main(self, to_reset):
    try:
        local_static_values = {'Interface': ['0.0.0.0', 'The local interface to start a listener'],
                               'Port': ['9999', 'The local port to start a listener'],
                               'Name': ['Listener', 'Name of the listener'],
                               'Reply': ['',
                                         'The reply to send back in the case of a failed listener authentication/ connection']}
        option = to_reset
        if option in local_static_values:
            self.config.listener_values[option] = local_static_values[option]
            self.log.pos('Reset option : ' + option)
            return {"status": "ok", "message": 'Reset option : ' + option, "data": {"listener_values": self.config.listener_values}}
        elif option == 'all':
            self.config.listener_values = local_static_values
            self.log.pos('Reset all options')
            return {"status": "ok", "message": 'Reset all options', "data": {"listener_values": self.config.listener_values}}
        else:
            self.log.err('Please specify a valid option to reset')
            return {"status": "error", "message": 'Please specify a valid option to reset', "data": None}
    except IndexError:
        self.log.err('Please specify a valid option to reset')
        return {"status": "error", "message": 'Please specify a valid option to reset', "data": None}
