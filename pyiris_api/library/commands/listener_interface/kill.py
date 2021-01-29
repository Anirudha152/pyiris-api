# API
# done


def main(self, to_kill):
    try:
        id = str(to_kill)
        if id in list(self.config.listener_database.keys()):
            del (self.config.listener_database[id])
            self.log.inf('Sent kill message to listener of ID : ' + id + '...')
            return {"status": "ok", "message": 'Sent kill message to listener of ID : ' + id + '...', "data": {"listener_database": self.config.listener_database}}
        elif id == 'all':
            self.log.inf('Sent kill message to all listeners')
            self.config.listener_database = {}
            return {"status": "ok", "message": 'Sent kill message to all listeners', "data": {"listener_database": self.config.listener_database}}
        else:
            self.log.err('Listener of ID : ' + id + ' is not active')
            return {"status": "error", "message": 'Listener of ID : ' + id + ' is not active', "data": None}
    except IndexError:
        self.log.err('Please specify the ID of the listener to kill, or specify "all"')
        return {"status": "error", "message": 'Please specify the ID of the listener to kill, or specify "all"', "data": None}
