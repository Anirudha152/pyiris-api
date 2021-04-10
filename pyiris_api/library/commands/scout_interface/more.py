# API
# done


def main(self, to_show):
    try:
        if to_show == 'all':
            keys = list(self.config.scout_database.keys())
            keys.sort()
            for i in keys:
                info = self.config.scout_database[i]
                self.log.inf('Advanced Info for : ' + i)
                self.log.blank('\n   Socket Object : ' + str(info["conn_object"]))
                self.log.blank('   Remote Scout Host : ' + info["host"])
                self.log.blank('   Remote Scout Port : ' + info["port"])
                self.log.blank('   Connected through : ' + info["connection_through"])
                self.log.blank('   Name              : ' + info["name"])
                self.log.blank('   Connected at      : ' + info["connected_at"])
                self.log.blank('   Connection Type   : ' + info["connection_type"])
                self.log.blank('\n')
            return {"status": "ok", "message": "", "data": {"scout_database": self.config.scout_database}}
        else:
            info = self.config.scout_database[to_show]
            self.log.inf('Advanced Info for : ' + to_show)
            self.log.blank('\n   Socket Object     : ' + str(info["conn_object"]))
            self.log.blank('   Remote Scout Host : ' + info["host"])
            self.log.blank('   Remote Scout Port : ' + info["port"])
            self.log.blank('   Connected through : ' + info["connection_through"])
            self.log.blank('   Name              : ' + info["name"])
            self.log.blank('   Connected at      : ' + info["connected_at"])
            self.log.blank('   Connection Type   : ' + info["connection_type"])
            self.log.blank('\n')
            return {"status": "ok", "message": "", "data": {"scout_database": {to_show: self.config.scout_database[to_show]}}}
    except (IndexError, KeyError):
        self.log.err('Please specify a valid scout ID to show more info for')
        return {"status": "ok", "message": "Please specify a valid scout ID to show more info for", "data": None}
