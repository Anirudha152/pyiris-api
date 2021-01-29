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
                self.log.blank('   Interface                : ' + info[0])
                self.log.blank('   Port                     : ' + str(info[1]))
                self.log.blank('   Assigned Name            : ' + info[2])
                self.log.blank('   Started on               : ' + info[3])
                self.log.blank('   Scout connection history : ')
                for scout_history in info[4]:
                    self.log.blank('    - ' + scout_history)
                self.log.blank('\n')
            return {"status": "ok", "message": "", "data": {"listener_database": self.config.listener_database}}
        else:
            info = self.config.listener_database[to_show]
            self.log.inf('Advanced Info : ')
            self.log.blank('\n   ID                       : ' + to_show)
            self.log.blank('   Interface                : ' + info[0])
            self.log.blank('   Port                     : ' + str(info[1]))
            self.log.blank('   Assigned Name            : ' + info[2])
            self.log.blank('   Started on               : ' + info[3])
            self.log.blank('   Scout connection history : ')
            for scout_history in info[4]:
                self.log.blank('    - ' + scout_history)
            self.log.blank('\n')
            return {"status": "ok", "message": "", "data": {"listener_database_" + to_show: self.config.listener_database}}
    except (IndexError, KeyError) as e:
        self.log.err('Please specify a valid listener ID to show more info for')
        return {"status": "error", "message": "Please specify a valid listener ID to show more info for", "data": None}
