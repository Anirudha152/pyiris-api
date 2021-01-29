# API
# done


def main(self, key, val):
    try:
        self.config.listener_values[str(key)][0] = str(val)
        self.log.pos('Set "' + str(key) + '" to "' + str(val) + '"')
        return {"status": "ok", "message": 'Set "' + str(key) + '" to "' + str(val) + '"', "data": {"listener_values": self.config.listener_values}}
    except (IndexError, KeyError) as e:
        self.log.err('Please specify a valid option and value')
        return {"status": "error", "message": 'Please specify a valid option and value', "data": None}
