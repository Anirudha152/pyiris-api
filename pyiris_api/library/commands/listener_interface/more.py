# API
# done


def main(self, to_show):
    try:
        if to_show == 'all':
            keys = list(self.config.listener_database.keys())
            keys.sort()
            for i in keys:
                info = self.config.listener_database[i]
                self.log.inf('Advanced Info for : ' + i)
                self.log.blank('\n   ID                       : ' + i)
                self.log.blank('   Interface                : ' + info["host"])
                self.log.blank('   Port                     : ' + str(info["port"]))
                self.log.blank('   Assigned Name            : ' + info["name"])
                self.log.blank('   Started on               : ' + info["created_on"])
                self.log.blank('   Scout connection history : ')
                for scout_history in info["connections"]:
                    self.log.blank('    - ' + scout_history)
                self.log.blank('\n')
            return {"status": "ok", "message": "", "data": {"listener_database": self.config.listener_database}}
        else:
            info = self.config.listener_database[to_show]
            self.log.inf('Advanced Info :')
            self.log.blank('\n   ID                       : ' + to_show)
            self.log.blank('   Interface                : ' + info["host"])
            self.log.blank('   Port                     : ' + str(info["port"]))
            self.log.blank('   Assigned Name            : ' + info["name"])
            self.log.blank('   Started on               : ' + info["created_at"])
            self.log.blank('   Scout connection history : ')
            for scout_history in info["connections"]:
                self.log.blank('    - ' + scout_history)
            self.log.blank('\n')
            return {"status": "ok", "message": "", "data": {"listener_database": {to_show: info}}}
    except (IndexError, KeyError) as e:
        raise e
        self.log.err('Please specify a valid listener ID to show more info for')
        return {"status": "error", "message": "Please specify a valid listener ID to show more info for", "data": None}
